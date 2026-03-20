from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTabWidget

from app.services.auth_service import AuthService
from app.ui.login_widget import LoginWidget
from app.ui.main_window import MainWindow
from app.ui.register_widget import RegisterWidget


class AuthWindow(QMainWindow):
    def __init__(self, app, dark_theme: str, light_theme: str) -> None:
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.resize(420, 260)

        self.app = app
        self.dark_theme = dark_theme
        self.light_theme = light_theme
        self.auth_service = AuthService()
        self.main_window = None

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        self.tabs = QTabWidget()

        self.login_widget = LoginWidget()
        self.register_widget = RegisterWidget()

        self.tabs.addTab(self.login_widget, "Вход")
        self.tabs.addTab(self.register_widget, "Регистрация")

        layout.addWidget(self.tabs)

        self.login_widget.login_button.clicked.connect(self.handle_login)
        self.register_widget.register_button.clicked.connect(self.handle_register)

    def handle_login(self) -> None:
        username = self.login_widget.username_input.text()
        password = self.login_widget.password_input.text()

        ok, message = self.auth_service.authenticate(username, password)
        self.login_widget.message_label.setText(message)

        if ok:
            self.main_window = MainWindow(
                current_user=username,
                app=self.app,
                dark_theme=self.dark_theme,
                light_theme=self.light_theme,
            )
            self.main_window.show()
            self.close()

    def handle_register(self) -> None:
        username = self.register_widget.username_input.text()
        password = self.register_widget.password_input.text()
        confirm_password = self.register_widget.confirm_password_input.text()

        if password != confirm_password:
            self.register_widget.message_label.setText("Пароли не совпадают.")
            return

        ok, message = self.auth_service.register_user(username, password)
        self.register_widget.message_label.setText(message)

        if ok:
            self.tabs.setCurrentIndex(0)
            self.login_widget.username_input.setText(username)