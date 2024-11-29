from django import template
from django.db import ProgrammingError

from carLoudApp.interactions.models import Like
from carLoudApp.projects.models import  ProjectImages

register = template.Library()

@register.simple_tag
def is_liked(user, image_pk):
    if image_pk:
        user_liked_images_pks = Like.objects.filter(user=user).values_list('image', flat=True)
        if image_pk in user_liked_images_pks:
            return 'liked'
    return ''
