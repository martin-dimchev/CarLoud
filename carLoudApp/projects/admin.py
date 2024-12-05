from django.contrib import admin

from carLoudApp.projects.models import Project, ProjectPosts


class ProjectImageInline(admin.StackedInline):
    model = ProjectPosts
    can_delete = False
    verbose_name_plural = 'Project Images'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]