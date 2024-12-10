from django.contrib import admin
from carLoudApp.projects.models import Project, ProjectPost

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = ('title', 'user', 'brand', 'model', 'year', 'private', 'posts', 'created_at')
    list_filter = ('private', 'brand', 'year', 'created_at')
    search_fields = ('title', 'brand', 'model', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Project Info', {
            'fields': ('title', 'user', 'brand', 'model', 'year', 'drivetrain')
        }),
        ('Status', {
            'fields': ('private',)
        }),
        ('Additional Info', {
            'fields': ('description', 'horsepower', 'created_at'),
        }),
    )

    def posts(self, obj):
        return obj.posts.count()


@admin.register(ProjectPost)
class ProjectPostsAdmin(admin.ModelAdmin):
    list_display = ('user','project', 'caption', 'likes', 'comments', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('project__title','project__brand', 'project__model', 'caption', 'project__user__username')

    def user(self, obj):
        return obj.project.user

    def likes(self, obj):
        return obj.likes.count()

    def comments(self, obj):
        return obj.comments.count()
