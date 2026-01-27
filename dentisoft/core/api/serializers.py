# core/api/serializers.py
import json
import re
import uuid
from datetime import timedelta
from urllib import parse
from urllib import request

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Clinica
from core.models import InvitacionUsuario
from core.models import Rol


def verify_recaptcha(token: str) -> bool:
    """Validate recaptcha token with Google."""
    secret = getattr(settings, "RECAPTCHA_SECRET_KEY", "")
    if not secret:
        return False
    data = parse.urlencode({"secret": secret, "response": token}).encode()
    req = request.Request(
        "https://www.google.com/recaptcha/api/siteverify",
        data=data,
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=5) as resp:  # noqa: S310
            payload = json.loads(resp.read().decode())
    except Exception:  # noqa: BLE001
        return False
    return bool(payload.get("success"))


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
        except Rol.DoesNotExist as exc:
            raise ValidationError({"rol": "Rol inválido"}) from exc

        try:
            clinica = Clinica.objects.get(pk=clinica_id)
        except Clinica.DoesNotExist as exc:
            raise ValidationError({"clinica": "Clínica inválida"}) from exc

        attrs["rol"] = rol
        attrs["clinica"] = clinica
        email = attrs.get("email")
        if (
            email
            and InvitacionUsuario.objects.filter(
                email=email, clinica=clinica, estado="pendiente",
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
    """Serializer para registrar un ``User`` desde una invitación."""

    token = serializers.CharField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    telefono = serializers.CharField(max_length=20)
    fecha_nacimiento = serializers.DateField()
    genero = serializers.ChoiceField(choices=User._meta.get_field("genero").choices)
    recaptcha = serializers.CharField(write_only=True, required=False)
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

    def validate(self, attrs):
        inv = attrs.get("token")
        if attrs.get("email") != inv.email:
            raise ValidationError({"email": "El email no coincide con la invitación"})

        if User.objects.filter(email=attrs["email"]).exists():
            raise ValidationError({"email": "Este correo ya está registrado"})

        if User.objects.filter(telefono=attrs["telefono"]).exists():
            raise ValidationError({"telefono": "Este teléfono ya está registrado"})

        password = attrs.get("password1")
        if password != attrs.get("password2"):
            raise ValidationError({"password2": "Las contraseñas no coinciden"})

        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[0-9!@#$%^&*()_+=\-]", password):
            raise ValidationError({"password1": "La contraseña no cumple la política"})

        if getattr(settings, "RECAPTCHA_REQUIRED", False):
            token = attrs.get("recaptcha")
            if not token or not verify_recaptcha(token):
                raise ValidationError({"recaptcha": "ReCaptcha inválido"})

        return attrs

    def create(self, validated_data):
        inv = validated_data.pop("token")
        validated_data.pop("password2")
        validated_data.pop("recaptcha", None)
        password = validated_data.pop("password1")
        with transaction.atomic():
            user = User.objects.create_user(
                email=validated_data["email"],
                password=password,
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                telefono=validated_data["telefono"],
                fecha_nacimiento=validated_data["fecha_nacimiento"],
                genero=validated_data["genero"],
                rol=inv.rol,
                clinica=inv.clinica,
            )
            inv.estado = "usada"
            inv.save()
        return user
    

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ["id", "nombre", "descripcion"]


class ClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinica
        fields = ["id", "nombre", "direccion", "telefono", "email"]
