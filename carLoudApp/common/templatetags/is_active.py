from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active(context,starts_with):
    request = context.get('request')
    if request.path.startswith(starts_with):
        if starts_with  == '/accounts/' and request.path.endswith('/details/'):
            if request.user!=context['object']:
                return ''
        return 'active'
    return ''