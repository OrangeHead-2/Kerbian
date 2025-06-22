import threading

class DatabaseConnection:
    _instances = {}

    def __init__(self, db_type, **kwargs):
        self.db_type = db_type
        self.kwargs = kwargs
        self._connect()

    def _connect(self):
        if self.db_type == "sqlite":
            import sqlite3
            self.conn = sqlite3.connect(self.kwargs.get("path", ":memory:"), check_same_thread=False)
        elif self.db_type == "postgres":
            import psycopg2
            self.conn = psycopg2.connect(**self.kwargs)
        elif self.db_type == "firebase":
            from kerbian.db.providers.firebase import FirebaseConnection
            self.conn = FirebaseConnection(**self.kwargs)
        else:
            raise NotImplementedError(f"DB type {self.db_type} not supported.")

    @classmethod
    def get_instance(cls, key, db_type, **kwargs):
        if key not in cls._instances:
            cls._instances[key] = cls(db_type, **kwargs)
        return cls._instances[key]

    def cursor(self):
        if self.db_type in ["sqlite", "postgres"]:
            return self.conn.cursor()
        return self.conn.cursor()

    def commit(self):
        if hasattr(self.conn, "commit"):
            self.conn.commit()

    def close(self):
        self.conn.close()