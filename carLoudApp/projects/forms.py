import os
from django import forms
from django.core.exceptions import ValidationError

from carLoudApp.projects.models import Project, ProjectPost


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'title', 'brand', 'model', 'year', 'description',
            'horsepower', 'drivetrain', 'private'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control auth-input'}),
            'brand': forms.TextInput(attrs={'class': 'form-control auth-input'}),
            'model': forms.TextInput(attrs={'class': 'form-control auth-input'}),
            'year': forms.NumberInput(attrs={'class': 'form-control auth-input'}),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control auth-input'
            }),
            'horsepower': forms.NumberInput(attrs={
                'class': 'form-control auth-input'},

            ),
            'drivetrain': forms.Select(attrs={'class': 'form-control auth-input'}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProjectPostsForm(forms.ModelForm):

    class Meta:
        model = ProjectPost
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control auth-input'}),
            'caption': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'image': 'Photo',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        print(os.path.splitext(image.name)[1].lower())

        if image:
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError("Only JPG and PNG files are allowed.")

        return image