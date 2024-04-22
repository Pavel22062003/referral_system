from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from referral_system.serializers import ReferralSerializer
from referral_system.services.referral_system_manager import ReferralSystemManager


# from user.models import User
# from .filters import ReferralFilter
# from .models import ReferralCode, Referral
# from .serializers import ReferralCodeSerializer, ReferralSerializer
# from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from customer.models import Customer


# class ReferralCodeViewSet(viewsets.ModelViewSet):
#     # queryset = ReferralCode.objects.all()
#     # serializer_class = ReferralCodeSerializer
#     # permission_classes = [IsAdminUser]


class ReferralViewSet(viewsets.ReadOnlyModelViewSet):
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
