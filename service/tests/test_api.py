from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..serializers import QuestionsSerializer
from ..models import Question, Category


class APITestCase(APITestCase):
    def test_get(self):
        Category.objects.create(title='First category')
        question_1 = Question.objects.create(title='First question', category_id=1)
        question_2 = Question.objects.create(title='Second question', category_id=1)

        url = reverse('questions-list')
        response = self.client.get(url)

        serialized_data = QuestionsSerializer([question_1, question_2], many=True).data

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(serialized_data, response.data)
