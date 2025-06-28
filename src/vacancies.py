from dataclasses import dataclass


@dataclass
class Vacancy:
    vacancy_id: int
    employer_id: int
    title: str
    salary_from: int | None
    salary_to: int | None
    url: str
