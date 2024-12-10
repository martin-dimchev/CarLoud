from django import template
from django.db import ProgrammingError

from carLoudApp.interactions.models import Like
from carLoudApp.projects.models import  ProjectPost

register = template.Library()

@register.simple_tag
def is_liked(user, post_pk):
    if post_pk:
        user_liked_images_pks = Like.objects.filter(user=user).values_list('post', flat=True)
        if post_pk in user_liked_images_pks:
            return 'liked'
    return ''
