import six
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from carLoudApp.accounts.tasks import send_email_task


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_verified)


generate_token = TokenGenerator()


def send_email(request, user):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('accounts/account-verify.html', {
        'user': user,
        'activation_url': f'http://{current_site.domain}/accounts/account/{urlsafe_base64_encode(force_bytes(user.pk))}/{generate_token.make_token(user)}/'
    })

    send_email_task.delay(email_subject, email_body, user.email)
