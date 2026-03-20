from PyQt6.QtWidgets import QMainWindow, QTabWidget, QToolBar, QPushButton

from app.ui.analytics_tab import AnalyticsTab
from app.ui.vacancies_tab import VacanciesTab


class MainWindow(QMainWindow):
    def __init__(self, current_user: str, app, dark_theme: str, light_theme: str) -> None:
        super().__init__()
        self.setWindowTitle(f"HH Analytics — {current_user}")
        self.resize(1280, 780)

        self.app = app
        self.dark_theme = dark_theme
        self.light_theme = light_theme
        self.is_dark = True

        self.tabs = QTabWidget()

        self.vacancies_tab = VacanciesTab()
        self.analytics_tab = AnalyticsTab(self.vacancies_tab)

        self.tabs.addTab(self.vacancies_tab, "Вакансии")
        self.tabs.addTab(self.analytics_tab, "Аналитика")

        self.setCentralWidget(self.tabs)

        toolbar = QToolBar("Тема")
        self.addToolBar(toolbar)

        self.theme_button = QPushButton("Светлая тема")
        self.theme_button.clicked.connect(self.toggle_theme)
        toolbar.addWidget(self.theme_button)

    def toggle_theme(self) -> None:
        if self.is_dark:
            self.app.setStyleSheet(self.light_theme)
            self.theme_button.setText("Тёмная тема")
        else:
            self.app.setStyleSheet(self.dark_theme)
            self.theme_button.setText("Светлая тема")

        self.is_dark = not self.is_dark