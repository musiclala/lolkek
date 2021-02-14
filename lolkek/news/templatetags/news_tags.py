from django import template
from django.db.models import Count

from lolkek.news.models import Category


register = template.Library()


@register.inclusion_tag('news/tags/list_categories.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    return {'categories': categories, }
