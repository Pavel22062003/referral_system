from rest_framework.exceptions import ValidationError
import random
from user.models import User
import time
from loguru import logger


class PhoneAuthManager:
    def __init__(self, data):
        self.data = data
        self.phone = None
        self.is_valid = False
        self.user: User | None = None

    def validate(self):
        phone = self.data.get('phone')
        if not phone:
            raise ValidationError({'phone': 'Phone number must be provided'})
        self.user = User.objects.filter(phone=phone).first()
        # if users:
        #     raise ValidationError({'error': 'user with this phone already exists'})
        self.is_valid = True
        self.phone = phone

    def process_user(self):
        if not self.is_valid:
            self.validate()
        code = self.generate_verify_token()
        time.sleep(2)
        if not self.user:
            User.objects.create(auth_code=code, phone=self.phone)
        else:
            self.user.auth_code = code
            self.user.save()
        logger.info(code)
        return code

    @staticmethod
    def generate_verify_token():
        code = ''
        for num in range(4):
            code += str(random.randint(0, 9))
        return code
