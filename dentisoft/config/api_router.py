from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from core.api.views import InvitacionUsuarioViewSet
from dentisoft.users.api.views import UserViewSet


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("invitaciones", InvitacionUsuarioViewSet)


app_name = "api"
urlpatterns = router.urls
