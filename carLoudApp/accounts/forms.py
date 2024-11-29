from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class UserRegisterForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        exclude = ['profile_image']