from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse

from core.models import InvitacionUsuario


@shared_task()
def enviar_invitacion_email(invitacion_id: str) -> None:
    invitacion = InvitacionUsuario.objects.get(id=invitacion_id)
    subject = "Invitación a DentiSoft"
    mensaje = (
        "Has sido invitado a unirte a DentiSoft. "
        f"Utiliza este token para registrarte: {invitacion.token}"
    )
    send_mail(subject, mensaje, None, [invitacion.email])

