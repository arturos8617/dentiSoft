# core/api/serializers.py
import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import InvitacionUsuario, Clinica, Rol

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
        extra_kwargs = {
            "fecha_expiracion": {"required": False},
        }

    def validate_email(self, value):
        """Ensure there isn't already an active user with this email."""
        if User.objects.filter(email=value, activo=True).exists():
            raise ValidationError("Este correo ya está registrado")
        return value

    def validate(self, attrs):
        """Additional validation for invitations."""
        request = self.context.get("request")

        rol_id = self.initial_data.get("rol")
        clinica_id = self.initial_data.get("clinica")

        try:
            rol = Rol.objects.get(pk=rol_id)
        except Rol.DoesNotExist as exc:  # noqa: B904
            raise ValidationError({"rol": "Rol inválido"}) from exc

        try:
            clinica = Clinica.objects.get(pk=clinica_id)
        except Clinica.DoesNotExist as exc:  # noqa: B904
            raise ValidationError({"clinica": "Clínica inválida"}) from exc

        attrs["rol"] = rol
        attrs["clinica"] = clinica        
        email = attrs.get("email")
        if (
            email
            and InvitacionUsuario.objects.filter(
                email=email, clinica=clinica, estado="pendiente"
            ).exists()
        ):
            raise ValidationError("Ya existe una invitación pendiente para este correo")
        
        if request:
            if getattr(request.user, "clinica_id", None) != clinica.id:
                raise ValidationError({"clinica": "Clínica inválida para este usuario"})

            rol_nombre = getattr(getattr(request.user, "rol", None), "nombre", None)
            if rol.nombre == "CCA" and rol_nombre != "CCA":
                raise ValidationError({"rol": "No puede asignar el rol CCA"})

        return attrs

    def create(self, validated_data):
        """Create an ``InvitacionUsuario`` assigning defaults when needed."""

        if not validated_data.get("fecha_expiracion"):
            validated_data["fecha_expiracion"] = timezone.now() + timedelta(days=7)

        validated_data["token"] = uuid.uuid4().hex
        # Aquí podrías disparar un task de Celery para enviar el e-mail
        return super().create(validated_data)


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
        except InvitacionUsuario.DoesNotExist as exc:
            msg = "Token inválido o ya usado/expirado."
            raise ValidationError(msg) from exc

        if inv.fecha_expiracion < timezone.now():
            msg = "La invitación ha expirado."
            raise ValidationError(msg)

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
