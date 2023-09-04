from datetime import timedelta, datetime, date

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail

from config import settings
from habit.models import Habit
from user.models import User

# Делаем логгер для отображения информации в консоли
logger = get_task_logger(__name__)


@shared_task
def my_task():
    # Периодическая задача для отправки сообщений в телеграм бота или на почту о исполнении привычки
    habs = Habit.objects.all().values()
    apiToken = settings.TG_KEY
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    for hab in habs:
        message = f"Сделать {hab['action']} {hab['place']}"
        if hab['time'].hour >= datetime.now().hour and hab['next_send'] >= date.today():
            if requests.get(apiURL, data={'chat_id': hab['tg_chat_id'], 'text': message}) is not None:
                hab['next_send'] += timedelta(days=8 - hab['frequency'])
            else:
                if hab['user_id']:
                    user = User.objects.filter(pk=hab['user_id']).values()
                    user = user[0]
                    if send_mail(subject="Привычка", message=message, from_email=settings.DEFAULT_FROM_EMAIL,
                                 recipient_list=[user['email']]) == 1:
                        hab['next_send'] += timedelta(days=hab['frequency'])
