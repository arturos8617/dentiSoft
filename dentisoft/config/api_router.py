from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from core.api.views import (
    InvitacionUsuarioViewSet,
    RolViewSet,
    ClinicaViewSet,
)
from dentisoft.users.api.views import UserViewSet


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("invitaciones", InvitacionUsuarioViewSet)

router.register("roles", RolViewSet)
router.register("clinicas", ClinicaViewSet)

app_name = "api"
urlpatterns = router.urls
