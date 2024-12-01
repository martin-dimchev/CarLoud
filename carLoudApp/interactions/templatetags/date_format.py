from datetime import datetime,timedelta

from django import template

register = template.Library()

@register.simple_tag
def date_format(timestamp):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    if timestamp.date() == today:
        return timestamp.strftime("%H:%M")
    elif timestamp.date() == yesterday:
        return 'Yesterday'
    return timestamp.strftime("%d/%m/%y")
