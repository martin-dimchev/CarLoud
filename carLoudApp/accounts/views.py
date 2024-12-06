from time import sleep

from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import DetailView, CreateView

from carLoudApp.accounts.forms import UserRegisterForm, UserLoginForm, ResendEmailForm
from carLoudApp.accounts.utils import generate_token
from carLoudApp.projects.models import Project, ProjectPosts
from django.conf import settings

UserModel = get_user_model()

from .tasks import send_email_task
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def send_email(request, user):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('accounts/account-verify.html', {
        'user': user,
        'activation_url': f"http://{current_site.domain}/accounts/account/{urlsafe_base64_encode(force_bytes(user.pk))}/{generate_token.make_token(user)}/"
    })
    send_email_task.delay(email_subject, email_body, user.email)

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
                'message': 'Already verified. Please login.',
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
                return render(request, 'accounts/account-login.html', {
                    'form': UserLoginForm(),
                    'message': 'Your email is already verified. Please login.'
                })
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
        return render(self.request, 'accounts/account-login.html', {
            'form': UserLoginForm(),
            'message': 'Verification email sent.'
        })


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
                print(request.get_full_path_info())
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

        images_count = ProjectPosts.objects.filter(project__user=user).count()
        context['posts_count'] = images_count

        if self.request.user == user:
            context['projects'] = Project.objects.filter(user=user)
            context['posts'] = ProjectPosts.objects.filter(project__user=user)
        else:
            context['projects'] = Project.objects.filter(user=user, private=False)
            context['posts'] = ProjectPosts.objects.filter(project__user=user, project__private=False)

        return context
