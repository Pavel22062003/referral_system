from rest_framework.exceptions import ValidationError
from datetime import datetime
from referral_system.models import ReferralCode, Referral, AccrualSettings, BalanceOperation
from user.models import User
import random
import string


class ReferralSystemManager:
    def __init__(self, user: User):
        self.user = user

    def get_referral_code(self):
        if not self.user.referral_code_id:
            self.user.referral_code = ReferralCode.objects.create(number=self._get_number())
            self.user.save(update_fields=('referral_code',))
        return self.user.referral_code

    def activate_referral_code(self, number: int):
        referral_code = ReferralCode.objects.filter(number=number).first()
        if not referral_code:
            raise ValidationError({'error': 'Referral code not found.'})
        if Referral.objects.filter(user=self.user).exists():
            raise ValidationError({'error': 'Referral code already activated.'})
        return Referral.objects.create(user=self.user, referral_code=referral_code)

    def try_to_approve_referral(self):
        referral = Referral.objects.filter(user=self.user).first()
        if not referral:
            return
        settings = AccrualSettings.get_instance()
        if settings.for_referral:
            referral.balance_operation = BalanceOperation.objects.create(
                user=self.user,
                title='Активация реферальной ссылки',
                message='Спасибо, что пользуетесь приложением',
                sum=settings.for_referral,
                event=BalanceOperation.Event.REFERRAL
            )
            referral.approved_at = datetime.utcnow()
            referral.save()

        if not settings.for_referral_code_owner:
            return

        operation = BalanceOperation.objects.create(
            customer=referral.referral_code.user,
            title='Бонус за рекомендацию',
            message='Поздравляем, по вашей ссылке совершон вход',
            sum=settings.for_referral_code_owner,
            event=BalanceOperation.Event.REFERRAL,
        )

    @staticmethod
    def _get_number():
        letters = ''.join(random.choices(string.ascii_letters, k=3))
        digits = ''.join(random.choices(string.digits, k=3))
        code = ''.join(random.sample(letters + digits, k=6))
        referral_code = ReferralCode.objects.filter(number=code).first()
        if not referral_code:
            return code
        else:
            return ReferralSystemManager._get_number()
