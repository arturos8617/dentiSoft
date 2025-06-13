import pytest
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
        "name": "New User",
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
        "name": "Bad",
        "email": "bad@example.com",
        "password": "pass",
    }
    url = reverse("invite-register")
    response = client.post(url, data)

    assert response.status_code == 400
    assert "token" in response.json()
    assert not User.objects.filter(email="bad@example.com").exists()
