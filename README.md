Курсовая работа 7. DRF.
=======================
Сервис, который получает от пользователя привычки и напоминает пользователю об их выполнении.

Проект сделан из двух приложений - user и habit.

:white_check_mark: Настроены ограничения на аутентификацию и владельца привычки. В случае, если привычка публичкая, то авторизованные пользователи могут увидеть привычку.

:white_check_mark:Настроены периодические задачи через celery на отправку сообщений в телеграм и по почте, в зависимости от того, как пользователь обращался к сервису.

:white_check_mark: Сделана интергация с телеграм, подключается запуском файла tg.py. При подключении активируется бот и апользователь при наборе /start получает сообщения от бота, если у него не занесены привычки. Если же занесены, то бот уведомляет об их выполнении.
