from django.contrib import admin
from django.contrib.auth import get_user_model

from carLoudApp.accounts.forms import UserProfileEditForm
from carLoudApp.accounts.models import Profile

UserModel = get_user_model()

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    change_form = UserProfileEditForm
    inlines = [ProfileInline, ]
