import os
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


UserModel = get_user_model()


class UserRegisterForm(BaseUserCreationForm):
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'example@email.com'
        })
    )

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'JohnDoe'
        })

    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
        })
    )

    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'widget': forms.PasswordInput(attrs={
                'class': 'form-control auth-input',
            })
        })
    )

    class Meta:
        model = UserModel
        fields = ['email', 'username', 'password1', 'password2']


class UserLoginForm(forms.Form):
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'example@email.com'
        })
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
        })
    )

    class Meta:
        model = UserModel
        fields = ['email', 'password']


class UserProfileEditForm(forms.ModelForm):
    profile_image = forms.FileField(required=False)
    age = forms.IntegerField(required=False, validators=[
        MinValueValidator(1, 'Your age cannot be negative or zero value.'),
    ])
    bio = forms.CharField(widget=forms.Textarea, required=False, )

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if user:
            self.fields['bio'].initial = user.profile.bio
            self.fields['age'].initial = user.profile.age

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control auth-input'

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')

        if profile_image:
            ext = os.path.splitext(profile_image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError('Only JPG and PNG files are allowed.')

        return profile_image

    def save(self, commit=True):
        user = super().save(commit)

        user.profile.bio = self.cleaned_data['bio']
        user.profile.age = self.cleaned_data['age']
        user.profile.save()

        return user

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'age', 'profile_image', 'bio']


class ResendEmailForm(forms.Form):
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'example@email.com'
        })
    )
