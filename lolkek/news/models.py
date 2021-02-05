from django.db import models
from django.urls import reverse_lazy


class News(models.Model):

    title = models.CharField(verbose_name='Наименование', max_length=50)
    content = models.TextField(verbose_name='Контент', blank=True)
    created_at = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    photo = models.ImageField(verbose_name='Фото', upload_to='photos/%Y/%m/%d/', blank=True, )
    is_published = models.BooleanField(verbose_name='Опубликовано?', default=True)
    category = models.ForeignKey('Category', verbose_name='Категория',
                                 on_delete=models.PROTECT, null=True)

    def get_absolute_url(self):
        return reverse_lazy('view_news', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Category(models.Model):

    title = models.CharField(verbose_name='Наименование', max_length=50, db_index=True)

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
