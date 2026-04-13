from database import Database
from typing import Optional, Dict


class AuthManager:
    """Менеджер аутентификации пользователей"""

    def __init__(self, db: Database):
        self.db = db
        self.current_user: Optional[Dict] = None

    def login(self, login: str, password: str) -> bool:
        user = self.db.get_user_by_credentials(login, password)
        if user:
            self.current_user = user
            print(f"Вход выполнен: {user['fio']} ({user['type']})")
            return True
        print("Неверный логин или пароль")
        return False

    def logout(self):
        if self.current_user:
            print(f"Пользователь {self.current_user['fio']} вышел из системы")
        self.current_user = None

    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def get_current_user_role(self) -> Optional[str]:
        return self.current_user.get('type') if self.current_user else None

    def get_current_user_id(self) -> Optional[int]:
        return self.current_user.get('userid') if self.current_user else None

    def has_permission(self, required_roles: list) -> bool:
        if not self.current_user:
            return False
        return self.current_user.get('type') in required_roles