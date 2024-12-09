from django.contrib import admin

from carLoudApp.interactions.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass