# Generated by Django 4.2.16 on 2024-12-08 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_delete_follower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='gender',
        ),
    ]