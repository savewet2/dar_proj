from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any, Dict, List


class AnalyticsService:
    @staticmethod
    def extract_salary_values(vacancies: List[Dict[str, Any]]) -> List[int]:
        values: List[int] = []

        for vacancy in vacancies:
            salary = vacancy.get("salary")
            if not salary:
                continue

            value = salary.get("from") or salary.get("to")
            if isinstance(value, int):
                values.append(value)

        return values

    @staticmethod
    def salary_buckets(vacancies: List[Dict[str, Any]]) -> Dict[str, int]:
        buckets = {
            "0-50k": 0,
            "50-100k": 0,
            "100-150k": 0,
            "150-200k": 0,
            "200k+": 0,
        }

        for value in AnalyticsService.extract_salary_values(vacancies):
            if value < 50_000:
                buckets["0-50k"] += 1
            elif value < 100_000:
                buckets["50-100k"] += 1
            elif value < 150_000:
                buckets["100-150k"] += 1
            elif value < 200_000:
                buckets["150-200k"] += 1
            else:
                buckets["200k+"] += 1

        return buckets

    @staticmethod
    def top_cities(vacancies: List[Dict[str, Any]], limit: int = 10) -> List[tuple[str, int]]:
        counter = Counter()

        for vacancy in vacancies:
            city = vacancy.get("area", {}).get("name") or "Не указано"
            counter[city] += 1

        return counter.most_common(limit)

    @staticmethod
    def top_employers(vacancies: List[Dict[str, Any]], limit: int = 10) -> List[tuple[str, int]]:
        counter = Counter()

        for vacancy in vacancies:
            employer = vacancy.get("employer", {}).get("name") or "Не указано"
            counter[employer] += 1

        return counter.most_common(limit)

    @staticmethod
    def vacancies_by_month(vacancies: List[Dict[str, Any]]) -> List[tuple[str, int]]:
        counter = Counter()

        for vacancy in vacancies:
            published_at = vacancy.get("published_at")
            if not published_at:
                continue

            try:
                dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                key = dt.strftime("%Y-%m")
                counter[key] += 1
            except ValueError:
                continue

        return sorted(counter.items())

    @staticmethod
    def summary_text(vacancies: List[Dict[str, Any]]) -> str:
        total = len(vacancies)
        salaries = AnalyticsService.extract_salary_values(vacancies)
        avg_salary = int(sum(salaries) / len(salaries)) if salaries else 0

        top_cities = AnalyticsService.top_cities(vacancies, 5)
        top_city_text = ", ".join(f"{city} ({count})" for city, count in top_cities) if top_cities else "нет данных"

        return (
            f"Найдено вакансий: {total}\n"
            f"Вакансий с указанной зарплатой: {len(salaries)}\n"
            f"Средняя ориентировочная зарплата: {avg_salary} ₽\n"
            f"Топ городов: {top_city_text}"
        )
