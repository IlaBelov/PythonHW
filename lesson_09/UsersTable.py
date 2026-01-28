from sqlalchemy import create_engine
from sqlalchemy.sql import text


class UserTable:
    __scripts = {
        "select": text("SELECT * FROM users WHERE user_id = :user_id"),
        "select_all": text("SELECT * FROM users"),
        "insert": text("""
            INSERT INTO users (user_id, user_email, subject_id)
            VALUES (:user_id, :user_email, :subject_id)
        """),
        "update": text("""
            UPDATE users
            SET user_email = :user_email, subject_id = :subject_id
            WHERE user_id = :user_id
        """),
        "delete": text("DELETE FROM users WHERE user_id = :user_id"),
        "delete_all": text("DELETE FROM users"),
        "count": text("SELECT COUNT(*) FROM users"),
        "select_by_email": text(
            "SELECT * FROM users WHERE user_email = :user_email"),
        "check_exists": text(
            "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = :user_id)")
    }

    def __init__(self, connection_string):
        self.__db = create_engine(
            connection_string,
            pool_pre_ping=True,
            echo=False
        )
        self._test_connection()

    def _test_connection(self):
        try:
            with self.__db.connect() as conn:
                conn.execute("SELECT 1")
        except Exception as e:
            raise ConnectionError(
                f"Не удалось подключиться к базе данных: {e}")

    def create(self, user_id: int, user_email: str, subject_id: int):
        if self.check_exists(user_id):
            raise ValueError(f"Пользователь user_id={user_id} уже существует")

        with self.__db.connect() as conn:
            try:
                result = conn.execute(self.__scripts["insert"], {
                    "user_id": user_id,
                    "user_email": user_email,
                    "subject_id": subject_id
                })
                conn.execute("COMMIT")
                return result.rowcount
            except Exception as e:
                # Откат транзакции при ошибке
                conn.execute("ROLLBACK")
                raise e

    def get(self, user_id: int):
        """Получение пользователя по ID"""
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["select"], {"user_id":
                                                             user_id})
            # В SQLAlchemy 1.4 fetchone() возвращает RowProxy или None
            row = result.fetchone()
            return row

    def get_all(self):
        """Получение всех пользователей"""
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["select_all"])
            # В SQLAlchemy 1.4 fetchall() возвращает список RowProxy
            rows = result.fetchall()
            return rows

    def update(self, user_id: int, user_email: str, subject_id: int):
        """Обновление данных пользователя"""
        # Проверка существования пользователя перед обновлением
        if not self.check_exists(user_id):
            raise ValueError(f"Пользователь с user_id={user_id} не найден")

        with self.__db.connect() as conn:
            try:
                result = conn.execute(self.__scripts["update"], {
                    "user_id": user_id,
                    "user_email": user_email,
                    "subject_id": subject_id
                })
                conn.execute("COMMIT")
                return result.rowcount
            except Exception as e:
                conn.execute("ROLLBACK")
                raise e

    def delete(self, user_id: int):
        """Удаление пользователя по ID"""
        # Проверка существования пользователя перед удалением
        if not self.check_exists(user_id):
            raise ValueError(f"Пользователь с user_id={user_id} не найден")

        with self.__db.connect() as conn:
            try:
                result = conn.execute(self.__scripts["delete"], {"user_id":
                                                                 user_id})
                conn.execute("COMMIT")
                return result.rowcount
            except Exception as e:
                conn.execute("ROLLBACK")
                raise e

    def delete_all(self):
        """Удаление всех пользователей (очистка таблицы)"""
        with self.__db.connect() as conn:
            try:
                result = conn.execute(self.__scripts["delete_all"])
                conn.execute("COMMIT")
                return result.rowcount
            except Exception as e:
                conn.execute("ROLLBACK")
                raise e

    def count(self):
        """Получение количества пользователей в таблице"""
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["count"])
            count_row = result.fetchone()
            return count_row[0] if count_row else 0

    def get_by_email(self, user_email: str):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["select_by_email"],
                                  {"user_email": user_email})
            rows = result.fetchall()
            return rows

    def check_exists(self, user_id: int):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["check_exists"], {"user_id":
                                                                   user_id})
            exists_row = result.fetchone()
            return exists_row[0] if exists_row else False

    def create_batch(self, users_data):
        with self.__db.connect() as conn:
            try:
                rows_affected = 0
                for user_id, user_email, subject_id in users_data:
                    if not self.check_exists(user_id):
                        result = conn.execute(self.__scripts["insert"], {
                            "user_id": user_id,
                            "user_email": user_email,
                            "subject_id": subject_id
                        })
                        rows_affected += result.rowcount
                conn.execute("COMMIT")
                return rows_affected
            except Exception as e:
                conn.execute("ROLLBACK")
                raise e

    def get_user_as_dict(self, user_id: int):
        row = self.get(user_id)
        if row:
            return {
                'user_id': row[0],
                'user_email': row[1],
                'subject_id': row[2]
            }
        return None

    def get_all_as_dicts(self):
        rows = self.get_all()
        return [
            {
                'user_id': row[0],
                'user_email': row[1],
                'subject_id': row[2]
            }
            for row in rows
        ]

    def update_email(self, user_id: int, new_email: str):
        user = self.get(user_id)
        if not user:
            raise ValueError(f"Пользователь с user_id={user_id} не найден")

        current_subject_id = user[2]
        return self.update(user_id, new_email, current_subject_id)

    def update_subject(self, user_id: int, new_subject_id: int):
        user = self.get(user_id)
        if not user:
            raise ValueError(f"Пользователь с user_id={user_id} не найден")

        current_email = user[1]
        return self.update(user_id, current_email, new_subject_id)

    def search_users(self, email_pattern=None, min_subject_id=None,
                     max_subject_id=None):
        base_query = "SELECT * FROM users WHERE 1=1"
        params = {}

        if email_pattern:
            base_query += " AND user_email LIKE :email_pattern"
            params['email_pattern'] = f"%{email_pattern}%"

        if min_subject_id is not None:
            base_query += " AND subject_id >= :min_subject_id"
            params['min_subject_id'] = min_subject_id

        if max_subject_id is not None:
            base_query += " AND subject_id <= :max_subject_id"
            params['max_subject_id'] = max_subject_id

        search_script = text(base_query)

        with self.__db.connect() as conn:
            result = conn.execute(search_script, params)
            return result.fetchall()
