import logging
from datetime import datetime, timedelta

from celery import shared_task
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from config import settings
from habit.models import Habit
from tg_funcs import send_to_telegram
from user.models import User
from celery import Celery

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@shared_task(name='my_task')
def my_task():
    habs = Habit.objects.all().values()
    for hab in habs:
        days = ", ".join([str(i) for i in range(1, hab['frequency'] + 1)])
        logger.info(days)
        schedule = CrontabSchedule.objects.create(day_of_week=days, minute=hab['time'].minute, hour=hab['time'].hour)
        task = PeriodicTask.objects.create(name='adder',
                                           task='apps.task.add', crontab=schedule,
                                           start_time=datetime.utcnow() + timedelta(seconds=300))
        logger.info("task added")
        task.save()
        print(task)
        message = f"Сделать {hab['action']} {hab['place']}"
        if hab['time'].hour > datetime.now().hour:
            if hab['tg_chat_id']:
                send_to_telegram(hab['tg_chat_id'], message)
            else:
                user = User.objects.get(pk=hab['user_id'])
                user.email_user(subject="Привычка", message=message, from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[user.email])
