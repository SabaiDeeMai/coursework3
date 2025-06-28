from database import create_database, create_tables, fill_tables
from db_manager import DBManager


def main():
    # Параметры подключения и список компаний
    companies = [
        "Вконтакте", "Яндекс", "Авито", "Озон", "Т-банк",
        "Билайн", "МТС", "Мегафон", "Skypro", "Сбер"
    ]

    # Создание и заполнение БД
    create_database()
    create_tables()
    fill_tables(companies)

    # Работа с пользователем
    db_manager = DBManager()
    while True:
        print("\n1. Список компаний и количество вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            data = db_manager.get_companies_and_vacancies_count()
            for item in data:
                print(f"{item['name']}: {item['count']} вакансий")

        elif choice == "2":
            data = db_manager.get_all_vacancies()
            for vac in data:
                salary = f"{vac['salary_from']}-{vac['salary_to']}" if vac['salary_from'] and vac[
                    'salary_to'] else "Не указана"
                print(f"{vac['company']} - {vac['title']} - Зарплата: {salary} - {vac['url']}")

        elif choice == "3":
            avg = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg} руб.")

        elif choice == "4":
            data = db_manager.get_vacancies_with_higher_salary()
            for vac in data:
                salary = f"{vac['salary_from']}-{vac['salary_to']}"
                print(f"{vac['company']} - {vac['title']} - Зарплата: {salary} - {vac['url']}")

        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            data = db_manager.get_vacancies_with_keyword(keyword)
            for vac in data:
                salary = f"{vac['salary_from']}-{vac['salary_to']}" if vac['salary_from'] and vac[
                    'salary_to'] else "Не указана"
                print(f"{vac['company']} - {vac['title']} - Зарплата: {salary} - {vac['url']}")

        elif choice == "0":
            break


if __name__ == "__main__":
    main()
