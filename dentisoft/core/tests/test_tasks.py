import pytest
from celery.result import EagerResult
from django.core import mail

from django.utils import timezone

from core.models import Clinica, InvitacionUsuario, Rol
from core.tasks import enviar_invitacion_email, send_test_email

pytestmark = pytest.mark.django_db


def test_send_test_email(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.SITE_DOMAIN = "example.com"
    result = send_test_email.delay("test@example.com")
    assert isinstance(result, EagerResult)
    assert result.result is True
    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    assert message.to == ["test@example.com"]
    assert message.body.strip() == "Hello from example.com!"
    assert message.alternatives[0][0].strip() == (
        "<p>Hello from <strong>example.com</strong>!</p>"
    )


def test_enviar_invitacion_email(settings, user):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.SITE_DOMAIN = "example.com"

    rol = Rol.objects.create(nombre="Rol", descripcion="")
    clinica = Clinica.objects.create(
        nombre="Clinica",
        direccion="Dir",
        telefono="123",
        email="c@example.com",
    )
    invitacion = InvitacionUsuario.objects.create(
        email="invitee@example.com",
        token="token123",
        rol=rol,
        clinica=clinica,
        invitado_por=user,
        fecha_expiracion=timezone.now(),
    )

    result = enviar_invitacion_email.delay(str(invitacion.id))
    assert isinstance(result, EagerResult)
    assert result.result is True
    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    url = f"https://example.com/api/invite-register/?token={invitacion.token}"
    assert message.to == ["invitee@example.com"]
    assert url in message.body
    assert url in message.alternatives[0][0]

