from django.urls import path

from habit.apps import HabitConfig
from habit.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView

app_name = HabitConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('', HabitListAPIView.as_view(), name='habit_list'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_delete'),
]
