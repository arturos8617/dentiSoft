from rest_framework.permissions import BasePermission


class CanInvitePermission(BasePermission):
    """Allow access only to users that can send invitations."""

    authorized_roles = ["dentista", "recepcionista", "CCA"]

    def has_permission(self, request, view):
        role_name = getattr(getattr(request.user, "rol", None), "nombre", None)
        return bool(role_name in self.authorized_roles)
    