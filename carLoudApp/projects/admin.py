from django.contrib import admin
from carLoudApp.projects.models import Project, ProjectPost

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = ('title', 'user', 'brand', 'model', 'year', 'private', 'created_at')
    list_filter = ('private', 'brand', 'year', 'created_at')
    search_fields = ('title', 'brand', 'model', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Project Info', {
            'fields': ('title', 'user', 'brand', 'model', 'year', 'description', 'horsepower', 'drivetrain')
        }),
        ('Settings', {
            'fields': ('private', 'created_at'),
        }),
    )


@admin.register(ProjectPost)
class ProjectPostsAdmin(admin.ModelAdmin):
    pass