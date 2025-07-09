from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView


from dentisoft.users.models import User

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserDetailSerializer,
    UserListSerializer,
)


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """ViewSet for authenticated user operations."""

    serializer_class = UserListSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    def get_serializer_class(self):
        action = getattr(self, "action", None)
        if action in {"retrieve", "update", "partial_update", "me"}:
            return UserDetailSerializer
        return UserListSerializer

    @action(detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer