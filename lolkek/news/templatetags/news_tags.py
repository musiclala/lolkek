from django import template
from lolkek.news.models import Category


register = template.Library()


@register.inclusion_tag('news/tags/list_categories.html')
def show_categories():
    categories = Category.objects.all()
    return {'categories': categories, }
