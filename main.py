import requests
import psycopg2
from psycopg2 import sql
from config import DB_CONFIG  # Ваши настройки БД

# Настройки API Кинопоиска
API_KEY = "XRDTMJF-TFS46CS-GA7KVX1-04ZX7HW"
BASE_URL = "https://api.kinopoisk.dev/v1.3/movie"

# Подключение к БД
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()


def fetch_movies_from_api(year=None, genre=None, limit=250, page=400):
    """Получение фильмов с API Кинопоиска"""
    headers = {"X-API-KEY": API_KEY}
    params = {
        "page": page,
        'limit': limit,
        'selectFields': ['id', 'name', 'alternativeName', 'description',
                         'year', 'rating.kp', 'movieLength', 'type',
                         'genres.name', 'countries.name', 'poster.url',
                         'videos.trailers.url', 'persons.id', 'persons.name',
                         'persons.photo', 'persons.enProfession']
    }
    if year:
        params['year'] = year
    if genre:
        params['genres.name'] = genre

    response = requests.get(BASE_URL, headers=headers, params=params)
    return response.json()['docs'] if response.status_code == 200 else []


def save_to_database(movies):
    """Сохранение данных в PostgreSQL с обработкой NULL"""
    for movie in movies:
        # Пропускаем фильмы без обязательных полей
        if not movie.get('name') or not movie.get('alternativeName'):
            continue

        try:
            cursor.execute(
                """
                INSERT INTO films (kp_id, type, title, original_title, description, year, rating, duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    movie['id'],
                    movie.get('type', 'movie'),
                    movie.get('name', ''),
                    movie.get('alternativeName', ''),  # Гарантировано не NULL
                    movie.get('description', ''),
                    movie.get('year', 0),
                    float(movie.get('rating', {}).get('kp', 0)),
                    int(movie.get('movieLength', 0))
                )
            )



        except Exception as e:
            print(f"Ошибка при сохранении фильма ID {movie['id']}: {str(e)}")
            conn.rollback()
        cursor.execute("SELECT id FROM films WHERE kp_id = %s", (movie["id"],))
        result = cursor.fetchone()
        globalID = result[0] if result else None
        if globalID:
            # 2. Сохраняем жанры (film_genres)
            for genre in movie.get('genres', []):
                # Сначала проверяем существует ли жанр
                cursor.execute(
                    "SELECT id FROM genres WHERE name = %s",
                    (genre['name'],)
                )
                genre_id = cursor.fetchone()

                if not genre_id:
                    cursor.execute(
                        "INSERT INTO genres (name) VALUES (%s) RETURNING id",
                        (genre['name'],)
                    )
                    genre_id = cursor.fetchone()[0]
                else:
                    genre_id = genre_id[0]

                # Связываем фильм и жанр
                cursor.execute(
                    """
                    INSERT INTO film_genres (film_id, genre_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (globalID, genre_id)
                )

            # 3. Сохраняем страны (film_countries)
            for country in movie.get('countries', []):
                cursor.execute(
                    "SELECT id FROM countries WHERE name = %s",
                    (country['name'],)
                )
                country_id = cursor.fetchone()

                if not country_id:
                    cursor.execute(
                        "INSERT INTO countries (name) VALUES (%s) RETURNING id",
                        (country['name'],)
                    )
                    country_id = cursor.fetchone()[0]
                else:
                    country_id = country_id[0]

                cursor.execute(
                    """
                    INSERT INTO film_countries (film_id, country_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (globalID, country_id)
                )

            # 4. Сохраняем людей (film_people)
            for person in movie.get('persons', []):
                if not person.get('id'):
                    continue

                cursor.execute(
                    """
                    INSERT INTO people (id, first_name, last_name, photo_url)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        person['id'],
                        person.get('name', '').split(' ')[0] if person.get('name') else '',
                        ' '.join(person.get('name', '').split(' ')[1:]) if person.get('name') else '',
                        person.get('photo', '')
                    )
                )

                # Связываем фильм и человека
                cursor.execute(
                    """
                    INSERT INTO film_people (film_id, person_id, role, character_name)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (globalID, person['id'], person.get('enProfession', 'actor'), person.get("description", None))
                )

            # 5. Сохраняем медиа (media)
            if movie.get('poster', {}).get('url'):
                cursor.execute(
                    """
                    INSERT INTO media (film_id, type, url)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (globalID, 'poster', movie['poster']['url'])
                )

            # 6. Сохраняем трейлеры (trailers)
            for trailer in movie.get('videos', {}).get('trailers', []):
                if trailer.get('url'):
                    cursor.execute(
                        """
                        INSERT INTO trailers (film_id, url)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (globalID, trailer['url'])
                    )

        conn.commit()


# Пример использования
if __name__ == "__main__":
    for page in range(400, 600):
        movies_data = fetch_movies_from_api(page=page)

        if movies_data:
            save_to_database(movies_data)
            print(f"Успешно сохранено {len(movies_data)} фильмов в базу данных")
        else:
            print("Не удалось получить данные с API")

    cursor.close()
    conn.close()