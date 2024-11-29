from cloudinary.models import CloudinaryField
from django.contrib.auth.models import  AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import FileField

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


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    image = CloudinaryField(
        'profile_image',
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



class Follower(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
    is_following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
    )

    class Meta:
        unique_together = ('follower', 'is_following')