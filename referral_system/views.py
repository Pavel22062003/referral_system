from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from referral_system.models import BalanceOperation
from referral_system.serializers import ReferralSerializer
from referral_system.services.referral_system_manager import ReferralSystemManager


class ReferralViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def get_referral_code(self, request):
        user = request.user
        return Response({'referral_code': user.referral_code.number})

    @action(methods=['PUT'], detail=False)
    def activate_referral_code(self, request):
        code = request.data.get('code')
        if not code:
            raise ValidationError({'code': 'is required'})
        manager = ReferralSystemManager(user=request.user)
        result = manager.activate_referral_code(code)
        manager.try_to_approve_referral()
        return Response(ReferralSerializer(instance=result).data)


class BalanceOperationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return BalanceOperation.objects.filter(user=user)
