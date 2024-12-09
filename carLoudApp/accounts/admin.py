from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.html import format_html
from .models import Profile


UserModel = get_user_model()

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('image', 'age', 'bio')


@admin.register(UserModel)
class UserAdmin(DefaultUserAdmin):
    model = UserModel
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')
    list_display = ('email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'last_login')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = [ProfileInline]

    def get_inline_instances(self, request, obj=None):
        """Show inlines only when editing a specific user."""
        if obj:
            return super().get_inline_instances(request, obj)
        return []


