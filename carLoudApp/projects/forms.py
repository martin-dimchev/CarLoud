from django import forms

from carLoudApp.projects.models import Project


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['user']