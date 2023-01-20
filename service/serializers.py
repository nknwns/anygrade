from rest_framework import serializers

from service.models import *


class HasAuthor:
    def get_author(self, obj):
        if obj.author:
            return UserInListSerializer(obj.author).data
        return None


class HasSubject:
    def get_subject(self, obj):
        if obj.subject:
            return UserInListSerializer(obj.subject).data
        return None


class HasTemplate:
    def get_template(self, obj):
        if obj.template:
            return TemplateInListSerializer(obj.template).data
        return None


class HasParticipant:
    def get_participant(self, obj):
        if obj.participant:
            return UserInListSerializer(obj.participant.all(), many=True).data
        return None


class HasQuestion:
    def get_question(self, obj):
        if obj.question:
            return QuestionInListSerializer(obj.question.all(), many=True).data
        return None


class HasCategory:
    def get_category(self, obj):
        if obj.category:
            return CategoryInListSerializer(obj.category).data
        return None


class QuestionsSerializer(
    serializers.ModelSerializer,
    HasAuthor,
    HasCategory
):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"


class QuestionInListSerializer(serializers.Serializer, HasCategory):
    id = serializers.IntegerField()
    title = serializers.CharField()
    category = serializers.SerializerMethodField()


class ReviewSerializer(
    serializers.ModelSerializer,
    HasAuthor,
    HasSubject,
    HasTemplate,
    HasParticipant,
    HasQuestion
):
    subject = serializers.SerializerMethodField()
    template = serializers.SerializerMethodField()
    participant = serializers.SerializerMethodField()
    question = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = "__all__"


class ReviewInListSerializer(
    serializers.Serializer,
    HasSubject
):
    id = serializers.IntegerField()
    title = serializers.CharField()
    subject = serializers.SerializerMethodField()


class TemplatesSerializer(
    serializers.ModelSerializer,
    HasAuthor,
    HasQuestion
):
    author = serializers.SerializerMethodField()
    question = serializers.SerializerMethodField()

    class Meta:
        model = Template
        fields = "__all__"


class TemplateInListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    questions_count = serializers.ReadOnlyField()


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryInListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class ResultsSerializer(
    serializers.ModelSerializer,
    HasAuthor
):
    subject = serializers.SerializerMethodField()

    def get_subject(self, obj):
        if obj.subject:
            return ReviewInListSerializer(obj.subject).data
        return None

    def validate(self, data):
        if data.get('subject') is None:
            raise serializers.ValidationError('Поле subject - обязательное поле')

        question_count = data.get('subject').question.count()
        data_length = len(data.get('data'))

        if question_count != data_length:
            raise serializers.ValidationError(f'Требумая длина поля data - {question_count} символов')

        return data

    class Meta:
        model = Result
        fields = "__all__"
        extra_kwargs = {'subject': {'required': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_login', 'first_name', 'last_name', 'email', 'groups')


class UserInListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()
