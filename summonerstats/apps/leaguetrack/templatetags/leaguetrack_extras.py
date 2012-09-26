from django import template

register = template.Library()

@register.filter(name='english_list')
def english_list(value):
    return ' and'.join(', '.join(value).rsplit(',', 1))

@register.filter(name='en_href_list', is_safe=True)
def english_href_list(value):
    return ' and'.join(', '.join(['<a href="%s">%s</a>' % (s.href(), s.name) for s in value]).rsplit(',', 1))
