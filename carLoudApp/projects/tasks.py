import cloudinary.uploader
from celery import shared_task
from django.shortcuts import get_object_or_404
from pathlib import Path

from carLoudApp.projects.models import ProjectPost


@shared_task
def upload_to_cloudinary(temp_file_path, post_pk):
    post = get_object_or_404(ProjectPost, pk=post_pk)

    response = cloudinary.uploader.upload(temp_file_path)
    post.image = response['url']
    post.save()

    Path(temp_file_path).unlink(missing_ok=True)
