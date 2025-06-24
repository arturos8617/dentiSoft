import logging
import uuid

import pytest
from django.urls import reverse
from django.utils import timezone

from core.api.permissions import CanInvitePermission
from core.models import Clinica
from core.models import InvitacionUsuario
from core.models import Rol
from dentisoft.users.models import User

pytestmark = pytest.mark.django_db


def create_clinica_and_rol():
    role_name = CanInvitePermission.authorized_roles[0]
    rol, _ = Rol.objects.get_or_create(nombre=role_name, defaults={"descripcion": ""})
    clinica = Clinica.objects.create(
        nombre="Clinica",
        direccion="Dir",
        telefono="123",
        email="c@example.com",
    )
    return rol, clinica


def test_create_invitation_enqueues_task(client, user, monkeypatch):
    rol, clinica = create_clinica_and_rol()
    user.clinica = clinica
    user.rol = rol
    user.save()
    client.force_login(user)
    called = {}

    def fake_delay(inv_id):
        called["id"] = str(inv_id)

    monkeypatch.setattr("core.api.views.enviar_invitacion_email.delay", fake_delay)

    url = reverse("api:invitacionusuario-list")
    response = client.post(
        url,
        {
            "email": "invitee@example.com",
            "rol": rol.id,
            "clinica": clinica.id,
        },
    )

    assert response.status_code == 201
    invitation_id = response.json()["id"]
    assert called["id"] == invitation_id
    assert InvitacionUsuario.objects.filter(id=invitation_id).exists()
    invitation = InvitacionUsuario.objects.get(id=invitation_id)
    assert invitation.ip_creacion == "127.0.0.1"


def test_invite_register_creates_user(client):
    rol, clinica = create_clinica_and_rol()
    invitacion = InvitacionUsuario.objects.create(
        email="new@example.com",
        token="token123",
        rol=rol,
        clinica=clinica,
        fecha_expiracion=timezone.now() + timezone.timedelta(days=1),
    )
    data = {
        "token": invitacion.token,
        "first_name": "New",
        "last_name": "User",
        "email": invitacion.email,
        "password1": "Pass1234",
        "password2": "Pass1234",
        "telefono": "1234567",
        "fecha_nacimiento": timezone.now().date(),
        "genero": "M",
    }
    url = reverse("invite-register")
    response = client.post(url, data)

    assert response.status_code == 201
    invitacion.refresh_from_db()
    assert invitacion.estado == "usada"
    user = User.objects.get(email=invitacion.email)
    assert response.json() == {"id": str(user.id), "email": user.email}
    assert user.rol == rol
    assert user.clinica == clinica


def test_invite_register_email_mismatch(client):
    """Registration fails if provided email doesn't match invitation."""
    rol, clinica = create_clinica_and_rol()
    invitacion = InvitacionUsuario.objects.create(
        email="new2@example.com",
        token="token456",
        rol=rol,
        clinica=clinica,
        fecha_expiracion=timezone.now() + timezone.timedelta(days=1),
    )
    data = {
        "token": invitacion.token,
        "first_name": "New",
        "last_name": "User",
        "email": "wrong@example.com",
        "password1": "Pass1234",
        "password2": "Pass1234",
        "telefono": "1111",
        "fecha_nacimiento": timezone.now().date(),
        "genero": "M",
    }
    url = reverse("invite-register")
    response = client.post(url, data)

    assert response.status_code == 400
    assert "email" in response.json()


def test_invite_register_unique_phone(client):
    """Registration fails if phone already exists."""
    rol, clinica = create_clinica_and_rol()
    InvitacionUsuario.objects.create(
        email="dup@example.com",
        token="token789",
        rol=rol,
        clinica=clinica,
        fecha_expiracion=timezone.now() + timezone.timedelta(days=1),
    )
    User.objects.create_user(
        email="other@example.com",
        password="pass",
        first_name="A",
        last_name="B",
        telefono="9999",
        fecha_nacimiento=timezone.now().date(),
        genero="M",
        rol=rol,
        clinica=clinica,
    )
    data = {
        "token": "token789",
        "first_name": "Foo",
        "last_name": "Bar",
        "email": "dup@example.com",
        "password1": "Pass1234",
        "password2": "Pass1234",
        "telefono": "9999",
        "fecha_nacimiento": timezone.now().date(),
        "genero": "M",
    }
    url = reverse("invite-register")
    response = client.post(url, data)

    assert response.status_code == 400
    assert "telefono" in response.json()


def test_invite_register_password_policy(client):
    rol, clinica = create_clinica_and_rol()
    invitacion = InvitacionUsuario.objects.create(
        email="policy@example.com",
        token="tokpol",
        rol=rol,
        clinica=clinica,
        fecha_expiracion=timezone.now() + timezone.timedelta(days=1),
    )
    data = {
        "token": invitacion.token,
        "first_name": "N",
        "last_name": "U",
        "email": invitacion.email,
        "password1": "short",
        "password2": "short",
        "telefono": "1234",
        "fecha_nacimiento": timezone.now().date(),
        "genero": "M",
    }
    url = reverse("invite-register")
    response = client.post(url, data)

    assert response.status_code == 400
    assert "password1" in response.json()


def test_invite_register_recaptcha_required(client, settings, monkeypatch):
    rol, clinica = create_clinica_and_rol()
    invitacion = InvitacionUsuario.objects.create(
        email="bot@example.com",
        token="tokcap",
        rol=rol,
        clinica=clinica,
        fecha_expiracion=timezone.now() + timezone.timedelta(days=1),
    )
    settings.RECAPTCHA_REQUIRED = True
    monkeypatch.setattr("core.api.serializers.verify_recaptcha", lambda t: False)
    data = {
        "token": invitacion.token,
        "first_name": "B",
        "last_name": "O",
        "email": invitacion.email,
        "password1": "Pass1234",
        "password2": "Pass1234",
        "telefono": "123",
        "fecha_nacimiento": timezone.now().date(),
        "genero": "M",
        "recaptcha": "token",
    }
    url = reverse("invite-register")
    response = client.post(url, data)

    assert response.status_code == 400
    assert "recaptcha" in response.json()


def test_invite_register_invalid_token(client):
    data = {
        "token": "invalid",
        "first_name": "Bad",
        "last_name": "Guy",
        "email": "bad@example.com",
        "password1": "Pass1234",
        "password2": "Pass1234",
        "telefono": "1234567",
        "fecha_nacimiento": timezone.now().date(),
        "genero": "M",
    }
    url = reverse("invite-register")
    response = client.post(url, data)

    assert response.status_code == 400
    assert "token" in response.json()
    assert not User.objects.filter(email="bad@example.com").exists()



def test_create_invitation_logs(client, user, caplog):
    rol, clinica = create_clinica_and_rol()
    user.clinica = clinica
    user.rol = rol
    user.save()
    client.force_login(user)
    url = reverse("api:invitacionusuario-list")

    with caplog.at_level(logging.INFO, logger="core.api.views"):
        client.post(
            url,
            {
                "email": "log@example.com",
                "rol": rol.id,
                "clinica": clinica.id,
            },
        )

    assert any("log@example.com" in record.getMessage() for record in caplog.records)


def create_user_with_role_clinic(rol, clinica, *, email=None):
    if email is None:
        email = f"user-{uuid.uuid4()}@example.com"
    return User.objects.create_user(
        email=email,
        password="pass",
        first_name="John",
        last_name="Doe",
        telefono="123",
        fecha_nacimiento=timezone.now().date(),
        genero="M",
        rol=rol,
        clinica=clinica,
    )


def test_invite_with_nonexistent_role(client):
    rol, clinica = create_clinica_and_rol()
    user = create_user_with_role_clinic(rol, clinica, email="user1@example.com")
    client.force_login(user)

    url = reverse("api:invitacionusuario-list")
    response = client.post(
        url,
        {"email": "a@b.com", "rol": 9999, "clinica": clinica.id},
    )

    assert response.status_code == 400
    assert "rol" in response.json()


def test_invite_to_other_clinic(client):
    rol, clinica = create_clinica_and_rol()
    other_clinic = Clinica.objects.create(
        nombre="Otra", direccion="Dir", telefono="123", email="o@example.com",
    )
    user = create_user_with_role_clinic(rol, clinica, email="user2@example.com")
    client.force_login(user)

    url = reverse("api:invitacionusuario-list")
    response = client.post(
        url,
        {"email": "a@b.com", "rol": rol.id, "clinica": other_clinic.id},
    )

    assert response.status_code == 400
    assert "clinica" in response.json()


def test_non_cca_invites_cca(client):
    rol_user = Rol.objects.create(nombre="dentista", descripcion="")
    rol_cca, _ = Rol.objects.get_or_create(nombre="CCA", defaults={"descripcion": ""})
    clinica = Clinica.objects.create(
        nombre="Clinica1", direccion="Dir", telefono="123", email="c1@example.com",
    )
    user = create_user_with_role_clinic(rol_user, clinica, email="user3@example.com")
    client.force_login(user)

    url = reverse("api:invitacionusuario-list")
    response = client.post(
        url,
        {"email": "a@b.com", "rol": rol_cca.id, "clinica": clinica.id},
    )

    assert response.status_code == 400
    assert "rol" in response.json()

def test_invite_existing_active_user(client):
    """Creating invitation for an existing active user should fail."""
    rol, clinica = create_clinica_and_rol()
    inviter = create_user_with_role_clinic(rol, clinica, email="user4@example.com")
    active_user = create_user_with_role_clinic(rol, clinica, email="user5@example.com")
    active_user = create_user_with_role_clinic(rol, clinica)
    client.force_login(inviter)

    url = reverse("api:invitacionusuario-list")
    response = client.post(
        url,
        {"email": active_user.email, "rol": rol.id, "clinica": clinica.id},
    )

    assert response.status_code == 400
    assert "email" in response.json()


def test_invite_duplicate_pending(client):
    """Submitting a second pending invitation for same email and clinic fails."""
    rol, clinica = create_clinica_and_rol()
    inviter = create_user_with_role_clinic(rol, clinica, email="user6@example.com")
    client.force_login(inviter)

    InvitacionUsuario.objects.create(
        email="pending@example.com",
        token="tok123",
        rol=rol,
        clinica=clinica,
        invitado_por=inviter,
        fecha_expiracion=timezone.now() + timezone.timedelta(days=1),
    )

    url = reverse("api:invitacionusuario-list")
    response = client.post(
        url,
        {"email": "pending@example.com", "rol": rol.id, "clinica": clinica.id},
    )

    assert response.status_code == 400
    assert "non_field_errors" in response.json()

