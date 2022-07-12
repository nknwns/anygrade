from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Template(models.Model):
    title = models.CharField(max_length=127, verbose_name='Название')
    description = models.CharField(max_length=255, verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    question = models.ManyToManyField('Question', verbose_name='Вопросы')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('template', kwargs={'template_id': self.pk})

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['created_at', 'title']


class Question(models.Model):
    title = models.CharField(max_length=1023, verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.pk})

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['created_at']


class Category(models.Model):
    title = models.CharField(max_length=127, verbose_name='Название')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Review(models.Model):
    title = models.CharField(max_length=127, verbose_name='Название')
    description = models.CharField(max_length=255, verbose_name='Описание')
    start_time = models.DateTimeField(verbose_name='Время начала', null=True)
    end_time = models.DateTimeField(verbose_name='Время конца', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    question = models.ManyToManyField('Question', verbose_name='Вопросы')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор', related_name='author_review')
    subject = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Опрашиваемый', related_name='subject_review')
    participant = models.ManyToManyField(User, verbose_name='Участники', related_name='participant_review')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('review', kwargs={'review_id': self.pk})

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'


class Result(models.Model):
    data = models.CharField(max_length=255, verbose_name='Тело ответа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор', related_name='author_result')
    subject = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, verbose_name='Опрос', related_name='subject_result')

    def __str__(self):
        return f'{self.author} | {self.subject}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'