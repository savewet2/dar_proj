from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

from app.config import (
    DEFAULT_PER_PAGE,
    MAX_PAGES,
    REQUEST_TIMEOUT,
)


class HHClient:
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "HH-Analytics-App/4.0"})

    def search_vacancies(
        self,
        query: str,
        city: str = "",
        salary_from: Optional[int] = None,
        only_with_salary: bool = False,
        sort_new: bool = False,
        experience_id: str = "",
        schedule_id: str = "",
        employment_id: str = "",
        professional_role_id: str = "",
        date_from_days: str = "",
        per_page: int = DEFAULT_PER_PAGE,
        max_pages: int = MAX_PAGES,
    ) -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []

        text_parts = []
        if query.strip():
            text_parts.append(query.strip())
        if city.strip():
            text_parts.append(city.strip())

        search_text = " ".join(text_parts).strip()

        for page in range(max_pages):
            params: Dict[str, Any] = {
                "text": search_text,
                "search_field": ["name", "company_name", "description"],
                "per_page": per_page,
                "page": page,
                "area": 113,
                "only_with_salary": only_with_salary,
            }

            if salary_from is not None:
                params["salary"] = salary_from

            if sort_new:
                params["order_by"] = "publication_time"

            if experience_id:
                params["experience"] = experience_id

            if schedule_id:
                params["schedule"] = schedule_id

            if employment_id:
                params["employment"] = employment_id

            if professional_role_id:
                params["professional_role"] = professional_role_id

            if date_from_days:
                params["period"] = date_from_days

            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            payload = response.json()
            items = payload.get("items", [])

            for item in items:
                salary = item.get("salary")
                if salary and salary.get("currency") not in (None, "RUR"):
                    continue
                all_items.append(item)

            pages = payload.get("pages", 0)
            if not items or page >= pages - 1:
                break

        return all_items