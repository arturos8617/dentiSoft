from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import User
from .forms import UserAdminChangeForm, UserAdminCreationForm
from core.models import Rol, Clinica


if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


class CustomUserChangeForm(UserAdminChangeForm):
    """Formulario de edición en Admin, expone todos los campos relevantes."""
    class Meta(UserAdminChangeForm.Meta):
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "telefono",
            "avatar",
            "fecha_nacimiento",
            "genero",
            "rol",
            "clinica",
            "activo",
        )


class CustomUserCreationForm(UserAdminCreationForm):
    """Formulario de creación en Admin, con validación de campos obligatorios."""
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=True)
    clinica = forms.ModelChoiceField(queryset=Clinica.objects.all(), required=True)
    activo = forms.BooleanField(required=False, initial=True)

    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=150)
    telefono = forms.CharField(required=True, max_length=20)
    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    genero = forms.ChoiceField(
        choices=User._meta.get_field("genero").choices,
        required=False,
    )
    avatar = forms.ImageField(required=False)

    class Meta(UserAdminCreationForm.Meta):
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "telefono",
            "fecha_nacimiento",
            "genero",
            "avatar",
            "rol",
            "clinica",
            "activo",
        )

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get("password1")
        pw2 = cleaned.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Edición de usuario
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {
            "fields": (
                "first_name",
                "last_name",
                "telefono",
                "avatar",
                "fecha_nacimiento",
                "genero",
            )
        }),
        (_("Permisos"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        (_("Información personalizada"), {
            "fields": ("rol", "clinica", "activo")
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Creación de usuario
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "telefono",
                "fecha_nacimiento",
                "genero",
                "avatar",
                "rol",
                "clinica",
                "activo",
                "password1",
                "password2",
            ),
        }),
    )

    list_display = (
        "email",
        "first_name",
        "last_name",
        "rol",
        "clinica",
        "is_staff",
        "is_superuser",
        "activo",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "rol", "clinica")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")
