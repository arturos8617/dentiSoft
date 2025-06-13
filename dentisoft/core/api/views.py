from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.api.serializers import InvitacionUsuarioSerializer, InviteRegisterSerializer
from core.models import InvitacionUsuario
from core.tasks import enviar_invitacion_email


class InvitacionUsuarioViewSet(viewsets.ModelViewSet):
    queryset = InvitacionUsuario.objects.all()
    serializer_class = InvitacionUsuarioSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["invitado_por"] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        invitacion = serializer.save()
        enviar_invitacion_email.delay(invitacion.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InviteRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = InviteRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"id": str(user.id), "email": user.email}, status=status.HTTP_201_CREATED)
