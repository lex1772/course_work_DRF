import telegram

from config import settings
from tg_funcs import start, PLACE, place, TIME, time_to_start, ACTION, action, GOOD_HABIT_SIGN, good_habit_sign, \
    RELEATED_HABIT, related_habit, FREQUENCY, frequency, REWARD, reward, TIME_TO_COMPLETE, time_to_complete, IS_PUBLIC, \
    is_public, cancel

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Файл для запуска бота в телеграм

# Подключаем бота
bot = telegram.Bot(settings.TG_KEY)


def main():
    '''Функция для работы самого бота'''
    application = Application.builder().token(settings.TG_KEY).build()

    # Список вопросов от бота
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PLACE: [MessageHandler(filters.TEXT, place)],
            TIME: [MessageHandler(filters.TEXT, time_to_start)],
            ACTION: [MessageHandler(filters.TEXT, action), ],
            GOOD_HABIT_SIGN: [MessageHandler(filters.TEXT, good_habit_sign), ],
            RELEATED_HABIT: [MessageHandler(filters.TEXT, related_habit)],
            FREQUENCY: [MessageHandler(filters.TEXT, frequency)],
            REWARD: [MessageHandler(filters.TEXT, reward)],
            TIME_TO_COMPLETE: [MessageHandler(filters.TEXT, time_to_complete)],
            IS_PUBLIC: [MessageHandler(filters.TEXT, is_public)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
