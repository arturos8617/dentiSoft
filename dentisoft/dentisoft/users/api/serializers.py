from rest_framework import serializers

from dentisoft.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    rol = serializers.CharField(source="rol.nombre", read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "rol", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
