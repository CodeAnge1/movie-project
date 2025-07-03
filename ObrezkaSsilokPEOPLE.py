import psycopg2
import re


# Подключение к базе данных
def trim_photo_urls():
    conn = psycopg2.connect(
        dbname="CoopProject",
        user="postgres",
        password="1234",
        host="localhost"
    )
    cursor = conn.cursor()

    try:
        # Получаем все записи из таблицы people
        cursor.execute("SELECT id, photo_url FROM people")
        records = cursor.fetchall()

        updated_count = 0

        for record in records:
            person_id, old_url = record

            # Извлекаем имя файла из URL
            new_filename = f"360_{person_id}.jpg"

            # Обновляем запись в базе данных
            cursor.execute(
                "UPDATE people SET photo_url = %s WHERE id = %s",
                (new_filename, person_id)
            )
            updated_count += 1

        conn.commit()
        print(f"Обновлено {updated_count} записей в таблице people")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    trim_photo_urls()