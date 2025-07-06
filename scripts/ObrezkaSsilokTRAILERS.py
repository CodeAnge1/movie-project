import psycopg2
import re
from urllib.parse import urlparse


def update_trailers_urls():
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname="CoopProject",
        user="postgres",
        password="1234",
        host="localhost"
    )
    cursor = conn.cursor()

    try:
        # Получаем все записи из таблицы trailers
        cursor.execute("SELECT id, url FROM trailers")
        records = cursor.fetchall()

        for record in records:
            record_id, old_url = record
            # Извлекаем ID видео из YouTube URL
            video_id = extract_youtube_id(old_url)

            if video_id:
                # Обновляем запись в базе данных
                cursor.execute(
                    "UPDATE trailers SET url = %s WHERE id = %s",
                    (video_id, record_id)
                )
                print(f"Updated ID {record_id}: {old_url} -> {video_id}")
            else:
                print(f"Не удалось извлечь ID из URL: {old_url}")

        # Применяем изменения
        conn.commit()
        print("Все URL успешно обновлены!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def extract_youtube_id(url):
    """Извлекает ID видео из YouTube URL"""
    # Проверяем несколько возможных форматов YouTube URL
    patterns = [
        r"youtube\.com/embed/([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
        r"youtube\.com/v/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


if __name__ == "__main__":
    update_trailers_urls()