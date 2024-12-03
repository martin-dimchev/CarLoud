from django import forms

from carLoudApp.projects.models import Project, ProjectImages


from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'make', 'model', 'year', 'description',
            'horsepower', 'drivetrain', 'private'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control auth-input'}),
            'make': forms.TextInput(attrs={'class': 'form-control auth-input'}),
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


class ProjectImagesForm(forms.ModelForm):
    class Meta:
        model = ProjectImages
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control auth-input'}),
            'caption': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'image': 'Photo',
        }