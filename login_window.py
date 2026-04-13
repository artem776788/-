from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from src.auth import AuthManager
from ui.styles import LOGIN_STYLE


class LoginWindow(QDialog):

    def __init__(self, auth_manager: AuthManager):
        super().__init__()
        self.auth_manager = auth_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Авторизация - Сервисный центр")
        self.setFixedSize(400, 380)
        self.setStyleSheet(LOGIN_STYLE)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        title_label = QLabel("Вход в систему")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title_label)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.login_input.setFixedHeight(40)
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Войти")
        login_button.setFixedHeight(40)
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        info_label = QLabel("Тестовые учетные записи:\n\n"
                            "Администратор: admin / admin123\n"
                            "Менеджер: kasoo / root\n"
                            "Мастер: murashov123 / qwerty\n"
                            "Оператор: perinaAD / 250519\n"
                            "Заказчик: login2 / pass2")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 11px; margin-top: 20px;")
        layout.addWidget(info_label)

        self.setLayout(layout)

    def handle_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
            return

        if self.auth_manager.login(login, password):
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль!")
            self.password_input.clear()