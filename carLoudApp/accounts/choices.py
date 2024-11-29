from django.db import models


class GenderChoices(models.TextChoices):
    MALE = 'M', 'M'
    FEMALE = 'F', 'F'