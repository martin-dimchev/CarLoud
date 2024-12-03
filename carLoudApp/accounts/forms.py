from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm
UserModel = get_user_model()


class UserRegisterForm(BaseUserCreationForm):
    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'example@email.com'
        })
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'JohnDoe'
        })

    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
        })
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'widget': forms.PasswordInput(attrs={
                'class': 'form-control auth-input',
            })
        })
    )

    class Meta:
        model = UserModel
        fields = ['email','username', 'password1', 'password2']


class UserLoginForm(forms.Form):
    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'example@email.com'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
        })
    )
    class Meta:
        model = UserModel
        fields = ['email', 'password']



class UserChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        exclude = ['profile_image']


class ResendEmailForm(forms.Form):
    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'example@email.com'
        })
    )

