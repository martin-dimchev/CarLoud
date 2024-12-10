from django.contrib import admin

from carLoudApp.interactions.models import Comment, Like, Follower


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'post',
        'created_at',
    )
    search_fields = (
        'user__username',
        'post__project__title',
        'text',
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'post',
    )


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = (
        'follower',
        'is_following',
    )
