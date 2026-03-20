from __future__ import annotations

from app.db import get_connection
from app.utils import generate_salt, hash_password, utc_now_iso, verify_password


class AuthService:
    def register_user(self, username: str, password: str) -> tuple[bool, str]:
        username = username.strip()
        password = password.strip()

        if len(username) < 3:
            return False, "Логин должен быть не короче 3 символов."

        if len(password) < 6:
            return False, "Пароль должен быть не короче 6 символов."

        conn = get_connection()
        try:
            existing = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                (username,),
            ).fetchone()

            if existing:
                return False, "Пользователь с таким логином уже существует."

            salt = generate_salt()
            password_hash = hash_password(password, salt)

            conn.execute(
                """
                INSERT INTO users (username, password_hash, salt, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (username, password_hash, salt, utc_now_iso()),
            )
            conn.commit()
            return True, "Регистрация прошла успешно."
        finally:
            conn.close()

    def authenticate(self, username: str, password: str) -> tuple[bool, str]:
        username = username.strip()
        password = password.strip()

        conn = get_connection()
        try:
            row = conn.execute(
                """
                SELECT username, password_hash, salt
                FROM users
                WHERE username = ?
                """,
                (username,),
            ).fetchone()

            if row is None:
                return False, "Пользователь не найден."

            if not verify_password(password, row["salt"], row["password_hash"]):
                return False, "Неверный пароль."

            return True, f"Добро пожаловать, {row['username']}."
        finally:
            conn.close()
