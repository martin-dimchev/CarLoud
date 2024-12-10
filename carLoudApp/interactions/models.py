from django.contrib.auth import get_user_model
from django.db import models

from carLoudApp.accounts.models import Profile
from carLoudApp.projects.models import ProjectPost

UserModel = get_user_model()

class Like(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    post = models.ForeignKey(
        ProjectPost,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    def __str__(self):
        return f'{self.user}->{self.post}: like'

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        ProjectPost,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.post}: comment'


class Follower(models.Model):
    follower = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='following',
    )
    is_following = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='followers',
    )

    class Meta:
        unique_together = ('follower', 'is_following')