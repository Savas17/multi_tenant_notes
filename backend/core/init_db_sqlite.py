from core.database_sqlite import engine, Base
from models.user_sqlite import User
from models.note_sqlite import Note
from models.tenant_sqlite import Tenant

# Create tables
Base.metadata.create_all(bind=engine)
