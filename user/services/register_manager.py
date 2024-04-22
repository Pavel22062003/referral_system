from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from referral_system.services.referral_system_manager import ReferralSystemManager
from user.models import User
from user.serializers import RegisterSerializer


class RegisterManager:
    def __init__(self, data):
        self.data = data
        self.validated_data = None
        self.user: User | None = None

    def process(self):
        self.validate()
        self.update_user()
        return self.get_jwt_token()

    def validate(self):
        serializer = RegisterSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        self.validated_data = serializer.validated_data
        code = self.validated_data['auth_code']
        user = User.objects.filter(auth_code=code).first()
        if not user:
            raise ValidationError({'code': 'Invalid auth code'})
        self.user = user

    def update_user(self):
        password = self.validated_data['password']
        for key, value in self.validated_data.items():
            setattr(self.user, key, value)
        self.user.set_password(password)
        self.user.save()
        ReferralSystemManager(user=self.user).get_referral_code()

    def get_jwt_token(self):
        refresh = TokenObtainPairSerializer.get_token(self.user)
        data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
        return data

    def authenticate(self):
        phone = self.data.get('phone')
        if not phone:
            raise ValidationError({'phone': 'Missing phone'})
        password = self.data.get('password')
        if not password:
            raise ValidationError({'password': 'Missing password'})
        user = User.objects.filter(phone=phone).first()
        if not user:
            raise ValidationError({'no_user': 'with this credentials'})
        if not user.check_password(password):
            raise ValidationError({'no_user': 'with this credentials'})
        self.user = user
        return self.get_jwt_token()
