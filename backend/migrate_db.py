from app import app
from alembic.config import Config
from alembic import command

def upgrade_database():
    alembic_cfg = Config("./migrations/alembic.ini")
    
    # Generate a new migration file
    with app.app_context():
        command.revision(alembic_cfg, autogenerate=True, message="Updating models")
        
        # Upgrade the database schema to match the SQLAlchemy models
        command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    upgrade_database()
