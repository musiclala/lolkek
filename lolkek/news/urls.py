from django.views.decorators.cache import cache_page
from django.urls import path
from .views import *

urlpatterns = [
    path('', cache_page(60)(HomeNews.as_view()), name='home'),
    # path('', HomeNews.as_view(), name='home'),
    path('category/<int:pk>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('register/', Register.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('test/', SendEmailSupport.as_view(), name='contacts'),
]
