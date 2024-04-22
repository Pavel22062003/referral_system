from air_drf_relation.serializers import AirModelSerializer

from referral_system.models import ReferralCode, Referral


class ReferralCodeSerializer(AirModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ('uuid', 'number', 'created_at')


class ReferralSerializer(AirModelSerializer):

    class Meta:
        model = Referral
        fields = ('uuid', 'user', 'referral_code', 'created_at', 'approved_at', 'balance_operation')

