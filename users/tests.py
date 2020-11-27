from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class UserTests(APITestCase):
    user_data = {
        'username': 'Test',
        'first_name': 'some_name',
        'last_name': 'surname',
        'password': 'Qwerty123',
        'is_active': True,
    }
    test_data_user = {
        'username': 'Test1',
        'first_name': 'some_name',
        'last_name': 'surname',
        'password': 'Qwerty123',
        'is_active': True,
    }

    def setUp(self):
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.get(user=self.user)

        self.api_authenticate()

    def api_authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_create_user(self):
        self.client.force_authenticate(user=None)
        url = reverse('users_list_create')

        response = self.client.post(url, self.test_data_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.test_data_user['username'], response.data['username'])
        self.assertEqual(self.test_data_user['first_name'], response.data['first_name'])
        self.assertEqual(self.test_data_user['last_name'], response.data['last_name'])
        self.assertEqual(self.test_data_user['is_active'], response.data['is_active'])

        Token.objects.get(user_id=2)

    def test_token_obtain(self):
        url = reverse('obtain_token')
        response = self.client.post(url, {'username': self.user_data['username'],
                                          'password': self.user_data['password']},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token.key)

    def test_users_list(self):
        expected_data = {
            'id': 1,
            'username': 'Test',
            'first_name': 'some_name',
            'last_name': 'surname',
            'is_active': True,
            'last_login': None,
            'is_superuser': False
        }
        url = reverse('users_list_create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for data in response.data:
            self.assertEqual(dict(data), expected_data)

    def test_user_detail_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('user_detail', kwargs={'pk': 1})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(url, self.test_data_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(url, self.test_data_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_authorized(self):
        url = reverse('user_detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(url, self.test_data_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=1)
        self.assertEqual(user.username, self.test_data_user['username'])

        response = self.client.patch(url,
                                     {'username': 'Test2', 'password': 'Ytrewq321'},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'Test2')
        self.assertTrue(user.check_password('Ytrewq321'))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user = User.objects.filter(id=1)
        self.assertFalse(user)