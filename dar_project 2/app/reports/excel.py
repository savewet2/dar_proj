from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from app.config import EXPORTS_DIR


def _salary_to_text(salary: Dict[str, Any] | None) -> str:
    if not salary:
        return "Не указана"

    sal_from = salary.get("from")
    sal_to = salary.get("to")
    currency = salary.get("currency") or ""

    if sal_from and sal_to:
        return f"{sal_from} - {sal_to} {currency}".strip()
    if sal_from:
        return f"от {sal_from} {currency}".strip()
    if sal_to:
        return f"до {sal_to} {currency}".strip()
    return "Не указана"


def export_vacancies_to_excel(vacancies: List[Dict[str, Any]], filename: str = "vacancies_report.xlsx") -> Path:
    if not vacancies:
        raise ValueError("Нет данных для экспорта.")

    rows = []
    for vacancy in vacancies:
        rows.append(
            {
                "Название": vacancy.get("name", ""),
                "Город": vacancy.get("area", {}).get("name", ""),
                "Компания": vacancy.get("employer", {}).get("name", ""),
                "Зарплата": _salary_to_text(vacancy.get("salary")),
                "Опыт": vacancy.get("experience", {}).get("name", ""),
                "Тип занятости": vacancy.get("employment", {}).get("name", ""),
                "График": vacancy.get("schedule", {}).get("name", ""),
                "Дата публикации": vacancy.get("published_at", ""),
                "Ссылка": vacancy.get("alternate_url", ""),
            }
        )

    df = pd.DataFrame(rows)
    path = EXPORTS_DIR / filename
    df.to_excel(path, index=False)
    return path
