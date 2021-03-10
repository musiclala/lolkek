from django.db.models import Count, F
from django.views.generic.base import ContextMixin

from .models import *


class MixinForCategory(ContextMixin):

    mixin_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
        context['show_categories'] = categories
        context['title'] = self.mixin_title

        return context



