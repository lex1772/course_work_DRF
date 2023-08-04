from typing import Any

import psycopg2

from config import settings


def save_data_to_database(data: list[str, Any]):
    conn = psycopg2.connect(dbname=settings.DATABASES['default']['NAME'], user=settings.DATABASES['default']['USER'],
                            password=settings.DATABASES['default']['PASSWORD'])

    with conn.cursor() as cur:
        for i in range(len(data)):
            print(i, data[i])
        chat_id = data[0]
        place = data[1]
        time = data[2]
        action = data[3]
        good_habit_sign = data[4]
        related_habit = data[5]
        frequency = data[6]
        reward = data[7]
        time_to_complete = data[8]
        is_public = data[9]
        cur.execute(
            """
            INSERT INTO habit_habit (place, time, action, good_habit_sign, frequency, reward, time_to_complete, is_public, related_habit_id, tg_chat_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (place, time, action, good_habit_sign, frequency, reward, time_to_complete, is_public, related_habit,
             chat_id)
        )

    conn.commit()
    conn.close()


def get_related_habit(
        conn=psycopg2.connect(dbname=settings.DATABASES['default']['NAME'], user=settings.DATABASES['default']['USER'],
                              password=settings.DATABASES['default']['PASSWORD'])):
    """Функция, которая получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, action, tg_chat_id FROM habit_habit WHERE good_habit_sign = 'true' AND is_public = 'true'")
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append(row)
    return data
