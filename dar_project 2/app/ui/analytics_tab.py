from __future__ import annotations

import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QMessageBox,
)

from app.services.ai_service import AIService
from app.services.analytics_service import AnalyticsService


class AnalyticsTab(QWidget):
    def __init__(self, vacancies_tab) -> None:
        super().__init__()

        self.vacancies_tab = vacancies_tab
        self.analytics_service = AnalyticsService()
        self.ai_service = AIService()

        root = QVBoxLayout(self)
        buttons = QHBoxLayout()

        self.summary_button = QPushButton("Показать сводку")
        self.salary_chart_button = QPushButton("График зарплат")
        self.city_chart_button = QPushButton("Топ городов")
        self.month_chart_button = QPushButton("Вакансии по месяцам")
        self.ai_button = QPushButton("AI-анализ")

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        buttons.addWidget(self.summary_button)
        buttons.addWidget(self.salary_chart_button)
        buttons.addWidget(self.city_chart_button)
        buttons.addWidget(self.month_chart_button)
        buttons.addWidget(self.ai_button)

        root.addLayout(buttons)
        root.addWidget(self.output)

        self.summary_button.clicked.connect(self.show_summary)
        self.salary_chart_button.clicked.connect(self.show_salary_chart)
        self.city_chart_button.clicked.connect(self.show_city_chart)
        self.month_chart_button.clicked.connect(self.show_month_chart)
        self.ai_button.clicked.connect(self.show_ai_analysis)

    def _get_data(self) -> list[dict]:
        return self.vacancies_tab.data

    def show_summary(self) -> None:
        data = self._get_data()
        self.output.setText(self.analytics_service.summary_text(data))

    def show_salary_chart(self) -> None:
        data = self._get_data()
        buckets = self.analytics_service.salary_buckets(data)

        if not any(buckets.values()):
            QMessageBox.information(self, "Нет данных", "Нет зарплат для построения графика.")
            return

        plt.figure(figsize=(8, 5))
        plt.bar(list(buckets.keys()), list(buckets.values()))
        plt.title("Распределение зарплат")
        plt.xlabel("Диапазон")
        plt.ylabel("Количество вакансий")
        plt.tight_layout()
        plt.show()

    def show_city_chart(self) -> None:
        data = self._get_data()
        top = self.analytics_service.top_cities(data, 10)

        if not top:
            QMessageBox.information(self, "Нет данных", "Нет данных по городам.")
            return

        labels = [x[0] for x in top]
        values = [x[1] for x in top]

        plt.figure(figsize=(10, 5))
        plt.bar(labels, values)
        plt.title("Топ городов")
        plt.xlabel("Город")
        plt.ylabel("Количество вакансий")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.show()

    def show_month_chart(self) -> None:
        data = self._get_data()
        monthly = self.analytics_service.vacancies_by_month(data)

        if not monthly:
            QMessageBox.information(self, "Нет данных", "Нет данных по датам публикации.")
            return

        labels = [x[0] for x in monthly]
        values = [x[1] for x in monthly]

        plt.figure(figsize=(10, 5))
        plt.plot(labels, values, marker="o")
        plt.title("Вакансии по месяцам")
        plt.xlabel("Месяц")
        plt.ylabel("Количество вакансий")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.show()

    def show_ai_analysis(self) -> None:
        data = self._get_data()
        answer, citations = self.ai_service.generate_answer(
            query="Проанализируй рынок вакансий по найденным данным.",
            vacancies=data,
        )

        parts = [answer]

        if citations:
            parts.append("\nПримеры вакансий:")
            for item in citations[:5]:
                parts.append(
                    f"- {item['name']} | {item['company']} | {item['city']}\n  {item['url']}"
                )

        self.output.setText("\n".join(parts))
