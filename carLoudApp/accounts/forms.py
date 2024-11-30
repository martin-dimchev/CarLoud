from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm

UserModel = get_user_model()


class UserRegisterForm(BaseUserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ['email', 'password']



class UserChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        exclude = ['profile_image']