from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    class Sex(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'
        NOT_STATED = 'not_stated'

    id = models.AutoField(primary_key=True)
    username = models.CharField(null=True, unique=False, max_length=150, db_index=True)
    email = models.EmailField(null=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    sex = models.CharField(choices=Sex.choices, default=Sex.NOT_STATED, max_length=255)
    phone = models.CharField(max_length=20, null=True, db_index=True)
    auth_code = models.CharField(max_length=4, db_index=True)
    referral_code = models.ForeignKey('referral_system.ReferralCode', on_delete=models.CASCADE, null=True,
                                      related_name='user')
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'id'
    # USERNAME_FIELD = 'phone'
    groups = None
    user_permissions = None

    def __str__(self):
        return self.phone
