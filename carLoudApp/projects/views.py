from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from rest_framework.status import HTTP_403_FORBIDDEN


from carLoudApp.projects.forms import ProjectForm, ProjectImagesForm
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
    form_class = ProjectForm
    template_name = 'projects/project-create.html'
    login_url = reverse_lazy('user-login')

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = self.request.user
        project.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user-garage', kwargs={'pk': self.request.user.pk})

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    login_url = 'user-login'

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

def project_delete(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        if request.user == project.user:
            project.delete()
            return redirect(reverse_lazy('user-garage', kwargs={'pk': request.user.pk}))
        return HttpResponse(HTTP_403_FORBIDDEN, 'You do not have permission to delete this project.')

    return render(request, 'projects/project-delete.html', {'object': project})

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project-edit.html'

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        if project.user != request.user:
            return HttpResponse(HTTP_403_FORBIDDEN, 'You do not have permission to edit this project.')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        project = form.save(commit=False)
        user = self.request.user

        if user != project.user:
            return HttpResponse(HTTP_403_FORBIDDEN)
        project.save()
        return redirect(reverse_lazy('project-details', kwargs={'pk': project.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ProjectForm(instance=self.get_object())
        context['form'] = form
        return context

class ProjectImageCreateView(LoginRequiredMixin, CreateView):
    model = ProjectImages
    form_class = ProjectImagesForm
    template_name = 'projects/project-images-create.html'

    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        user = self.request.user

        try:
            project = Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            raise Http404

        if project.user == user:
            image = form.save(commit=False)
            image.project = project
            image.user = user
            image.save()
            return redirect('project-details', pk=project.pk)
        return HttpResponse(HTTP_403_FORBIDDEN)


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