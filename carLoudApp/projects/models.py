from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
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
    make = models.CharField(
        max_length=40,
    )
    model = models.CharField(
        max_length=40,
    )
    year = models.PositiveIntegerField()
    description = models.TextField()
    horsepower = models.FloatField(
        MinValueValidator(0, 'Horsepower can not be less than zero'),
        help_text='Horsepower'
    )
    drivetrain = models.CharField(
        max_length=3,
        choices=DrivetrainChoices.choices
    )
    private = models.BooleanField(
        default=False
    )
    created_at = models.DateField(
        auto_now_add=True,
    )

    @property
    def make_and_model(self):
        return f'{self.title} {self.model}'

class ProjectImages(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = CloudinaryField('project_image')
    created_at = models.DateTimeField(
        auto_now_add=True,
    )



