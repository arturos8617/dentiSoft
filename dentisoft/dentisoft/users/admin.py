from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from django import forms

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User
from core.models import Rol, Clinica


if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Forzar que el login del admin pase por el flujo de django-allauth
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


class CustomUserChangeForm(UserAdminChangeForm):
    """
    Extiende el formulario de cambio de usuario para exponer campos adicionales.
    """
    class Meta(UserAdminChangeForm.Meta):
        model = User
        fields = "__all__"  # Incluye rol, clinica y activo junto con los campos estándar


class CustomUserCreationForm(UserAdminCreationForm):
    """
    Extiende el formulario de creación de usuario para exponer rol, clinica y activo.
    """
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=False)
    clinica = forms.ModelChoiceField(queryset=Clinica.objects.all(), required=False)
    activo = forms.BooleanField(required=False, initial=True)

    class Meta(UserAdminCreationForm.Meta):
        model = User
        fields = ("email", "rol", "clinica", "activo")

    def clean_password2(self):
        # Validación de contraseñas duplicada ya viene en UserAdminCreationForm,
        # así que simplemente llamamos al padre.
        return super().clean_password2()

    def save(self, commit=True):
        user = super().save(commit=False)
        # “set_password” ya se realiza en el save() de la clase base
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    """
    Admin personalizado para el modelo User, mostrando y permitiendo editar
    los campos rol, clinica y activo en los formularios de creación y edición.
    """
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Campos que se muestran en la vista de detalle (editar usuario)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (_("Permisos"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        (_("Información personalizada"), {"fields": ("rol", "clinica", "activo")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Campos que se muestran en el formulario de creación de usuario
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "rol", "clinica", "activo", "password1", "password2"),
            },
        ),
    )

    list_display = ("email", "name", "rol", "clinica", "is_staff", "is_superuser", "activo")
    list_filter = ("is_staff", "is_superuser", "is_active", "rol", "clinica")
    search_fields = ("email", "name")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions",)
