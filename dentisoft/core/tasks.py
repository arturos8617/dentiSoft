from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from core.models import InvitacionUsuario


@shared_task()
def send_test_email(recipient: str) -> bool:
    """Send a test email with plain text and HTML versions."""
    context = {"domain": settings.SITE_DOMAIN}
    text_body = render_to_string("email/test_email.txt", context)
    html_body = render_to_string("email/test_email.html", context)
    message = EmailMultiAlternatives(
        subject="Test Email",
        body=text_body,
        to=[recipient],
        from_email=settings.DEFAULT_FROM_EMAIL,
    )
    message.attach_alternative(html_body, "text/html")
    message.send()
    return True


@shared_task()
def enviar_invitacion_email(invitacion_id: str) -> bool:
    """Send invitation email to the provided address."""
    invitacion = InvitacionUsuario.objects.get(id=invitacion_id)
    invitation_url = (
        f"https://{settings.SITE_DOMAIN}/api/invite-register/?token="
        f"{invitacion.token}"
    )
    context = {
        "domain": settings.SITE_DOMAIN,
        "invitation_url": invitation_url,
        "expiration_date": invitacion.fecha_expiracion,
    }
    text_body = render_to_string("email/invitation_email.txt", context)
    html_body = render_to_string("email/invitation_email.html", context)
    message = EmailMultiAlternatives(
        subject=_("Invitation to register"),
        body=text_body,
        to=[invitacion.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
    )
    message.attach_alternative(html_body, "text/html")
    message.send()
    return True


