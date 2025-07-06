import psycopg2
from psycopg2 import sql
from collections import defaultdict

def find_duplicates_in_database():
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname="CoopProject",
        user="postgres",  # замените на ваше имя пользователя
        password="1234",  # замените на ваш пароль
        host="localhost"
    )
    cursor = conn.cursor()

    # Словарь для хранения дубликатов
    duplicates = defaultdict(list)

    try:
        # Получаем список всех таблиц в базе данных
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]

        # Для каждой таблицы проверяем дубликаты
        for table in tables:
            # Получаем список всех столбцов в таблице
            cursor.execute(sql.SQL("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s
            """), [table])
            columns = [row[0] for row in cursor.fetchall()]

            # Пропускаем таблицы без данных
            if not columns:
                continue

            # Формируем запрос для поиска дубликатов
            query = sql.SQL("""
                SELECT {columns}, COUNT(*) as count
                FROM {table}
                GROUP BY {columns}
                HAVING COUNT(*) > 1
            """).format(
                columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
                table=sql.Identifier(table)
            )

            cursor.execute(query)
            duplicate_rows = cursor.fetchall()

            if duplicate_rows:
                duplicates[table] = duplicate_rows

        # Выводим результаты
        if duplicates:
            print("Найдены дубликаты в следующих таблицах:")
            for table, rows in duplicates.items():
                print(f"\nТаблица: {table}")
                print(f"Количество дублирующихся комбинаций: {len(rows)}")
                print("Примеры дубликатов:")
                for row in rows[:3]:  # Показываем первые 3 примера
                    print(row)
        else:
            print("Дубликаты не найдены.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    find_duplicates_in_database()