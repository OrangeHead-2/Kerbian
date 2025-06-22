from kerbian.db.connection import DatabaseConnection
from kerbian.db.models.user import User

conn = DatabaseConnection.get_instance("default", "sqlite", path="kerbian.db").conn
User.create_table(conn)
user = User()
user.id = 1
user.username = "jane"
user.email = "jane@kerbian.app"
user.save(conn)
print(User.all(conn))