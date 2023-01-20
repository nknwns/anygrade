from django.db.models import Q
from django.http import HttpResponseNotFound
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .permissions import IsAdminOrAuthorUpdateAndDeleteOrCreatorCreateOrAuthenticatedRead
from .serializers import *


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = (IsAdminOrAuthorUpdateAndDeleteOrCreatorCreateOrAuthenticatedRead, )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['category', 'title']

    @action(methods=['get'], detail=False)
    def all(self, request):
        questions = Question.objects.all()
        question_serializer = QuestionsSerializer(questions, many=True)

        return Response(question_serializer.data)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'start_time', 'end_time']

    @action(methods=['get'], detail=False)
    def current(self, request):
        reviews = Review.objects.filter(Q(start_time__lte=datetime.now()) & Q(end_time__gt=datetime.now()))
        review_serializer = ReviewSerializer(reviews, many=True)

        return Response(review_serializer.data)

    @action(methods=['get'], detail=True)
    def results(self, request, pk=None):
        results = Result.objects.filter(subject_id=pk)
        review = Review.objects.get(pk=pk)

        final_result = {
            'status': False,
            'finish': results.count() == review.participant.count(),
            'results_count': results.count(),
            'questions_count': review.question.count(),
            'participant': []
        }

        if results.count():
            final_result['status'] = True
            size = len(results[0].data)

            sum_results = [0 for i in range(size)]
            for result in results:
                row = result.data
                final_result['participant'].append(result.author.id)
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

            final_result['categories'] = list(map(lambda id: Category.objects.get(pk=id).pk, parsed_categories))

            final_result['average'] = list(map(lambda value, count: value / (results.count() * count), parsed_results, count_questions))

        return Response(final_result)


class TemplatesViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplatesSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    @action(methods=['post'], detail=True)
    def use(self, request, pk=None):
        title = request.POST['title']
        author = request.POST['author']
        subject = request.POST['subject']

        if not len(title):
            raise serializers.ValidationError('Поле title обязательное для заполнения.')
        if not User.objects.filter(pk=author).exists():
            raise serializers.ValidationError('Пользователь с таким ID не существует.')
        if not User.objects.filter(pk=subject).exists():
            raise serializers.ValidationError('Пользователь с таким ID не существует.')

        review = Review.objects.create(
            author_id=author,
            title=title,
            subject_id=subject,
            template_id=pk
        )

        review.question.set(Template.objects.get(pk=pk).question.all())
        review_serializer = ReviewSerializer(review)

        return Response(review_serializer.data)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']

    @action(methods=['get', 'post'], detail=True)
    def questions(self, request, pk=None):
        if request.method == 'GET':
            questions = Question.objects.filter(category__id=pk)
            question_serializer = QuestionsSerializer(questions, many=True)

            return Response(question_serializer.data)

        title = request.POST['title']
        author = request.POST['author']

        if not len(title):
            raise serializers.ValidationError('Поле title обязательное для заполнения.')
        if not User.objects.filter(pk=author).exists():
            raise serializers.ValidationError('Пользователь с таким ID не существует.')

        question = Question.objects.create(title=title, author_id=author)
        question_serializer = QuestionsSerializer(question)

        return Response(question_serializer.data)

    @action(methods=['get'], detail=False)
    def all(self, request):
        categories = Category.objects.all()
        category_serializer = CategoriesSerializer(categories, many=True)

        return Response(category_serializer.data)


class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultsSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена.')
