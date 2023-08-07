from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from user.models import User


# Создаем класс для тестов пользователя
class UserTestCase(APITestCase):

    def setUp(self) -> None:
        '''Создаем обьекты для тестирования, получаем токен и авторизуем пользователя'''
        self.user = User.objects.create(
            email='test@test.test', password='12345', is_superuser=True, is_staff=True)
        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_list(self):
        '''Получаем список пользователей'''
        response = self.client.get(
            reverse('user:user_list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['email'], 'test@test.test')

    def test_user_create(self):
        '''Создаем пользователя и сравниваем с общим количеством пользователей'''
        data = {
            "email": "test@t.ru",
            "password": "a"
        }
        response = self.client.post(reverse('user:user_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_update(self):
        '''обновляем пользователя и проверяем обновленные данные'''
        response = self.client.patch(reverse('user:user_update', kwargs={'pk': self.user.pk}),
                                     data={"email": "test1@r.ru"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['email'], 'test1@r.ru')

    def test_user_detail(self):
        '''Получаем пользователя по id'''
        resoponse = self.client.get(
            reverse('user:user', kwargs={'pk': self.user.pk}))
        self.assertEqual(resoponse.status_code, status.HTTP_200_OK)

    def test_user_delete(self):
        '''Удаляем пользователя'''
        response = self.client.delete(reverse('user:user_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
