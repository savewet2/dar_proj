from typing import Any, Dict, List, Tuple
import random

from openai import OpenAI
from openai import (
    RateLimitError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
)



class AIService:
    def __init__(self) -> None:
        self.client = None

        self.client = OpenAI(
                api_key= "sk-vxqwOVCM3RudJqOLK1akWIYZg0CABEinB5SQuZNyOrqrl5EiaZ69aWRhZdnW",
                base_url= "https://proxy.gen-api.ru/v1",
            )

    def _pick_sample(self, vacancies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if len(vacancies) <= 10:
            return vacancies
        return random.sample(vacancies, 10)

    def _salary_to_text(self, salary: Dict[str, Any] | None) -> str:
        if not salary:
            return "не указана"

        salary_from = salary.get("from")
        salary_to = salary.get("to")
        currency = salary.get("currency", "")

        if salary_from and salary_to:
            return f"{salary_from} - {salary_to} {currency}".strip()
        if salary_from:
            return f"от {salary_from} {currency}".strip()
        if salary_to:
            return f"до {salary_to} {currency}".strip()

        return "не указана"

    def build_context(self, vacancies: List[Dict[str, Any]]) -> str:
        sampled = self._pick_sample(vacancies)
        parts = []

        for i, vacancy in enumerate(sampled, start=1):
            salary_text = self._salary_to_text(vacancy.get("salary"))

            parts.append(
                f"""[Вакансия {i}]
Название: {vacancy.get("name", "")}
Город: {vacancy.get("area", {}).get("name", "")}
Компания: {vacancy.get("employer", {}).get("name", "")}
Опыт: {vacancy.get("experience", {}).get("name", "")}
График: {vacancy.get("schedule", {}).get("name", "")}
Занятость: {vacancy.get("employment", {}).get("name", "")}
Зарплата: {salary_text}
Ссылка: {vacancy.get("alternate_url", "")}"""
            )

        return "\n\n".join(parts)

    def build_citations(self, vacancies: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        sampled = self._pick_sample(vacancies)

        return [
            {
                "name": vacancy.get("name", ""),
                "company": vacancy.get("employer", {}).get("name", ""),
                "city": vacancy.get("area", {}).get("name", ""),
                "salary": self._salary_to_text(vacancy.get("salary")),
                "url": vacancy.get("alternate_url", ""),
            }
            for vacancy in sampled
        ]

    def generate_answer(
        self,
        query: str,
        vacancies: List[Dict[str, Any]],
    ) -> Tuple[str, List[Dict[str, str]]]:
        if not vacancies:
            return "По найденным вакансиям нет данных для AI-анализа.", []

        sampled = self._pick_sample(vacancies)
        citations = self.build_citations(sampled)

        if self.client is None:
            return (
                "GENAPI_API_KEY не задан. Поэтому AI-анализ сейчас недоступен.\n\n"
                "Ниже показаны примеры найденных вакансий.",
                citations,
            )

        context = self.build_context(sampled)

        system_prompt = (
            "Ты опытный HR-аналитик. "
            "Отвечай только на основе переданных вакансий. "
            "Не выдумывай факты. "
            "Если данных недостаточно, прямо скажи об этом. "
            "Пиши кратко, ясно и на русском языке."
            "Пиши без ### и так далее , так же НИКОГДА НЕ УПОМИНАЙ ПРО КОЛИЧЕСТВО ВАКАНСКИЙ"
        )

        user_prompt = f"""
Контекст:
{context}

Запрос:
{query}

Сделай структурированный отчёт с разделами:
1. Общая картина рынка
2. Зарплаты
3. Требования и опыт
4. Вывод
""".strip()

        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=700,
            )

            answer = response.choices[0].message.content.strip()

            if not answer:
                answer = (
                    "Не удалось получить текстовый ответ от модели.\n\n"
                    "Ниже показаны примеры найденных вакансий."
                )

            return answer, citations

        except RateLimitError:
            return (
                "Сейчас AI-анализ недоступен: превышен лимит запросов.\n\n"
                "Ниже показаны примеры найденных вакансий.",
                citations,
            )

        except AuthenticationError:
            return (
                "Сейчас AI-анализ недоступен: проблема с API-ключом GenAPI.\n\n"
                "Ниже показаны примеры найденных вакансий.",
                citations,
            )

        except BadRequestError as e:
            return (
                f"Сейчас AI-анализ недоступен: ошибка запроса к модели ({e}).\n\n"
                "Ниже показаны примеры найденных вакансий.",
                citations,
            )

        except APITimeoutError:
            return (
                "Сейчас AI-анализ недоступен: сервер модели не ответил вовремя.\n\n"
                "Ниже показаны примеры найденных вакансий.",
                citations,
            )

        except APIError as e:
            return (
                f"Сейчас AI-анализ временно недоступен: ошибка API ({e}).\n\n"
                "Ниже показаны примеры найденных вакансий.",
                citations,
            )

        except Exception as e:
            return (
                f"Сейчас AI-анализ временно недоступен: {e}\n\n"
                "Ниже показаны примеры найденных вакансий.",
                citations,
            )