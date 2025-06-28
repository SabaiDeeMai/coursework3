import psycopg2
from psycopg2 import sql

from config import Config
from hh_api import get_employer_data, get_vacancies


def create_database():
    """Создает базу данных"""
    conn = None  # Явная инициализация
    try:
        # Подключаемся к серверу PostgreSQL без указания базы данных
        conn = psycopg2.connect(
            dbname="postgres",
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Проверяем существование БД
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (Config.DB_NAME,))
        if not cur.fetchone():
            cur.execute(sql.SQL(f"CREATE DATABASE {Config.DB_NAME}"))
        cur.close()
    except Exception as e:
        print(f"Ошибка при создании БД: {str(e)}")  # Преобразуем исключение в строку
    finally:
        if conn is not None:  # Явная проверка на None
            conn.close()


def create_tables():
    """Создает таблицы в базе данных"""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
        )
        with conn.cursor() as cur:
            cur.execute(
                """
                        CREATE TABLE IF NOT EXISTS employers
                        (
                            employer_id
                            INTEGER
                            PRIMARY
                            KEY,
                            name
                            VARCHAR
                        (
                            255
                        ) NOT NULL
                            )
                        """
            )
            cur.execute(
                """
                        CREATE TABLE IF NOT EXISTS vacancies
                        (
                            vacancy_id
                            INTEGER
                            PRIMARY
                            KEY,
                            employer_id
                            INTEGER
                            REFERENCES
                            employers
                        (
                            employer_id
                        ),
                            title VARCHAR
                        (
                            255
                        ) NOT NULL,
                            salary_from INTEGER,
                            salary_to INTEGER,
                            url TEXT
                            )
                        """
            )
        conn.commit()
    except Exception as e:
        print(f"Ошибка при создании таблиц: {str(e)}")
    finally:
        if conn is not None:
            conn.close()


def fill_tables(employers: list):
    """Заполняет таблицы данными"""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
        )
        with conn.cursor() as cur:
            for employer_name in employers:
                employer = get_employer_data(employer_name)
                if not employer:
                    continue
                cur.execute(
                    "INSERT INTO employers (employer_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (employer["id"], employer["name"]),
                )
                vacancies = get_vacancies(employer["id"])
                for vacancy in vacancies:
                    salary = vacancy.get("salary")
                    salary_from = salary.get("from") if salary else None
                    salary_to = salary.get("to") if salary else None
                    cur.execute(
                        """
                        INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, url)
                        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
                        """,
                        (
                            vacancy["id"],
                            employer["id"],
                            vacancy["name"],
                            salary_from,
                            salary_to,
                            vacancy["alternate_url"],
                        ),
                    )
        conn.commit()
    except Exception as e:
        print(f"Ошибка при заполнении таблиц: {str(e)}")
    finally:
        if conn is not None:
            conn.close()
