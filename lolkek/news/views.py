from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from .utils import MixinForCategory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm


# def test(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             mail = send_mail(form.cleaned_data['subject'],
#                              form.cleaned_data['content'],
#                              settings.EMAIL_HOST_USER,
#                              ['r.misa2017@gmail.com'],
#                              fail_silently=False)
#             if mail:
#                 messages.success(request, 'Форма отправлена!')
#                 return redirect('test')
#             else:
#                 messages.error(request, 'ОШибка')
#     else:
#         form = ContactForm()
#     return render(request, 'news/test.html', {'form': form})


class SendEmailSupport(MixinForCategory, FormView):
    form_class = ContactForm
    template_name = 'news/test.html'

    mixin_title = 'Написать нам'

    def form_valid(self, form):

        subject = 'Сообщение от {}, email: {}. На тему {}'.format(self.request.user.username,
                                                                  self.request.user.email,
                                                                  form.cleaned_data['subject'])
        mail = send_mail(subject,
                         form.cleaned_data['content'],
                         settings.EMAIL_HOST_USER,
                         ['r.misa2017@gmail.com'],
                         fail_silently=False,)

        if mail:
            messages.success(self.request, 'Форма отправлена!')
            return redirect('test')
        else:
            messages.error(self.request, 'Ошибка')


class Register(MixinForCategory, FormView):
    form_class = UserRegisterForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('home')

    mixin_title = 'Регистрация'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегистрированы!')
        return super().form_valid(form)


class UserLogin(MixinForCategory, FormView):
    form_class = UserLoginForm
    template_name = 'news/login.html'
    success_url = reverse_lazy('home')

    mixin_title = 'Авторизация'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class UserLogout(LogoutView):
    next_page = reverse_lazy('login')


class HomeNews(MixinForCategory, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 5

    mixin_title = 'Главная страница'

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MixinForCategory, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['pk'],
                                   is_published=True).select_related('category')


class ViewNews(MixinForCategory, DetailView):
    model = News
    template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'pk'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, MixinForCategory, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
    login_url = '/admin/'  # redirect on registration, if not auth

    mixin_title = 'Добавление новости'
