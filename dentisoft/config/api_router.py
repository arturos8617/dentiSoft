from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from dentisoft.users.api.views import UserViewSet
from core.api.views import InvitacionUsuarioViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("invitaciones", InvitacionUsuarioViewSet)


app_name = "api"
urlpatterns = router.urls
