import os
import sqlite3

class MigrationManager:
    def __init__(self, migrations_dir="migrations", db_path="kerbian.db"):
        self.migrations_dir = migrations_dir
        self.db_path = db_path
        os.makedirs(migrations_dir, exist_ok=True)
        self._ensure_migrations_table()

    def _ensure_migrations_table(self):
        with sqlite3.connect(self.db_path) as c:
            c.execute("CREATE TABLE IF NOT EXISTS migrations (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
            c.commit()

    def applied_migrations(self):
        with sqlite3.connect(self.db_path) as c:
            c.execute("SELECT name FROM migrations")
            return {row[0] for row in c.fetchall()}

    def migrate(self):
        applied = self.applied_migrations()
        for fname in sorted(os.listdir(self.migrations_dir)):
            if fname.endswith(".sql") and fname not in applied:
                with open(os.path.join(self.migrations_dir, fname)) as f:
                    sql = f.read()
                with sqlite3.connect(self.db_path) as c:
                    c.executescript(sql)
                    c.execute("INSERT INTO migrations (name) VALUES (?)", (fname,))
                    c.commit()
                print(f"Applied migration: {fname}")