from rest_framework import routers
from user.views import UserViewSet

router = routers.SimpleRouter()
router.register('user', viewset=UserViewSet, basename='user')
urlpatterns = router.urls
