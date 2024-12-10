from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

from carLoudApp.projects.choices import DrivetrainChoices


UserModel = get_user_model()


class Project(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='projects',
    )

    title = models.CharField(
        max_length=30,
    )

    brand = models.CharField(
        max_length=40,
    )

    model = models.CharField(
        max_length=40,
    )

    year = models.PositiveIntegerField()

    description = models.TextField(
        null=True,
        blank=True,
    )

    horsepower = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    drivetrain = models.CharField(
        max_length=3,
        choices=DrivetrainChoices.choices,
    )

    private = models.BooleanField(
        default=False,
    )

    created_at = models.DateField(
        auto_now_add=True,
    )

    @property
    def brand_and_model(self):
        return f'{self.brand} {self.model}'

    def __str__(self):
        return self.title

class ProjectPost(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='posts',
    )

    image = CloudinaryField('project_image')

    caption = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.project}: post'

