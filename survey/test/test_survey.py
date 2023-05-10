from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User
from survey.models import Survey
from survey.serializers import SurveySerializer


class SurveyViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('form-list')
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password'
        )
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            'name': 'Test Survey',
            'description': 'This is survey',
            'created_by': self.user.id,
            'is_published': False,
        }
        self.invalid_payload = {
            'name': '',
            'description': 'This is a test survey.',
            'created_by': self.user.id,
            'is_published': False,
        }
        self.survey = Survey.objects.create(
            name='Survey1234',
            description='This is a test survey.',
            created_by=self.user,
            is_published=True,
        )

    def test_list_surveys(self):
        response = self.client.get(self.url)
        surveys = Survey.objects.filter(created_by=self.user).order_by('-id')
        serializer = SurveySerializer(surveys, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_valid_survey(self):
        response = self.client.post(self.url, self.valid_payload)
        print(response.content, '/////')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_survey(self):
        response = self.client.post(self.url, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_survey(self):
        url = reverse('form-detail', args=[self.survey.id])
        response = self.client.get(url)
        serializer = SurveySerializer(self.survey)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_valid_survey(self):
        url = reverse('form-detail', args=[self.survey.id])
        data = {
            'name': 'Updated Survey12',
            'description': 'This is an updated test survey.',
            'created_by': self.user.id,
            'is_published': False,
        }
        response = self.client.put(url, data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_invalid_survey(self):
        url = reverse('form-detail', args=[self.survey.id])
        data = {
            'name': '',
            'description': 'This is an updated test survey.',
            'created_by': self.user.id,
            'is_published': False,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_valid_survey(self):
        url = reverse('form-detail', args=[self.survey.id])
        data = {
            'name': 'Updated 1Test Survey',
            'description': 'This is an test survey.',

        }
        response = self.client.patch(url, data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_partial_update_invalid_survey(self):
        url = reverse('form-detail', args=[self.survey.id])
        data = {
            'name': '',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_survey(self):
        url = reverse('form-detail', args=[self.survey.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
