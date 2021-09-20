from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.simple_tag
def is_signed_to_author(author, user):
    return user.subscriptions.filter(author=author).exists()


@register.simple_tag
def format_ending(count, nominative, genitive, plural):
    remainder = count % 100
    if remainder == 0 or remainder >= 5 or (10 <= count <= 19):
        return plural
    if remainder == 1:
        return nominative
    return genitive
