from django.views.generic import ListView, DetailView, CreateView

from .models import News, Category
from .forms import NewsForm


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['pk'],
                                   is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'pk'
    context_object_name = 'news_item'


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CreateNews, self).get_context_data(**kwargs)
        context['title'] = 'Добавление новости'
        return context
