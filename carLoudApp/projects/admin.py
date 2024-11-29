from django.contrib import admin

from carLoudApp.projects.models import Project, ProjectImages


class ProjectImageInline(admin.StackedInline):
    model = ProjectImages
    can_delete = False
    verbose_name_plural = 'Project Images'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]