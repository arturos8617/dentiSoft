import pytest
import logging
from django.urls import reverse
from django.utils import timezone

from core.models import Clinica, Rol, InvitacionUsuario
from dentisoft.users.models import User

pytestmark = pytest.mark.django_db


def create_clinica_and_rol():
    rol = Rol.objects.create(nombre="Rol", descripcion="")
    clinica = Clinica.objects.create(
        nombre="Clinica",
        direccion="Dir",
        telefono="123",
        email="c@example.com",
    )
    return rol, clinica


def test_create_invitation_enqueues_task(client, user, monkeypatch):
    client.force_login(user)
    rol, clinica = create_clinica_and_rol()
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
        "password": "pass1234",
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


def test_invite_register_invalid_token(client):
    data = {
        "token": "invalid",
        "first_name": "Bad",
        "last_name": "Guy",
        "email": "bad@example.com",
        "password": "pass",
    }
    url = reverse("invite-register")
    response = client.post(url, data)

    assert response.status_code == 400
    assert "token" in response.json()
    assert not User.objects.filter(email="bad@example.com").exists()



def test_create_invitation_logs(client, user, caplog):
    client.force_login(user)
    rol, clinica = create_clinica_and_rol()
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


def create_user_with_role_clinic(rol, clinica):
    return User.objects.create_user(
        email="user@example.com",
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
    user = create_user_with_role_clinic(rol, clinica)
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
        nombre="Otra", direccion="Dir", telefono="123", email="o@example.com"
    )
    user = create_user_with_role_clinic(rol, clinica)
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
    rol_cca = Rol.objects.create(nombre="CCA", descripcion="")
    clinica = Clinica.objects.create(
        nombre="Clinica1", direccion="Dir", telefono="123", email="c1@example.com"
    )
    user = create_user_with_role_clinic(rol_user, clinica)
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
    inviter = create_user_with_role_clinic(rol, clinica)
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
    inviter = create_user_with_role_clinic(rol, clinica)
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

