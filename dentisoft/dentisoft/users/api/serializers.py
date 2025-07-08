from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from dentisoft.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    rol = serializers.CharField(source="rol.nombre", read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "rol", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Add additional user information into the JWT claims."""

    @classmethod
    def get_token(cls, user: User):  # type: ignore[override]
        token = super().get_token(user)
        token["rol"] = getattr(user.rol, "nombre", "")
        token["clinica_id"] = user.clinica_id
        return token