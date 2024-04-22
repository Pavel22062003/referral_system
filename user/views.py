from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.serializers import UserMainSerializer
from user.services.phone_auth_manager import PhoneAuthManager
from user.services.register_manager import RegisterManager


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action in ['auth_phone', 'register', 'auth']:
            permissions = []
        return [permission() for permission in permissions]

    @action(methods=['POST'], detail=False)
    def auth_phone(self, request):
        manager = PhoneAuthManager(data=request.data)
        return Response(manager.process_user())

    @action(methods=['POST'], detail=False)
    def register(self, request):
        manager = RegisterManager(data=request.data)
        return Response(manager.process())

    @action(methods=['POST'], detail=False)
    def auth(self, request):
        manager = RegisterManager(data=request.data)
        return Response(manager.authenticate())

    @action(methods=['GET'], detail=False)
    def profile(self, request):
        user = request.user
        extra_data = {'show_referrals': True}
        data = UserMainSerializer(instance=user, context={'extra_data': extra_data}).data

        return Response(data)
