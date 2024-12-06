from cloudinary.models import CloudinaryField
from django.contrib.auth.models import  AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from carLoudApp.accounts.choices import GenderChoices
from carLoudApp.accounts.validators import CapFirstValidator, IsAlphaValidator


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
    )
    first_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(1),
            CapFirstValidator('Your name must start with a capital letter'),
            IsAlphaValidator('Your name must contain only letters'),
        ]
    )
    last_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(1),
            CapFirstValidator('Your name must start with a capital letter'),
            IsAlphaValidator('Your name must contain only letters'),
        ]
    )
    is_verified = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    image = CloudinaryField(
        'profile_image',
        null=True,
        blank=True,
    )

    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=(
            GenderChoices.choices
        )
    )
    bio = models.TextField(
        max_length=255,
        null=True,
        blank=True,
    )
