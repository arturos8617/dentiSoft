import logging

from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.permissions import CanInvitePermission
from core.api.serializers import ClinicaSerializer
from core.api.serializers import InvitacionUsuarioSerializer
from core.api.serializers import InviteRegisterSerializer
from core.api.serializers import RolSerializer
from core.models import Clinica
from core.models import InvitacionUsuario
from core.models import Rol
from core.tasks import enviar_invitacion_email

logger = logging.getLogger(__name__)

class InvitacionUsuarioViewSet(viewsets.ModelViewSet):
    queryset = InvitacionUsuario.objects.all()
    serializer_class = InvitacionUsuarioSerializer
    permission_classes = [IsAuthenticated, CanInvitePermission]

    def get_permissions(self):
        """Allow unauthenticated access when validating by token."""
        if (
            self.action == "list"
            and "token" in self.request.query_params
        ):
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        token = self.request.query_params.get("token")
        qs = super().get_queryset()
        if token:
            return qs.filter(
                token=token,
                estado="pendiente",
                fecha_expiracion__gt=timezone.now(),
            )
        return qs

    def list(self, request, *args, **kwargs):
        token = request.query_params.get("token")
        if token:
            queryset = self.filter_queryset(self.get_queryset())
            if not queryset.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitacion = serializer.save(
            invitado_por=request.user,
            ip_creacion=request.META.get("REMOTE_ADDR"),
        )

        logger.info(
            "Invitation created: inviter=%s invitee=%s role=%s clinic=%s ip=%s",
            request.user.id,
            invitacion.email,
            invitacion.rol_id,
            invitacion.clinica_id,
            invitacion.ip_creacion,
        )
        enviar_invitacion_email.delay(invitacion.id)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

class InviteRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = InviteRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"id": str(user.id), "email": user.email},
            status=status.HTTP_201_CREATED,
        )


class RolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer


class ClinicaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Clinica.objects.all()
    serializer_class = ClinicaSerializer