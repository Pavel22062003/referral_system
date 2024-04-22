from user.models import User
from user.serializers import UserMainSerializer


class UserManager:
    def __init__(self, user: User):
        self.user = user

    def get_profile(self):
        user_data = UserMainSerializer(instance=self.user).data

