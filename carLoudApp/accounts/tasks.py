from pathlib import Path
import cloudinary.uploader
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404

from carLoudApp.accounts.models import Profile


@shared_task
def send_email_task(subject, body, to_email):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_FROM_USER,
        to=[to_email],
    )

    email.send()


@shared_task
def upload_to_cloudinary(temp_file_path, profile_pk):
    profile = get_object_or_404(Profile, pk=profile_pk)

    response = cloudinary.uploader.upload(temp_file_path)
    profile.image = response['url']
    profile.save()

    Path(temp_file_path).unlink(missing_ok=True)