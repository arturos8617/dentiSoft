import pytest
from django.urls import reverse

from core.models import Rol, Clinica

pytestmark = pytest.mark.django_db


def test_roles_endpoint_returns_data(client, user):
    Rol.objects.create(nombre="test", descripcion="")
    client.force_login(user)
    url = reverse("api:rol-list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.json()


def test_clinicas_endpoint_returns_data(client, user):
    Clinica.objects.create(nombre="C1", direccion="D", telefono="123", email="a@e.com")
    client.force_login(user)
    url = reverse("api:clinica-list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.json()
