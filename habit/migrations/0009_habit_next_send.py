# Generated by Django 4.2.3 on 2023-08-06 05:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0008_habit_tg_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='next_send',
            field=models.DateField(default=datetime.date.today, verbose_name='дата следующей отправки'),
        ),
    ]