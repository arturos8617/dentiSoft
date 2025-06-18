from typing import ClassVar
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from core.models import Clinica, Rol
from .managers import UserManager


class User(AbstractUser):
    """
    Modelo de usuario personalizado para DentiSoft,
    con campos obligatorios: first_name, last_name, telefono, fecha_nacimiento.
    """

    # Override default username fields
    username = None
    email = models.EmailField(_("email address"), unique=True)

    # Datos personales obligatorios
    first_name = models.CharField(_("Nombre"), max_length=30)
    last_name = models.CharField(_("Apellidos"), max_length=150)
    telefono = models.CharField(_("Teléfono"), max_length=20)
    fecha_nacimiento = models.DateField(_("Fecha de nacimiento"))

    # Opcional / adicionales
    avatar = models.ImageField(
        _("Foto de perfil"),
        upload_to="avatars/",
        blank=True,
        null=True,
        default="avatars/default-avatar.jpg",
    )
    genero = models.CharField(
        _("Género"),
        max_length=10,
        choices=[
            ("M", "Masculino"),
            ("F", "Femenino"),
            ("O", "Otro"),
            ("N", "Prefiero no decir"),
        ],
        blank=True,
    )

    # Relación con tu dominio
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE)
    activo = models.BooleanField(_("Activo"), default=True)

    # Autenticación
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "telefono", "fecha_nacimiento"]

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.id})
