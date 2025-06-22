import click
from kerbian.db.connection import DatabaseConnection

@click.group()
def db():
    """Database management commands."""

@db.command()
@click.option('--db-type', type=click.Choice(['sqlite', 'postgres', 'firebase']), default='sqlite')
@click.option('--path', default='kerbian.db')
def init(db_type, path):
    """Initialize a database."""
    conn = DatabaseConnection.get_instance("default", db_type, path=path)
    print(f"Initialized {db_type} database at {path}")

@db.command()
def migrate():
    """Run model migrations (create tables)."""
    from kerbian.db.models import user  # import all model modules
    conn = DatabaseConnection.get_instance("default", "sqlite", path="kerbian.db").conn
    user.User.create_table(conn)
    print("Migrations complete.")

@db.command()
def seed():
    """Add sample data."""
    from kerbian.db.models.user import User
    conn = DatabaseConnection.get_instance("default", "sqlite", path="kerbian.db").conn
    u = User()
    u.id = 1
    u.username = "admin"
    u.email = "admin@kerbian.dev"
    u.save(conn)
    print("Seeded database.")