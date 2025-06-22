import aiosqlite

class AsyncDatabaseConnection:
    _instances = {}

    def __init__(self, path="kerbian.db"):
        self.path = path

    @classmethod
    async def get_instance(cls, key, path="kerbian.db"):
        if key not in cls._instances:
            conn = await aiosqlite.connect(path)
            cls._instances[key] = conn
        return cls._instances[key]