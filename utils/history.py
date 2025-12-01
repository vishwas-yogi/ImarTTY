import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional

class HistoryManager:
    def __init__(self, db_path: str = "history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                exit_code INTEGER,
                output_snippet TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_entry(self, command: str, exit_code: int = 0, output_snippet: str = ""):
        """Add a new command entry to history."""
        if not command.strip():
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (command, exit_code, output_snippet) VALUES (?, ?, ?)",
            (command, exit_code, output_snippet)
        )
        conn.commit()
        conn.close()

    def get_recent(self, limit: int = 50) -> List[Tuple[int, str, str, int]]:
        """Get recent commands."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, command, timestamp, exit_code FROM history ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def search(self, query: str) -> List[Tuple[int, str, str, int]]:
        """Search history for a command."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, command, timestamp, exit_code FROM history WHERE command LIKE ? ORDER BY id DESC LIMIT 20",
            (f"%{query}%",)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows
