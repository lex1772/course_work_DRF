import re
from datetime import datetime, timedelta

import requests
import telegram

from config import settings
from db import get_related_habit, save_data_to_database

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

# Файл с основными функциями бота

# Подключаем бота
bot = telegram.Bot(settings.TG_KEY)

# Подключаем логи в консоль
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Выводим все вопросы
PLACE, TIME, ACTION, GOOD_HABIT_SIGN, RELEATED_HABIT, FREQUENCY, REWARD, TIME_TO_COMPLETE, IS_PUBLIC = range(9)

# Переменные для работы с пользователем и привычками
habit_list = []
ghs = ''
rel_habits = get_related_habit()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    '''Старт бота с получением места выполнения'''
    await update.message.reply_text(
        "Привет! Я бот для создания полезных привычек и напоминания о них. Начнем выполнять полезные привычки вместе?"
        "Отправь /cancel для завершения разговора.\n\n"
        "Где ты собираешься выполнять привычку?")

    return PLACE


async def place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Добавление места выполнения в список и получение времени привычки"""
    user = update.message.from_user
    habit_list.append(update.message.chat_id)
    logger.info("place of %s: %s", user.first_name, update.message.text)
    habit_list.append(update.message.text)
    if update.message.text == "/cancel":
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Пока! Надеюсь ты передумаешь и заполнишь привычку", reply_markup=ReplyKeyboardRemove()
        )
        habit_list.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "В какое время ты собираешься выполнять привычку?")

        return TIME


async def time_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Добавление в список времени выполнения привычки и получение самой привычки"""
    user = update.message.from_user
    logger.info("time of %s: %s", user.first_name, update.message.text)
    message = re.sub("[^\d\.]", "", update.message.text).strip()
    try:
        if len(message) == 4:
            time = message[0:2] + ":" + message[2:]
        else:
            time = message[0] + ":" + message[1:]
    except IndexError:
        await update.message.reply_text(
            "Укажи корректное время в формате ЧЧ:ММ")
        message = re.sub("[^\d\.]", "", update.message.text).strip()
        if len(message) == 4:
            time = message[0:2] + ":" + message[2:]
        else:
            time = message[0] + ":" + message[1:]
    habit_list.append(datetime.strptime(time, '%H:%M'))
    if update.message.text == "/cancel":
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Пока! Надеюсь ты передумаешь и заполнишь привычку", reply_markup=ReplyKeyboardRemove()
        )
        habit_list.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text("Какую привычку ты будешь выполнять?")

        return ACTION


async def action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Добавление в список привычки и получение через выбор признака приятной привычки"""
    reply_keyboard = [["Полезная", "Приятная"]]
    user = update.message.from_user
    logger.info("action of %s: %s", user.first_name, update.message.text)
    habit_list.append(update.message.text)
    if update.message.text == "/cancel":
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Пока! Надеюсь ты передумаешь и заполнишь привычку", reply_markup=ReplyKeyboardRemove()
        )
        habit_list.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "Это будет полезная привычка или приятная? Предупреждаю сразу, за приятную привычку награды не будет, а за полезную будет или награда или выполнение приятной привычки.",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Полезная или Приятная?"))

        return GOOD_HABIT_SIGN


async def good_habit_sign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Добавление в список признака приятной привычки и получение связаной привычки"""
    user = update.message.from_user
    logger.info("good habit sign of %s: %s", user.first_name, update.message.text)
    if update.message.text == "Полезная":
        habit_list.append(True)
    else:
        habit_list.append(False)
    ghs = update.message.text
    if update.message.text == "/cancel":
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Пока! Надеюсь ты передумаешь и заполнишь привычку", reply_markup=ReplyKeyboardRemove()
        )
        habit_list.clear()
        return ConversationHandler.END
    else:
        if ghs == "Полезная":
            user_habits = []
            for rel_hb in rel_habits:
                if rel_hb[2] == update.message.chat_id:
                    user_habits.append(rel_hb)
            if len(user_habits) > 0:
                reply_keyboard = [[i[1] for i in user_habits]]
                print([(str(i[0]) + " " + i[1]) for i in user_habits])
                await update.message.reply_text(
                    "Хочешь связать полезную привычку с приятной?",
                    reply_markup=ReplyKeyboardMarkup(
                        reply_keyboard, one_time_keyboard=True,
                        input_field_placeholder=', '.join([(str(i[0]) + " " + i[1]) for i in user_habits])))
            else:
                reply_keyboard = [["None", ]]
                await update.message.reply_text(
                    "Нет приятных привычек, поэтому привычки связывать не будем. Просто жмякай None",
                    reply_markup=ReplyKeyboardMarkup(
                        reply_keyboard, one_time_keyboard=True,
                        input_field_placeholder="None"))
                habit_list.append(None)
            return RELEATED_HABIT
        else:
            reply_keyboard = [["None", ]]
            await update.message.reply_text(
                "Выбрана приятная привычка, поэтому привычки связывать не будем. Просто жмякай None",
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True,
                    input_field_placeholder="None"))
            return RELEATED_HABIT


async def related_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Добавление в список связаной привычки и получение частоты выполнения в неделю через выбор пользователя"""
    reply_keyboard = [["1", "2", "3", "4", "5", "6", "7", ]]
    user = update.message.from_user
    list_of_rel_habits = [(str(i[0]) + " " + i[1]) for i in rel_habits]
    logger.info("releted_habit of %s: %s", user.first_name, update.message.text)
    for hab in list_of_rel_habits:
        if update.message.text in hab:
            id = hab.split(" ")
            habit_list.append(int(id[0]))
            break
    if update.message.text == "/cancel":
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Пока! Надеюсь ты передумаешь и заполнишь привычку", reply_markup=ReplyKeyboardRemove()
        )
        habit_list.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "Сколько раз в неделю ты будешь выполнять привычку?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True,
                input_field_placeholder="1 раз в неделю, 2 раза в неделю, 3 раза в неделю, 4 раза в неделю, 5 раз в неделю, 6 раз в неделю, 7 раз в неделю,"))

        return FREQUENCY


async def frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Добавление в список частоты выполнения и получение награды"""
    reply_keyboard = [["None", ]]
    user = update.message.from_user
    logger.info("frequency of %s: %s", user.first_name, update.message.text)
    habit_list.append(int(update.message.text))
    if update.message.text == "/cancel":
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Пока! Надеюсь ты передумаешь и заполнишь привычку", reply_markup=ReplyKeyboardRemove()
        )
        habit_list.clear()
        return ConversationHandler.END
    else:
        logger.info(print(habit_list[RELEATED_HABIT]))
        if habit_list[GOOD_HABIT_SIGN] == "Полезная" and habit_list[RELEATED_HABIT] is None:
            await update.message.reply_text(
                "Какую награду ты хочешь получить за выполнение привычки?")

            return REWARD

        else:
            await update.message.reply_text(
                "Выбрана приятная привычка или выбрана связанная привычка поэтому награды не будет. Просто жмякай None",
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True,
                    input_field_placeholder="None"))
            return REWARD


async def reward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Добавление в список награды и получение времени на выполнение"""
    user = update.message.from_user
    logger.info("reward of %s: %s", user.first_name, update.message.text)
    habit_list.append(update.message.text)
    if update.message.text == "/cancel":
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Пока! Надеюсь ты передумаешь и заполнишь привычку", reply_markup=ReplyKeyboardRemove()
        )
        habit_list.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "Сколько отведем времени на выполнение привычки? Должно быть не более 120 секунд.")

        return TIME_TO_COMPLETE


async def time_to_complete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Добавление в список времени на выполнение и получение признака публичности"""
    reply_keyboard = [["Публичная", "Приватная"]]
    user = update.message.from_user
    logger.info("time to complete of %s: %s", user.first_name, update.message.text)
    if isinstance(int(update.message.text), int) and int(update.message.text) < 120:
        habit_list.append(timedelta(seconds=int(update.message.text)))
    else:
        habit_list.append(timedelta(seconds=120))
    if update.message.text == "/cancel":
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Пока! Надеюсь ты передумаешь и заполнишь привычку", reply_markup=ReplyKeyboardRemove()
        )
        habit_list.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "И последний вопрос, сделаем привычку публичной? Пользователи смогут посмотреть эту привычку и забрать идею себе.",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True,
                input_field_placeholder="Публичная или Приватная"))

        return IS_PUBLIC


async def is_public(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Добавление в список признака публичности и загрузка списка в базу и его очистка"""
    user = update.message.from_user
    logger.info("IS public of %s: %s", user.first_name, update.message.text)
    if update.message.text == "False":
        habit_list.append(False)
    else:
        habit_list.append(True)
    if update.message.text == "/cancel":
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Пока! Надеюсь ты передумаешь и заполнишь привычку", reply_markup=ReplyKeyboardRemove()
        )
        habit_list.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "Спасибо за ответы, теперь жди от меня напоминания о выполнении твоих привычек. Хорошего дня!")

        logger.info(habit_list)
        save_data_to_database(habit_list)
        habit_list.clear()
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена работы бота"""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Пока! Надеюсь ты передумаешь и заполнишь привычку", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def send_to_telegram(chat_id, message):
    """Функция для отправки сообщения в телеграм"""
    apiToken = settings.TG_KEY
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    response = requests.get(apiURL, data={'chat_id': chat_id, 'text': message}).json()
    try:
        response['error_code']
    except KeyError:
        return None
    else:
        return response['error_code']
