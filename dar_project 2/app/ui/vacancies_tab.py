from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QComboBox,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)

from app.api.hh_client import HHClient
from app.reports.excel import export_vacancies_to_excel


EXPERIENCE_OPTIONS = {
    "Любой": "",
    "Нет опыта": "noExperience",
    "От 1 года до 3 лет": "between1And3",
    "От 3 до 6 лет": "between3And6",
    "Более 6 лет": "moreThan6",
}

SCHEDULE_OPTIONS = {
    "Любой": "",
    "Полный день": "fullDay",
    "Сменный график": "shift",
    "Гибкий график": "flexible",
    "Удаленная работа": "remote",
    "Вахта": "flyInFlyOut",
}

EMPLOYMENT_OPTIONS = {
    "Любой": "",
    "Полная занятость": "full",
    "Частичная занятость": "part",
    "Проектная работа": "project",
    "Стажировка": "probation",
    "Волонтерство": "volunteer",
}

PROFESSIONAL_ROLES = {
    "Любая": "",
    "Программист, разработчик": "96",
    "Системный администратор": "157",
    "DevOps-инженер": "160",
    "Аналитик": "10",
    "Тестировщик": "124",
    "Менеджер проекта": "107",
    "Дизайнер": "34",
}

DATE_FILTERS = {
    "Любая дата": "",
    "За сутки": "1",
    "За 3 дня": "3",
    "За неделю": "7",
    "За месяц": "30",
}


class VacanciesTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.hh_client = HHClient()
        self.data = []

        root = QVBoxLayout(self)
        root.setSpacing(10)

        filters_row_1 = QHBoxLayout()
        filters_row_2 = QHBoxLayout()
        actions_row = QHBoxLayout()

        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Профессия или ключевой запрос")

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Город вручную, например: Москва")

        self.salary_spin = QSpinBox()
        self.salary_spin.setRange(0, 5_000_000)
        self.salary_spin.setSingleStep(5000)
        self.salary_spin.setValue(0)
        self.salary_spin.setPrefix("от ")

        self.only_salary_checkbox = QCheckBox("Только с зарплатой")
        self.sort_new_checkbox = QCheckBox("Сначала новые")

        self.date_filter_combo = QComboBox()
        self.date_filter_combo.addItems(DATE_FILTERS.keys())

        self.experience_combo = QComboBox()
        self.experience_combo.addItems(EXPERIENCE_OPTIONS.keys())

        self.schedule_combo = QComboBox()
        self.schedule_combo.addItems(SCHEDULE_OPTIONS.keys())

        self.employment_combo = QComboBox()
        self.employment_combo.addItems(EMPLOYMENT_OPTIONS.keys())

        self.role_combo = QComboBox()
        self.role_combo.addItems(PROFESSIONAL_ROLES.keys())

        self.search_button = QPushButton("Найти вакансии")
        self.clear_button = QPushButton("Сбросить фильтры")
        self.export_button = QPushButton("Экспорт в Excel")

        self.status_label = QLabel("Введите параметры поиска и нажмите кнопку.")

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            [
                "Вакансия",
                "Город",
                "Компания",
                "Зарплата",
                "Опыт",
                "График",
                "Тип занятости",
            ]
        )
        self.table.setWordWrap(True)
        self.table.cellDoubleClicked.connect(self.open_link)

        filters_row_1.addWidget(QLabel("Запрос:"))
        filters_row_1.addWidget(self.query_input)
        filters_row_1.addWidget(QLabel("Город:"))
        filters_row_1.addWidget(self.city_input)
        filters_row_1.addWidget(QLabel("ЗП:"))
        filters_row_1.addWidget(self.salary_spin)

        filters_row_2.addWidget(QLabel("Новизна:"))
        filters_row_2.addWidget(self.date_filter_combo)
        filters_row_2.addWidget(QLabel("Опыт:"))
        filters_row_2.addWidget(self.experience_combo)
        filters_row_2.addWidget(QLabel("График:"))
        filters_row_2.addWidget(self.schedule_combo)
        filters_row_2.addWidget(QLabel("Занятость:"))
        filters_row_2.addWidget(self.employment_combo)
        filters_row_2.addWidget(QLabel("Роль:"))
        filters_row_2.addWidget(self.role_combo)
        filters_row_2.addWidget(self.only_salary_checkbox)
        filters_row_2.addWidget(self.sort_new_checkbox)

        actions_row.addWidget(self.search_button)
        actions_row.addWidget(self.clear_button)
        actions_row.addWidget(self.export_button)

        root.addLayout(filters_row_1)
        root.addLayout(filters_row_2)
        root.addLayout(actions_row)
        root.addWidget(self.status_label)
        root.addWidget(self.table)

        self.search_button.clicked.connect(self.load_data)
        self.clear_button.clicked.connect(self.clear_filters)
        self.export_button.clicked.connect(self.export_data)

    def clear_filters(self) -> None:
        self.query_input.clear()
        self.city_input.clear()
        self.salary_spin.setValue(0)
        self.only_salary_checkbox.setChecked(False)
        self.sort_new_checkbox.setChecked(False)
        self.date_filter_combo.setCurrentIndex(0)
        self.experience_combo.setCurrentIndex(0)
        self.schedule_combo.setCurrentIndex(0)
        self.employment_combo.setCurrentIndex(0)
        self.role_combo.setCurrentIndex(0)
        self.status_label.setText("Фильтры сброшены.")

    def load_data(self) -> None:
        self.search_button.setEnabled(False)
        self.status_label.setText("Загрузка вакансий...")

        try:
            salary_from = self.salary_spin.value() or None
            date_from_days = DATE_FILTERS[self.date_filter_combo.currentText()]

            self.data = self.hh_client.search_vacancies(
                query=self.query_input.text(),
                city=self.city_input.text(),
                salary_from=salary_from,
                only_with_salary=self.only_salary_checkbox.isChecked(),
                sort_new=self.sort_new_checkbox.isChecked(),
                experience_id=EXPERIENCE_OPTIONS[self.experience_combo.currentText()],
                schedule_id=SCHEDULE_OPTIONS[self.schedule_combo.currentText()],
                employment_id=EMPLOYMENT_OPTIONS[self.employment_combo.currentText()],
                professional_role_id=PROFESSIONAL_ROLES[self.role_combo.currentText()],
                date_from_days=date_from_days,
            )

            self.populate_table(self.data)
            self.status_label.setText(f"Загружено вакансий: {len(self.data)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить вакансии:\n{e}")
            self.status_label.setText("Ошибка загрузки.")
        finally:
            self.search_button.setEnabled(True)

    def populate_table(self, vacancies: list[dict]) -> None:
        self.table.setRowCount(len(vacancies))

        for row, vacancy in enumerate(vacancies):
            salary = vacancy.get("salary") or {}
            salary_text = "Не указана"
            salary_from = salary.get("from")
            salary_to = salary.get("to")
            currency = salary.get("currency") or ""

            if salary_from and salary_to:
                salary_text = f"{salary_from} - {salary_to} {currency}".strip()
            elif salary_from:
                salary_text = f"от {salary_from} {currency}".strip()
            elif salary_to:
                salary_text = f"до {salary_to} {currency}".strip()

            title_item = QTableWidgetItem(vacancy.get("name", ""))
            title_item.setForeground(Qt.GlobalColor.cyan)
            title_item.setToolTip(vacancy.get("alternate_url", ""))
            title_item.setData(Qt.ItemDataRole.UserRole, vacancy.get("alternate_url", ""))

            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, QTableWidgetItem(vacancy.get("area", {}).get("name", "")))
            self.table.setItem(row, 2, QTableWidgetItem(vacancy.get("employer", {}).get("name", "")))
            self.table.setItem(row, 3, QTableWidgetItem(salary_text))
            self.table.setItem(row, 4, QTableWidgetItem(vacancy.get("experience", {}).get("name", "")))
            self.table.setItem(row, 5, QTableWidgetItem(vacancy.get("schedule", {}).get("name", "")))
            self.table.setItem(row, 6, QTableWidgetItem(vacancy.get("employment", {}).get("name", "")))

        self.table.resizeColumnsToContents()

    def open_link(self, row: int, column: int) -> None:
        item = self.table.item(row, 0)
        if not item:
            return

        url = item.data(Qt.ItemDataRole.UserRole)
        if url:
            QDesktopServices.openUrl(QUrl(url))

    def export_data(self) -> None:
        try:
            path: Path = export_vacancies_to_excel(self.data)
            QMessageBox.information(self, "Готово", f"Файл сохранён:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка экспорта", str(e))