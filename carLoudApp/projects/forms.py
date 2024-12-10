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
    post_image = forms.FileField(required=False)
    caption = forms.CharField(required=False, widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control auth-input'


    def clean_post_image(self):
        post_image = self.cleaned_data.get('post_image')

        if post_image:
            ext = os.path.splitext(post_image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError('Only JPG and PNG files are allowed.')

        return post_image

    class Meta:
        model = ProjectPost
        fields = ['post_image', 'caption']
        labels = {
            'post_image': 'Photo',
        }
