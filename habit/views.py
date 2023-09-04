from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.pagintors import HabitPaginator
from habit.permissions import IsOwner, IsPublic
from habit.serializers import HabitSerializer


# Create your views here.
class HabitCreateAPIView(generics.CreateAPIView):
    # Контроллер для создания привычек
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # сохранение пользователя в привычку
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    '''Контролер для получения списка привычек
    с ограничением на аутентификацию и публичность привычки'''
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [IsPublic | IsAuthenticated]


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    '''Контролер для просмотра привычки
    с ограничением на аутентификацию и публичность привычки'''
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsPublic | IsAuthenticated]


class HabitUpdateAPIView(generics.UpdateAPIView):
    '''Контролер для обновления привычки
    с ограничением на создателя привычки'''
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    '''Контролер для удаления привычки
    с ограничением на создателя привычки'''
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]
