import sqlite3
from datetime import datetime
from contextlib import contextmanager


class MemoryStorage:
    def __init__(self, db_path: str = "conversations.db"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        """上下文管理数据库连接"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        """初始化数据库"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    input TEXT NOT NULL,
                    response TEXT NOT NULL
                )
            """)

    def save(self, user_input: str, response: str):
        """存储对话记录"""
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO history (input, response) VALUES (?, ?)",
                (user_input, response)
            )
            conn.commit()

    def query(self, keyword: str, limit: int = 5) -> list:
        """查询历史对话"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT timestamp, input, response FROM history WHERE input LIKE ? ORDER BY timestamp DESC LIMIT ?",
                (f"%{keyword}%", limit)
            )
            return cursor.fetchall()