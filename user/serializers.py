from air_drf_relation.serializers import AirModelSerializer, AirRelatedField

from referral_system.models import Referral
from referral_system.serializers import ReferralCodeSerializer
from user.models import User
from rest_framework import serializers


class RegisterSerializer(AirModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    referral_code = AirRelatedField(ReferralCodeSerializer, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'is_staff', 'last_name', 'email', 'password', 'middle_name',
                  'is_superuser', 'sex', 'username', 'auth_code', 'referral_code')
        read_only_fields = ('is_superuser',)


class UserMainSerializer(AirModelSerializer):
    referral_code = AirRelatedField(ReferralCodeSerializer, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'is_staff', 'last_name', 'email', 'middle_name',
                  'is_superuser', 'sex', 'username', 'auth_code', 'referral_code')
        read_only_fields = ('is_superuser',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        extra_data = self.context.get('extra_data')
        if extra_data and extra_data.get('show_referrals'):
            referrals = Referral.objects.filter(referral_code_id=instance.referral_code_id).values_list('user__phone',
                                                                                                        flat=True)
            data['referrals'] = referrals
        return data
