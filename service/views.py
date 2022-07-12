from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *
from .models import *


class UserCreate(CreateView):
    form_class = RegisterUserForm
    template_name = 'anygrade/registration.html'
    success_url = reverse_lazy('authorization')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация нового пользователя'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserAuth(LoginView):
    form_class = AuthorizationUserForm
    template_name = 'anygrade/authorization.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('authorization')


def index(request):
    posts = User.objects.all()
    context = {
        'posts': posts,
        'title': 'Главная страница'
    }
    return render(request, 'anygrade/index.html', context=context)


def questions(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
        'title': 'Список вопросов'
    }
    return render(request, 'anygrade/questions/page.html', context=context)


def show_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
        'title': f'Редактирование вопроса | Вопрос #{question.pk}'
    }
    return render(request, 'anygrade/questions/edit.html', context=context)


def remove_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_question(request):
    if request.method == 'POST':
        pass
    else:
        context = {
            'title': 'Новый вопрос'
        }
        return render(request, 'anygrade/questions/add.html', context=context)


def templates(request):
    templates = Template.objects.all()

    context = {
        'templates': templates,
        'title': 'Шаблоны'
    }
    return render(request, 'anygrade/templates/page.html', context=context)


def show_template(request, template_id):
    template = get_object_or_404(Template, pk=template_id)

    context = {
        'template': template,
        'title': f'Шаблон #{template_id} | {template.title} '
    }
    return render(request, 'anygrade/templates/single.html', context=context)


def edit_template(request, template_id):
    if request.method == 'POST':
        pass
    else:
        template = get_object_or_404(Template, pk=template_id)

        context = {
            'template': template,
            'title': 'Редактирование шаблона'
        }
        return render(request, 'anygrade/templates/edit.html', context=context)


def add_template(request):
    if request.method == 'POST':
        pass
    else:
        context = {
            'title': 'Новый шаблон'
        }
        return render(request, 'anygrade/templates/add.html', context=context)


def copy_template(request, template_id):
    context = {
        'title': 'Новый шаблон'
    }
    return render(request, 'anygrade/index.html', context=context)


def remove_template(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    template.delete()
    return redirect('templates')


def show_user(request, user_slug):
    user = get_object_or_404(User, username=user_slug)
    context = {
        'user': user,
        'title': user.get_full_name()
    }
    return render(request, 'anygrade/staff/single.html', context=context)


def reviews(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews,
        'title': 'Отчеты'
    }
    return render(request, 'anygrade/reviews/page.html', context=context)


def show_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    results = Result.objects.filter(subject_id=review.pk)
    final_result = {
        'status': False
    }

    if (results.count()):
        final_result['status'] = True
        size = len(results[0].data)

        sum_results = [0 for i in range(size)]
        for result in results:
            row = result.data
            for i in range(len(row)):
                sum_results[i] += int(row[i])

        all_categories = []
        for question in review.question.all():
            all_categories.append(question.category_id)

        count_questions = []
        parsed_results = []
        parsed_categories = []
        for i in range(size):
            if all_categories[i] in parsed_categories:
                index = parsed_categories.index(all_categories[i])
                parsed_results[index] += sum_results[i]
                count_questions[index] += 1
            else:
                parsed_results.append(sum_results[i])
                parsed_categories.append(all_categories[i])
                count_questions.append(1)

        final_result['categories'] = '|'.join(list(map(lambda id: Category.objects.get(pk=id).title, parsed_categories)))

        final_result['data'] = '|'.join(list(map(lambda value, count: str(value / (results.count() * count)), parsed_results, count_questions)))

    print(final_result)

    context = {
        'review': review,
        'result': final_result,
        'title': f'Отчет #{review.pk}'
    }
    return render(request, 'anygrade/reviews/single.html', context=context)


def add_review(request):
    if request.method == 'POST':
        pass
    else:
        context = {
            'title': 'Новый опрос'
        }
        return render(request, 'anygrade/reviews/add.html', context=context)


def edit_review(request, review_id):
    if request.method == 'POST':
        pass
    else:
        review = get_object_or_404(Review, pk=review_id)

        context = {
            'review': review,
            'title': 'Редактировать опрос'
        }
        return render(request, 'anygrade/reviews/edit.html', context=context)


def remove_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    return redirect('reviews')


def do_review(request, review_id):
    if request.method == 'POST':
        pass
    else:
        review = get_object_or_404(Review, pk=review_id)

        context = {
            'review': review,
            'title': 'Выполнение опроса'
        }
        return render(request, 'anygrade/reviews/do.html', context=context)




def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'title': 'Категории'
    }
    return render(request, 'anygrade/categories/page.html', context=context)


def edit_category(request, category_id):
    if request.method == 'POST':
        pass
    else:
        category = get_object_or_404(Category, pk=category_id)

        context = {
            'category': category,
            'title': 'Редактирование категории'
        }
        return render(request, 'anygrade/categories/edit.html', context=context)


def remove_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return redirect('categories')


def add_category(request):
    if request.method == 'POST':
        pass
    else:
        context = {
            'title': 'Новая категория'
        }
        return render(request, 'anygrade/categories/add.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена.')