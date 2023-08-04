from datetime import datetime, timedelta, time

from django.core.validators import MaxValueValidator
from django.db import models

from user.models import User, NULLABLE


# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', **NULLABLE)
    place = models.TextField(verbose_name='место')
    time = models.TimeField(default=time(14), verbose_name='время')
    action = models.CharField(max_length=255, verbose_name='действие')
    good_habit_sign = models.BooleanField(default=False, verbose_name='признак хорошей привычки')
    related_habit = models.ForeignKey('self', on_delete=models.DO_NOTHING, **NULLABLE)
    frequency = models.SmallIntegerField(default=1, validators=[
        MaxValueValidator(limit_value=7, message='Не может быть реже 1 раза в неделю')], verbose_name='Периодичность')
    reward = models.CharField(max_length=255, verbose_name='награда', **NULLABLE)
    time_to_complete = models.DurationField(default=timedelta(seconds=120), validators=[
        MaxValueValidator(timedelta(seconds=120), message='Не может быть больше 120 секунд')],
                                            verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
    tg_chat_id = models.TextField(verbose_name='id чата в телеграме', **NULLABLE)

    def __str__(self):
        return f'{self.place}, {self.action}, {self.time}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
