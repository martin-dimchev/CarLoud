from django.db import models


class DrivetrainChoices(models.TextChoices):
    FWD = 'FWD', 'FWD'
    RWD = 'RWD', 'RWD'
    AWD = 'AWD', 'AWD'