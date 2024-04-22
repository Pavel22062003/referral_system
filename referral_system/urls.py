from rest_framework import routers

from referral_system.views import ReferralViewSet, BalanceOperationViewSet

router = routers.SimpleRouter()
router.register('referral_system', viewset=ReferralViewSet, basename='referral_system')
router.register('balance_operation', viewset=BalanceOperationViewSet, basename='balance_operation')
urlpatterns = router.urls
