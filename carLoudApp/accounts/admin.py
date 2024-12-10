from django.contrib import admin
from django.contrib.auth import get_user_model

from carLoudApp.accounts.models import Profile

UserModel = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('image', 'age', 'bio')


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    model = UserModel
    inlines = [ProfileInline]

    list_display = (
        'username',
        'first_name',
        'last_name',
        'is_verified',
        'is_staff',
        'last_login',
    )

    list_filter = (
        'is_verified',
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    )

    search_fields = (
        'email',
        'first_name',
        'last_name',
    )

    readonly_fields = (
        'last_login',
        'date_joined',
    )

    ordering = (
        'email',
    )

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
                'first_name',
                'last_name',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_verified',
                'groups',
                'user_permissions',
            )
        }),
        ('Important Dates', {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields['is_verified'].help_text = ('Designates whether the user has verified email '
                                                     'and can login in the system.')

        return form
