# Generated by Django 5.1.3 on 2024-11-29 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_projectimages_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='brand',
            new_name='make',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='name',
            new_name='title',
        ),
    ]
