from typing import Any, Dict, List

import psycopg2

from config import Config


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
        )

    def __del__(self):
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> List[Dict[str, Any]]:
        """Возвращает список компаний с количеством вакансий."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, COUNT(v.vacancy_id)
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name
            """
            )
            return [{"name": row[0], "count": row[1]} for row in cur.fetchall()]

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """Возвращает все вакансии с указанием компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
            """
            )
            return [
                {
                    "company": row[0],
                    "title": row[1],
                    "salary_from": row[2],
                    "salary_to": row[3],
                    "url": row[4],
                }
                for row in cur.fetchall()
            ]

    def get_avg_salary(self) -> float:
        """Возвращает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((salary_from + salary_to) / 2)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """
            )
            return round(cur.fetchone()[0], 2)

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """Возвращает вакансии с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE (v.salary_from + v.salary_to) / 2 > %s
            """,
                (avg_salary,),
            )
            return [
                {
                    "company": row[0],
                    "title": row[1],
                    "salary_from": row[2],
                    "salary_to": row[3],
                    "url": row[4],
                }
                for row in cur.fetchall()
            ]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Возвращает вакансии, содержащие ключевое слово в названии."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.title ILIKE %s
            """,
                (f"%{keyword}%",),
            )
            return [
                {
                    "company": row[0],
                    "title": row[1],
                    "salary_from": row[2],
                    "salary_to": row[3],
                    "url": row[4],
                }
                for row in cur.fetchall()
            ]
