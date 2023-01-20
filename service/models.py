from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User
from django.db import models
from django.urls import reverse
from django.utils.datetime_safe import datetime
from simple_history.models import HistoricalRecords


# Create your models here

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    history = HistoricalRecords(
        inherit=True,
        history_change_reason_field=models.TextField(null=True)
    )

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Template(BaseModel):
    title = models.CharField(max_length=128, verbose_name='Название')
    description = models.CharField(max_length=256, verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    question = models.ManyToManyField('Question', verbose_name='Вопросы')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('template', kwargs={'template_id': self.pk})

    @property
    def questions_count(self):
        return self.question.count()

    questions_count.fget.short_description = 'Количество вопросов'

    @property
    def review_count(self):
        return Review.objects.filter(template__pk=self.pk).count()

    review_count.fget.short_description = 'Действующие опросы'

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['created_at', 'title']


class Question(BaseModel):
    title = models.CharField(max_length=255, unique=True, verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.pk})

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['created_at']


class Category(BaseModel):
    title = models.CharField(max_length=128, verbose_name='Название')
    author = models.ForeignKey(User, verbose_name='Автор', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Review(BaseModel):
    title = models.CharField(max_length=128, verbose_name='Название')
    description = models.CharField(max_length=256, verbose_name='Описание')
    start_time = models.DateTimeField(verbose_name='Время начала', null=True)
    end_time = models.DateTimeField(verbose_name='Время конца', null=True)
    question = models.ManyToManyField('Question', verbose_name='Вопросы')
    template = models.ForeignKey('Template', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Изначальный шаблон')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор',
                               related_name='author_review')
    subject = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Опрашиваемый',
                                related_name='subject_review')
    participant = models.ManyToManyField(User, verbose_name='Участники', related_name='participant_review')

    @property
    def result_count(self):
        return Result.objects.filter(subject__pk=self.pk).count()

    result_count.fget.short_description = 'Количество ответов'

    @property
    def status(self):
        if self.end_time:
            return ['Закончен', 'Активен'][self.end_time.timestamp() > datetime.now().timestamp()]
        return 'Не определено'

    status.fget.short_description = 'Статус'

    @property
    def question_count(self):
        return self.question.count()

    question_count.fget.short_description = 'Количество вопросов'

    @property
    def participant_count(self):
        return self.participant.count()

    participant_count.fget.short_description = 'Количество опрашиваемых'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('review', kwargs={'review_id': self.pk})

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Result(BaseModel):
    data = models.CharField(max_length=256, verbose_name='Тело ответа')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор',
                               related_name='author_result')
    subject = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, verbose_name='Опрос',
                                related_name='subject_result')

    def __str__(self):
        return f'{self.author} | {self.subject}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
