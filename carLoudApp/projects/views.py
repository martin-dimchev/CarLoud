from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED, HTTP_404_NOT_FOUND

from carLoudApp.accounts.models import Follower
from carLoudApp.projects.forms import ProjectCreationForm
from carLoudApp.projects.models import Project, ProjectImages

UserModel = get_user_model()

class GarageListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/projects-garage.html'
    login_url = reverse_lazy('user-login')

    def get_queryset(self, **kwargs):
        try:
            user = UserModel.objects.get(pk=self.kwargs['pk'])
        except UserModel.DoesNotExist:
            raise Http404
        if self.request.user == user:
            projects = Project.objects.filter(user=user)
        else:
            projects = Project.objects.filter(user=user, private=False)
        return projects

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['projects_user'] = UserModel.objects.get(pk=self.kwargs['pk'])
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'projects/project-create.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('user-login')

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = self.request.user
        project.save()
        return super().form_valid(form)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project-details.html'

    def get_object(self, **kwargs):
        try:
            project =  Project.objects.get(pk=self.kwargs['pk'])
        except Project.DoesNotExist:
            raise Http404

        print(self.request.user)
        print(project.user)
        if (self.request.user != project.user) and project.private:
            raise Http404
        return project


class ProjectImageDetailView(LoginRequiredMixin, DetailView):
    model = ProjectImages
    template_name = 'projects/project-image-details.html'

    def get_object(self, queryset=None):
        try:
            image = ProjectImages.objects.get(pk=self.kwargs['image_pk'])
        except ProjectImages.DoesNotExist:
            raise Http404
        if (self.request.user != image.project.user) and image.project.private:
            raise Http404
        return image