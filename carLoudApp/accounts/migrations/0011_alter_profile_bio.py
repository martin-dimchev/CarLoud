# Generated by Django 4.2.16 on 2024-12-03 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
