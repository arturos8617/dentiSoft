import pytest
from celery.result import EagerResult
from django.core import mail

from core.tasks import send_test_email

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

