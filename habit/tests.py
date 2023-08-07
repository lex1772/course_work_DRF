from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from habit.models import Habit
from user.models import User


class HabitTestCase(APITestCase):
    # Тесты для привычек
    def setUp(self) -> None:
        # Создание привычки и пользователя для тестирования, авторизация пользователя через токен
        self.user = User.objects.create(
            email='test@test.test', password='12345', is_superuser=True, is_staff=True)
        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.habit = Habit.objects.create(
            place="дома",
            action="анжумания",
            user=self.user
        )

    def test_get_list(self):
        # Получение списка привычек и сравнение с действием первой привычки
        response = self.client.get(
            reverse('habit:habit_list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'][0]['action'], 'анжумания')

    def test_habit_create(self):
        # Создание привычки и сравнение с количеством привычек
        data = {
            "place": "улица",
            "action": "бегит"
        }
        response = self.client.post(reverse('habit:habit_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        # Обновление привычки и сравнение с обновленным действием привычки
        response = self.client.patch(reverse('habit:habit_update', kwargs={'pk': self.habit.pk}),
                                     data={'action': 'пресс качат'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['action'], 'пресс качат')

    def test_habit_delete(self):
        # Удаление привычки
        data = {
            "place": "улица",
            "action": "турник"
        }
        res = self.client.post(reverse('habit:habit_create'), data=data)
        response = self.client.delete(reverse('habit:habit_delete', kwargs={'pk': res.json()['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_habit_detail(self):
        # Просмотр привычки
        response = self.client.get(
            reverse('habit:habit', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_create_validtion_error(self):
        # Тестирование валидации приятной привычки
        data = {
            "place": "улица",
            "action": "сидеть",
            "good_habit_sign": "True",
            "reward": "Покурить"
        }
        response = self.client.post(reverse('habit:habit_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки.']})
        data = {
            "place": "улица",
            "action": "сидеть",
            "good_habit_sign": "True",
            "related_habit": self.habit.pk
        }
        response = self.client.post(reverse('habit:habit_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки.']})

        data = {
            "place": "дома",
            "action": "играть",
            "reward": "попить энергетика"
        }
        response = self.client.post(reverse('habit:habit_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "place": "дома",
            "action": "играть",
            "related_habit": self.habit.pk
        }
        response = self.client.post(reverse('habit:habit_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
