import cloudinary.uploader
from celery import shared_task
from django.shortcuts import get_object_or_404
from carLoudApp.projects.models import ProjectPosts
import cloudinary
from pathlib import Path


@shared_task
def upload_to_cloudinary(temp_file_path, post_pk):
    post = get_object_or_404(ProjectPosts, pk=post_pk)
    response = cloudinary.uploader.upload(temp_file_path)
    post.image = response['url']
    post.save()
    Path(temp_file_path).unlink(missing_ok=True)
