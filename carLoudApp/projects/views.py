import os
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from rest_framework.status import HTTP_403_FORBIDDEN

from carLoudApp import settings
from carLoudApp.projects.forms import ProjectForm, ProjectImagesForm
from carLoudApp.projects.models import Project, ProjectPosts
from carLoudApp.projects.tasks import upload_to_cloudinary, upload_to_cloudinary

UserModel = get_user_model()


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


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    login_url = 'user-login'

    def get(self, request, *args, **kwargs):
        project = self.get_object()

        if (self.request.user != project.user) and project.private:
            return HttpResponse(HTTP_403_FORBIDDEN, 'You are not allowed to view this project')
        return super().get(request, *args, **kwargs)


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
        form = self.form_class(instance=self.get_object())
        context['form'] = form
        return context


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.user != request.user:
        return HttpResponse(HTTP_403_FORBIDDEN, 'You do not have permission to delete this project.')

    if request.method == 'POST':
        project.delete()
        return redirect(reverse_lazy('user-garage', kwargs={'pk': request.user.pk}))

    context = {
        'object': project,
        'text': 'this project',
    }
    return render(request, 'projects/confirm-delete.html', context)


class ProjectPostCreateView(LoginRequiredMixin, CreateView):
    model = ProjectPosts
    form_class = ProjectImagesForm
    template_name = 'projects/project-post-create.html'

    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        user = self.request.user
        project = get_object_or_404(Project, pk=project_pk)

        if project.user != user:
            return HttpResponse(HTTP_403_FORBIDDEN, 'You do not have permission to add post to this project.')

        uploaded_file = self.request.FILES['image']
        temp_file_path = str(settings.TEMP_FILES / uploaded_file.name)

        with default_storage.open(temp_file_path, 'wb') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        post = form.save(commit=False)
        post.project = project
        post.image = None
        post.save()

        upload_to_cloudinary.delay(temp_file_path, post.pk)

        return redirect(reverse_lazy('project-details', kwargs={'pk': project.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        context['object'] = project
        return context


class ProjectPostDetailView(LoginRequiredMixin, DetailView):
    model = ProjectPosts
    template_name = 'projects/project-post-details.html'
    pk_url_kwarg = 'post_pk'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(ProjectPosts, pk=self.kwargs.get('post_pk'))
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))

        if post not in project.posts.all():
            raise Http404

        if (self.request.user != post.project.user) and post.project.private:
            return HttpResponse(HTTP_403_FORBIDDEN, 'You do not have permission to view this image')

        return super().get(request, *args, **kwargs)



class ProjectPostEditView(LoginRequiredMixin, UpdateView):
    model = ProjectPosts
    form_class = ProjectImagesForm
    template_name = 'projects/project-post-edit.html'
    pk_url_kwarg = 'post_pk'

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))

        if post not in project.posts.all():
            raise Http404

        if post.project.user != request.user:
            return HttpResponse(HTTP_403_FORBIDDEN, 'You do not have permission to edit this post')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(instance=self.get_object())
        context['form'] = form
        return context

    def form_valid(self, form):
        post = get_object_or_404(ProjectPosts, pk=self.kwargs.get('post_pk'))

        if post.project.user == self.request.user:
            if self.request.FILES:
                uploaded_file = self.request.FILES['image']
                temp_file_path = str(settings.TEMP_FILES / uploaded_file.name)

                with default_storage.open(temp_file_path, 'wb') as temp_file:
                    for chunk in uploaded_file.chunks():
                        temp_file.write(chunk)

                upload_to_cloudinary(temp_file_path, post.pk)
            else:
                form.save()
            return redirect(reverse_lazy('project-post-details', kwargs={'pk': post.project.pk, 'post_pk': post.pk}))
        return HttpResponse(HTTP_403_FORBIDDEN)


def project_post_delete(request, pk, post_pk):
    post = get_object_or_404(ProjectPosts, pk=post_pk)
    project = get_object_or_404(Project, pk=pk)

    if post not in project.posts.all():
        raise Http404
    elif project.user != request.user:
        return HttpResponse(HTTP_403_FORBIDDEN, 'You do not have permission to delete this project.')

    if request.method == 'POST':
        post.delete()
        return redirect(reverse_lazy('project-details', kwargs={'pk': pk}))

    context = {
        'object': post,
        'text': 'this post',
    }

    return render(request, 'projects/confirm-delete.html', context)
