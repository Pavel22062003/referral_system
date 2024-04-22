from rest_framework import routers

from referral_system.views import ReferralViewSet

router = routers.SimpleRouter()
router.register('referral_system', viewset=ReferralViewSet, basename='referral_system')
urlpatterns = router.urls
