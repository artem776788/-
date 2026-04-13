from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QComboBox, QPushButton,
                             QFormLayout, QGroupBox, QListWidget, QMessageBox,
                             QDateEdit)
from PyQt5.QtCore import QDate
from src.database import Database
from src.auth import AuthManager
from datetime import date


class RequestWindow(QDialog):

    def __init__(self, db: Database, request_id: int, auth_manager: AuthManager):
        super().__init__()
        self.db = db
        self.request_id = request_id
        self.auth_manager = auth_manager
        self.user_role = auth_manager.get_current_user_role()
        self.user_id = auth_manager.get_current_user_id()
        self.init_ui()

        if request_id:
            self.load_request_data()
            self.setWindowTitle(f"Редактирование заявки N{request_id}")
        else:
            self.setWindowTitle("Новая заявка")

    def init_ui(self):
        self.setFixedSize(600, 700)

        layout = QVBoxLayout()

        form_group = QGroupBox("Информация о заявке")
        form_layout = QFormLayout()

        self.tech_type_input = QLineEdit()
        self.tech_model_input = QLineEdit()
        self.problem_input = QTextEdit()

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Новая заявка", "В процессе ремонта",
                                    "Готова к выдаче", "Ожидание запчастей"])

        if self.user_role not in ['Менеджер', 'Мастер']:
            self.status_combo.setEnabled(False)

        self.master_combo = QComboBox()
        masters = self.db.get_masters()
        self.master_combo.addItem("Не назначен", None)
        for master in masters:
            self.master_combo.addItem(master['fio'], master['userid'])

        if self.user_role != 'Менеджер':
            self.master_combo.setEnabled(False)

        self.repair_parts = QTextEdit()
        self.repair_parts.setPlaceholderText("Укажите использованные запчасти...")

        if self.user_role not in ['Менеджер', 'Мастер']:
            self.repair_parts.setEnabled(False)

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        if self.request_id:
            self.date_input.setEnabled(False)

        form_layout.addRow("Тип техники:", self.tech_type_input)
        form_layout.addRow("Модель:", self.tech_model_input)
        form_layout.addRow("Описание проблемы:", self.problem_input)

        if self.user_role in ['Менеджер', 'Мастер', 'Оператор']:
            form_layout.addRow("Статус:", self.status_combo)

        if self.user_role == 'Менеджер':
            form_layout.addRow("Ответственный мастер:", self.master_combo)

        if self.user_role in ['Менеджер', 'Мастер']:
            form_layout.addRow("Использованные запчасти:", self.repair_parts)

        form_layout.addRow("Дата создания:", self.date_input)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        if self.request_id and self.user_role in ['Мастер', 'Менеджер']:
            comments_group = QGroupBox("Комментарии мастера")
            comments_layout = QVBoxLayout()

            self.comments_list = QListWidget()
            comments_layout.addWidget(self.comments_list)

            self.new_comment = QTextEdit()
            self.new_comment.setPlaceholderText("Добавить комментарий...")
            self.new_comment.setMaximumHeight(80)
            comments_layout.addWidget(self.new_comment)

            add_comment_btn = QPushButton("Добавить комментарий")
            add_comment_btn.clicked.connect(self.add_comment)
            comments_layout.addWidget(add_comment_btn)

            comments_group.setLayout(comments_layout)
            layout.addWidget(comments_group)

        buttons_layout = QHBoxLayout()

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_request)
        buttons_layout.addWidget(save_button)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def load_request_data(self):
        request = self.db.get_request_by_id(self.request_id)
        if request:
            self.tech_type_input.setText(request['hometechtype'])
            self.tech_model_input.setText(request['hometechmodel'])
            self.problem_input.setText(request['problemdescryption'])

            if self.user_role in ['Менеджер', 'Мастер', 'Оператор']:
                self.status_combo.setCurrentText(request['requeststatus'])

            if self.user_role in ['Менеджер', 'Мастер']:
                self.repair_parts.setText(request['repairparts'] or "")

            self.date_input.setDate(QDate.fromString(str(request['startdate']), "yyyy-MM-dd"))

            if self.user_role == 'Менеджер' and request['masterid']:
                index = self.master_combo.findData(request['masterid'])
                if index >= 0:
                    self.master_combo.setCurrentIndex(index)

        if self.user_role in ['Мастер', 'Менеджер']:
            self.load_comments()

    def load_comments(self):
        comments = self.db.get_comments(self.request_id)
        self.comments_list.clear()
        for comment in comments:
            self.comments_list.addItem(f"[{comment['mastername']}]: {comment['message']}")

    def add_comment(self):
        message = self.new_comment.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Ошибка", "Введите текст комментария!")
            return

        self.db.add_comment(message, self.user_id, self.request_id)
        self.load_comments()
        self.new_comment.clear()
        QMessageBox.information(self, "Успех", "Комментарий добавлен")

    def save_request(self):
        if not self.tech_type_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите тип техники!")
            return

        if not self.tech_model_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите модель техники!")
            return

        if not self.problem_input.toPlainText().strip():
            QMessageBox.warning(self, "Ошибка", "Введите описание проблемы!")
            return

        old_status = None
        if self.request_id:
            request = self.db.get_request_by_id(self.request_id)
            if request:
                old_status = request['requeststatus']

        if self.request_id:
            completion = None
            new_status = self.status_combo.currentText() if self.user_role in ['Менеджер', 'Мастер',
                                                                               'Оператор'] else None

            if new_status == "Готова к выдаче":
                completion = str(date.today())

            if new_status:
                self.db.update_request_status(
                    self.request_id,
                    new_status,
                    completion,
                    self.repair_parts.toPlainText() if self.user_role in ['Менеджер', 'Мастер'] else None
                )

            if old_status and new_status and old_status != new_status:
                QMessageBox.information(self, "Уведомление",
                                        f"Статус заявки N{self.request_id} изменен с '{old_status}' на '{new_status}'")

            if self.user_role == 'Менеджер':
                master_id = self.master_combo.currentData()
                if master_id:
                    self.db.assign_master(self.request_id, master_id)
        else:
            new_id = self.db.create_new_request(
                self.user_id,
                self.tech_type_input.text(),
                self.tech_model_input.text(),
                self.problem_input.toPlainText(),
                str(self.date_input.date().toPyDate())
            )
            if not new_id:
                QMessageBox.critical(self, "Ошибка", "Не удалось создать заявку!")
                return
            QMessageBox.information(self, "Уведомление", f"Создана новая заявка N{new_id}")

        self.accept()