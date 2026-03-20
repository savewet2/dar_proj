import sys
from PyQt6.QtWidgets import QApplication
from app.db import init_db
from app.ui.auth_window import AuthWindow


DARK_THEME = """
QMainWindow, QWidget {
    background-color: #101418;
    color: #E6EDF3;
    font-size: 13px;
    font-family: Arial;
}
QLabel {
    color: #DCE6F2;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox, QTableWidget {
    background-color: #161B22;
    color: #E6EDF3;
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 6px;
    selection-background-color: #2F81F7;
    selection-color: white;
}
QPushButton {
    background-color: #2F81F7;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #1F6FEB;
}
QPushButton:pressed {
    background-color: #1158C7;
}
QPushButton:disabled {
    background-color: #3B424A;
    color: #9AA4AF;
}
QCheckBox {
    spacing: 8px;
    color: #DCE6F2;
}
QTabWidget::pane {
    border: 1px solid #30363D;
    border-radius: 10px;
    background-color: #101418;
}
QTabBar::tab {
    background: #161B22;
    color: #C9D1D9;
    padding: 8px 14px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}
QTabBar::tab:selected {
    background: #2F81F7;
    color: white;
}
QHeaderView::section {
    background-color: #1C2128;
    color: #F0F6FC;
    border: 1px solid #30363D;
    padding: 8px;
    font-weight: 600;
}
QTableWidget {
    gridline-color: #30363D;
}
"""

LIGHT_THEME = """
QMainWindow, QWidget {
    background-color: #F8FAFC;
    color: #0F172A;
    font-size: 13px;
    font-family: Arial;
}
QLabel {
    color: #0F172A;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox, QTableWidget {
    background-color: #FFFFFF;
    color: #0F172A;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    padding: 6px;
    selection-background-color: #2563EB;
    selection-color: white;
}
QPushButton {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #1D4ED8;
}
QPushButton:pressed {
    background-color: #1E40AF;
}
QPushButton:disabled {
    background-color: #94A3B8;
    color: #E2E8F0;
}
QCheckBox {
    spacing: 8px;
    color: #0F172A;
}
QTabWidget::pane {
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    background-color: #F8FAFC;
}
QTabBar::tab {
    background: #E2E8F0;
    color: #0F172A;
    padding: 8px 14px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}
QTabBar::tab:selected {
    background: #2563EB;
    color: white;
}
QHeaderView::section {
    background-color: #E2E8F0;
    color: #0F172A;
    border: 1px solid #CBD5E1;
    padding: 8px;
    font-weight: 600;
}
QTableWidget {
    gridline-color: #CBD5E1;
}
"""


def main() -> None:
    init_db()

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)

    window = AuthWindow(app=app, dark_theme=DARK_THEME, light_theme=LIGHT_THEME)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()