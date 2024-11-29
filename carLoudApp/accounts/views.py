from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView
from rest_framework.status import HTTP_403_FORBIDDEN

from carLoudApp.accounts.forms import UserRegisterForm
from carLoudApp.accounts.models import Follower
from carLoudApp.projects.models import Project, ProjectImages

UserModel = get_user_model()

class UserDetailsView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/account-details.html'
    login_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        followers_pks = user.followers.values_list('follower', flat=True)
        context['followers_pks'] = followers_pks

        images_count = ProjectImages.objects.filter(project__user=user).count()
        context['images_count'] = images_count

        if self.request.user == user:
            context['projects'] = Project.objects.filter(user=user)
            context['images'] = ProjectImages.objects.filter(project__user=user)
        else:
            context['projects'] = Project.objects.filter(user=user, private=False)
            context['images'] = ProjectImages.objects.filter(project__user=user, project__private=False)

        return context

class UserRegisterView(CreateView):
    model = UserModel
    form_class = UserRegisterForm
    template_name = 'accounts/account-register.html'
    success_url = reverse_lazy('user-login')


class UserLoginView(LoginView):
    model = UserModel
    form_class = AuthenticationForm
    template_name = 'accounts/account-login.html'
    success_url = reverse_lazy('index')


class FollowToggleView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        follower = request.user
        is_following = UserModel.objects.get(pk=kwargs.get('pk'))

        if follower == is_following:
            return HTTP_403_FORBIDDEN(message='You cannot follow yourself!')

        if Follower.objects.filter(follower=follower, is_following=is_following).exists():
            Follower.objects.get(follower=follower, is_following=is_following).delete()
            return redirect(reverse_lazy('user-details', kwargs={'pk': is_following.pk}))

        Follower.objects.create(follower=follower, is_following=is_following).save()
        return redirect(reverse_lazy('user-details', kwargs={'pk': is_following.pk}))
