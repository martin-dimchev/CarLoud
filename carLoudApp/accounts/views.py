import os
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import DetailView, CreateView, UpdateView

from carLoudApp import settings
from carLoudApp.accounts.forms import UserRegisterForm, UserLoginForm, ResendEmailForm, UserProfileEditForm
from carLoudApp.accounts.utils import generate_token, send_email
from carLoudApp.projects.models import Project, ProjectPost
from carLoudApp.accounts.tasks import upload_to_cloudinary

UserModel = get_user_model()


def activate_user(request, uidb64, token):
    try:
        decoded_uid = urlsafe_base64_decode(uidb64)
        uid = force_str(decoded_uid)
        user = UserModel.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user is not None:
        if user.is_verified:
            context = {
                'message': 'Your email is already verified. Please login.',
                'form': UserLoginForm(),
            }

            return render(request, 'accounts/account-login.html', context)

    if user and generate_token.check_token(user, token):
        user.is_verified = True
        user.save()

        context = {
            'form': UserLoginForm(),
            'message': 'Email verified successfully.',
        }

        return render(request, 'accounts/account-login.html', context)

    return render(request, 'accounts/verification-failed.html')


def resend_verification_email(request):
    form = ResendEmailForm(request.POST or None)
    message = ''

    if form.is_valid():
        email = request.POST.get('email')

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            message = 'No account found with this email.'
            user = None

        if user:
            if user.is_verified:
                context = {
                    'form': UserLoginForm(),
                    'message': 'Your email is already verified. Please login.'
                }

                return render(request, 'accounts/account-login.html', context)
            else:
                send_email(request, user)
                message = 'A new verification email has been sent. Please check your inbox.'

    context = {
        'form': form,
        'message': message,
    }

    return render(request, 'accounts/resend-email.html', context)


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/account-register.html'

    def form_valid(self, form):
        user = form.save()
        send_email(self.request, user)

        context = {
            'form': UserLoginForm(),
            'message': 'Verification email sent.'
        }

        return render(self.request, 'accounts/account-login.html', context)


def user_login(request):
    form = UserLoginForm(request.POST or None)
    message = ''

    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_verified:
                login(request, user)

                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))

                return redirect('index')
            else:
                message = 'Your email is not verified.'
        else:
            message = 'Invalid email or password.'

    context = {
        'form': form,
        'message': message,
    }

    return render(request, 'accounts/account-login.html', context)


class UserDetailsView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/account-details.html'
    login_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        followers_pks = user.followers.values_list('follower', flat=True)
        context['followers_pks'] = followers_pks

        images_count = ProjectPost.objects.filter(project__user=user).count()
        context['posts_count'] = images_count

        if self.request.user == user:
            context['projects'] = Project.objects.filter(user=user)
            context['posts'] = ProjectPost.objects.filter(project__user=user)
        else:
            context['projects'] = Project.objects.filter(user=user, private=False)
            context['posts'] = ProjectPost.objects.filter(project__user=user, project__private=False)

        return context


class UserEditView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = UserProfileEditForm
    template_name = 'accounts/account-edit.html'

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        if self.request.user != user:
            return HttpResponseForbidden('You do not have permission to edit this account.')

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('user-details', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        form_user = form.save(commit=False)
        user = self.get_object()

        if self.request.user != user:
            return HttpResponseForbidden('You do not have permission to edit this account.')

        if self.request.FILES:
            uploaded_file = self.request.FILES['profile_image']
            temp_dir = settings.TEMP_FILES
            os.makedirs(temp_dir, exist_ok=True)
            temp_file_path = str(temp_dir / uploaded_file.name)

            with default_storage.open(temp_file_path, 'wb+') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            upload_to_cloudinary.delay(temp_file_path, form_user.profile.pk)
            form_user.profile.image = None

        form_user.save()

        return super().form_valid(form)
