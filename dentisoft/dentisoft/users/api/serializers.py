from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from dentisoft.users.models import User


class UserListSerializer(serializers.ModelSerializer[User]):
    """Lightweight serializer for listing users."""

    rol = serializers.CharField(source="rol.nombre", read_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "rol", "activo"]


class UserDetailSerializer(serializers.ModelSerializer[User]):
    """Full serializer used on detail and update views."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "telefono",
            "fecha_nacimiento",
            "genero",
            "rol",
            "clinica",
            "activo",
        ]
        read_only_fields = ["id", "email"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Add additional user information into the JWT claims."""

    @classmethod
    def get_token(cls, user: User):  # type: ignore[override]
        token = super().get_token(user)
        token["rol"] = getattr(user.rol, "nombre", "")
        token["clinica_id"] = user.clinica_id
        return token