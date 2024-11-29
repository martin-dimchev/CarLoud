from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active(context,starts_with):
    request = context.get('request')
    if request.path.startswith(starts_with):
        return 'active'
    return ''