from django import forms


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label='Phone Number')


class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(max_length=4, label='Verification Code')
