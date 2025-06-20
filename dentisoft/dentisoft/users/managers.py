from typing import TYPE_CHECKING

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ImproperlyConfigured
from core.models import Rol, Clinica


if TYPE_CHECKING:
    from .models import User  # noqa: F401


class UserManager(DjangoUserManager["User"]):
    """Custom manager for the User model."""

    def _create_user(self, email: str, password: str | None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            msg = "The given email must be set"
            raise ValueError(msg)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):  # type: ignore[override]
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):  # type: ignore[override]

        try:
            default_rol = Rol.objects.get(nombre="CCA")
            default_clinica = Clinica.objects.get(nombre="Default Clinic")
        except Rol.DoesNotExist:
            raise ImproperlyConfigured("Falta el Rol por defecto 'CCA'. Aplica las migraciones de core.")
        except Clinica.DoesNotExist:
            raise ImproperlyConfigured("Falta la Clínica por defecto 'Default Clinic'. Aplica las migraciones de core.")

        # Asignar por defecto rol y clinica si no vienen en extra_fields
        extra_fields.setdefault("rol", default_rol)
        extra_fields.setdefault("clinica", default_clinica)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("activo", True)


        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self._create_user(email, password, **extra_fields)
