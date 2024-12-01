from django.contrib.auth import get_user_model
from django.db import models

from carLoudApp.accounts.models import Profile
from carLoudApp.projects.models import ProjectImages

UserModel = get_user_model()

class Like(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    image = models.ForeignKey(
        ProjectImages,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    class Meta:
        unique_together = ('user', 'image')


class Comment(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    image = models.ForeignKey(
        ProjectImages,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
