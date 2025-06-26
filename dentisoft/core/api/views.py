import logging

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.permissions import CanInvitePermission
from core.api.serializers import InvitacionUsuarioSerializer
from core.api.serializers import InviteRegisterSerializer
from core.api.serializers import RolSerializer, ClinicaSerializer
from core.models import InvitacionUsuario, Rol, Clinica
from core.tasks import enviar_invitacion_email

logger = logging.getLogger(__name__)

class InvitacionUsuarioViewSet(viewsets.ModelViewSet):
    queryset = InvitacionUsuario.objects.all()
    serializer_class = InvitacionUsuarioSerializer
    permission_classes = [IsAuthenticated, CanInvitePermission]


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