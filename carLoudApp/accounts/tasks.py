from celery import shared_task
from django.core.mail import EmailMessage

from django.conf import settings

@shared_task
def send_email_task(subject, body, to_email):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_FROM_USER,
        to=[to_email],
    )
    email.send()
