import psycopg2
import re
from urllib.parse import urlparse


# Подключение к базе данных
def update_media_urls():
    conn = psycopg2.connect(
        dbname="CoopProject",
        user="postgres",
        password="1234",
        host="localhost"
    )
    cursor = conn.cursor()

    try:
        # Получаем все записи из таблицы media
        cursor.execute("SELECT id, url FROM media WHERE type = 'poster'")
        records = cursor.fetchall()

        for record in records:
            record_id, old_url = record
            # Извлекаем нужные части URL с помощью регулярного выражения
            match = re.search(r'kinopoisk-images/(\d+)/([a-f0-9-]+)/', old_url)
            if match:
                new_url = f"{match.group(1)}/{match.group(2)}"

                # Обновляем запись в базе данных
                cursor.execute(
                    "UPDATE media SET url = %s WHERE id = %s",
                    (new_url, record_id)
                )
                print(f"Updated ID {record_id}: {old_url} -> {new_url}")
            else:
                print(f"URL не соответствует шаблону: {old_url}")

        # Применяем изменения
        conn.commit()
        print("Все URL успешно обновлены!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    update_media_urls()