from typing import Any, Dict, List

import requests


def get_employer_data(employer_name: str) -> Dict[str, Any] | None:
    """Получает данные о работодателе по названию."""
    url = "https://api.hh.ru/employers"
    params = {"text": employer_name, "only_with_vacancies": True}
    response = requests.get(url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])
    return items[0] if items else None


def get_vacancies(employer_id: int) -> List[Dict[str, Any]]:
    """Получает вакансии работодателя по ID."""
    url = "https://api.hh.ru/vacancies"
    params = {"employer_id": employer_id, "per_page": 100}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("items", [])
