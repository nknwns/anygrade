from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from service.seed import seed_users, seed_categories, seed_questions, seed_templates, seed_reviews, seed_results


class Command(BaseCommand):
    help = u'Заполнение базы данных случайными данными'

    def add_arguments(self, parser):
        parser.add_argument('users_count', type=int, help=u'Количество создаваемых пользователей')
        parser.add_argument('categories_count', type=int, help=u'Количество создаваемых категорий')
        parser.add_argument('questions_count', type=int, help=u'Количество создаваемых вопросов')
        parser.add_argument('templates_count', type=int, help=u'Количество создаваемых шаблонов')
        parser.add_argument('reviews_count', type=int, help=u'Количество создаваемых опросов')

    def handle(self, *args, **kwargs):
        users_count = kwargs['users_count']
        categories_count = kwargs['categories_count']
        questions_count = kwargs['questions_count']
        templates_count = kwargs['templates_count']
        reviews_count = kwargs['reviews_count']

        seed_users(users_count)
        self.stdout.write(u'Генерация %s пользователей прошла успешно!' % users_count)

        seed_categories(categories_count)
        self.stdout.write(u'Генерация %s категорий прошла успешно!' % categories_count)

        seed_questions(questions_count)
        self.stdout.write(u'Генерация %s вопросов прошла успешно!' % questions_count)

        seed_templates(templates_count)
        self.stdout.write(u'Генерация %s шаблонов прошла успешно!' % templates_count)

        seed_reviews(reviews_count)
        self.stdout.write(u'Генерация %s опросов прошла успешно!' % reviews_count)

        seed_results()
        self.stdout.write('Генерация ответов прошла успешно!')
