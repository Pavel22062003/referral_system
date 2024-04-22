from django.urls import path
from . import views
from user_interface.apps import UserInterfaceConfig

app_name = UserInterfaceConfig.name

urlpatterns = [
    path('', views.all_user_events, name='events'),
    path('logout/', views.logout_func, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('enter_phone', views.enter_phone_number, name='enter_phone'),
    path('enter_code', views.enter_verification_code, name='enter_code'),
    path('activate_referral_code', views.enter_referral_code, name='activate_referral_code'),
]
