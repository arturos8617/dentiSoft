# core/api/serializers.py
import uuid
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from core.models import InvitacionUsuario
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class InvitacionUsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para crear y listar InvitacionUsuario.
    - Genera token y expiración si no se proveen.
    """
    class Meta:
        model = InvitacionUsuario
        fields = [
            "id",
            "email",
            "rol",
            "clinica",
            "invitado_por",
            "fecha_creacion",
            "fecha_expiracion",
            "estado",
        ]
        read_only_fields = ["id", "fecha_creacion", "estado"]

    def create(self, validated_data):
        # Si no se envió fecha_expiracion, la ponemos a +7 días
        if not validated_data.get("fecha_expiracion"):
            validated_data["fecha_expiracion"] = timezone.now() + timedelta(days=7)
        # Generar token único
        validated_data["token"] = uuid.uuid4().hex
        invitacion = super().create(validated_data)
        # Aquí podrías disparar un task de Celery para enviar el e-mail
        return invitacion


class InviteRegisterSerializer(serializers.Serializer):
    """
    Serializer para registrar un User a partir de un token de invitación.
    """
    token = serializers.CharField()
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            inv = InvitacionUsuario.objects.get(token=value, estado="pendiente")
        except InvitacionUsuario.DoesNotExist:
            raise ValidationError("Token inválido o ya usado/expirado.")
        if inv.fecha_expiracion < timezone.now():
            raise ValidationError("La invitación ha expirado.")
        return inv

    def create(self, validated_data):
        inv = validated_data.pop("token")
        # Crear el usuario con los datos de la invitación
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
            rol=inv.rol,
            clinica=inv.clinica,
        )
        # Marcar invitación como usada
        inv.estado = "usada"
        inv.save()
        return user
