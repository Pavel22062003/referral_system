from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from referral_system.models import Referral
from django.shortcuts import redirect
from django.shortcuts import render

from referral_system.services.referral_system_manager import ReferralSystemManager
from user.models import User
from user.services.phone_auth_manager import PhoneAuthManager
from user_interface.forms import PhoneNumberForm, VerificationCodeForm


def logout_func(request):
    logout(request)
    return redirect('user_interface:enter_phone')


def enter_phone_number(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['phone_number']
            data = {'phone': number}
            PhoneAuthManager(data=data).process_user()
            request.session['phone_number'] = number
            return redirect('user_interface:enter_code')
    else:
        form = PhoneNumberForm()
    return render(request, 'user_interface/enter_phone.html', {'form': form})


def enter_verification_code(request):
    error_message = None
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['verification_code']
            phone = request.session.get('phone_number')
            user = User.objects.filter(phone=phone, auth_code=entered_code).first()
            if not user:
                error_message = "Неверный проверочный код"
                form = VerificationCodeForm()
                return render(request, 'user_interface/enter_code.html', {'form': form, 'error_message': error_message})
            login(request, user)
            ReferralSystemManager(user=user).get_referral_code()
            return redirect('user_interface:profile')
    else:
        form = VerificationCodeForm()
    return render(request, 'user_interface/enter_code.html', {'form': form, 'error_message': error_message})


def all_user_events(request):
    return render(request, 'user_interface/base.html')


@login_required
def profile(request):
    user = request.user
    referral_info = Referral.objects.filter(user=user).first()
    error_info = request.session.get('error_message')
    return render(request, 'user_interface/profile.html',
                  {'user': user, 'referral_info': referral_info, 'error_info': error_info})


@login_required
def enter_referral_code(request):
    error_message = None
    if request.method == 'POST':
        referral_code = request.POST.get('referral_code')
        user = request.user
        try:
            manager = ReferralSystemManager(user=user)
            manager.activate_referral_code(referral_code)
        except Exception as e:
            error_message = e.detail['error']
            request.session['error_message'] = error_message
    return redirect('user_interface:profile')
