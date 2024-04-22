from django.db import models

from core.models import BaseModel
from user.models import User


# Create your models here.
class ReferralCode(BaseModel):
    number = models.CharField(db_index=True, unique=True, max_length=6)


class Referral(BaseModel):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='referrals')
    referral_code = models.ForeignKey('referral_system.ReferralCode', on_delete=models.CASCADE,
                                      related_name='referrals', null=True)
    balance_operation = models.ForeignKey('referral_system.BalanceOperation', on_delete=models.SET_NULL, null=True)
    approved_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BalanceOperation(BaseModel):
    class Event(models.TextChoices):
        REFERRAL = 'referral'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balance_operations')
    event = models.CharField(max_length=32, choices=Event.choices, db_index=True, null=True)
    sum = models.IntegerField(default=0)
    title = models.CharField(max_length=128)
    previous_balance = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    message = models.CharField(max_length=256, null=True)
    description = models.CharField(max_length=512, null=True)


class AccrualSettings(BaseModel):
    for_referral = models.IntegerField(default=20)
    for_referral_code_owner = models.IntegerField(default=20)

    @staticmethod
    def get_instance():
        instance = AccrualSettings.objects.all().first()
        if not instance:
            instance = AccrualSettings.objects.create()
        return instance
