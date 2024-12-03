from django import template

register = template.Library()

@register.simple_tag
def alert_class(message):
    success_messages = [
        'Your email is already verified. Please login.',
        'Email verified successfully.',
        'Verification email sent.',
        'A new verification email has been sent. Please check your inbox.',
    ]
    danger_messages = [
        'Your email is not verified.',
        'Invalid email or password.',
        'No account found with this email.',
    ]

    if message in success_messages:
        return 'success'
    elif message in danger_messages:
        return 'danger'

    return ''