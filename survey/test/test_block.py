from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User
from survey.models import Survey, Block
from survey.serializers import BlockSerializer


class BlockViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(name='Test Survey', created_by=self.user)
        self.block = Block.objects.create(name='Test Block', survey=self.survey)
        self.client.force_authenticate(user=self.user)

    def test_list_blocks(self):
        url = reverse('block-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        serialized_data = BlockSerializer(instance=self.block).data
        self.assertEqual(response.data, [serialized_data])

    def test_retrieve_block(self):
        url = reverse('block-detail', args=[self.block.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = BlockSerializer(instance=self.block).data
        self.assertEqual(response.data, serialized_data)

    def test_create_block(self):
        url = reverse('block-list')
        data = {
            'name': 'New Block',
            'survey_id': self.survey.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        block = Block.objects.get(id=response.data['data']['id'])
        self.assertEqual(block.name, data['name'])
        self.assertEqual(block.survey.id, data['survey_id'])

    def test_update_block(self):
        url = reverse('block-detail', args=[self.block.id])
        data = {
            'name': 'Updated Block',
            'survey': self.survey.id
        }
        response = self.client.put(url, data=data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        block = Block.objects.get(id=response.data['data']['id'])
        self.assertEqual(block.name, data['name'])
        self.assertEqual(block.survey.id, data['survey_id'])

    def test_partial_update_block(self):
        url = reverse('block-detail', args=[self.block.id])
        data = {
            'name': 'Updated Block',
            'survey_id': self.survey.id

        }
        response = self.client.patch(url, data=data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        block = Block.objects.get(id=response.data['data']['id'])
        self.assertEqual(block.name, data['name'])
        self.assertEqual(block.survey.id, data['survey_id'])

    def test_delete_block(self):
        url = reverse('block-detail', args=[self.block.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Block.objects.filter(id=self.block.id).exists())
