from core.database_sqlite import SessionLocal
from models.user_sqlite import User
from models.tenant_sqlite import Tenant

def seed():
    db = SessionLocal()
    # Seed tenants
    tenants = [
        Tenant(id="acme", name="Acme Corp", plan="free"),
        Tenant(id="globex", name="Globex Ltd", plan="pro"),
    ]
    for tenant in tenants:
        if not db.query(Tenant).filter_by(id=tenant.id).first():
            db.add(tenant)
    db.commit()

    # Seed users
    users = [
        User(username="acmeAdmin", password="123", role="admin", tenant_id="acme"),
        User(username="acmeMember", password="123", role="member", tenant_id="acme"),
        User(username="globexAdmin", password="123", role="admin", tenant_id="globex"),
        User(username="globexMember", password="123", role="member", tenant_id="globex"),
    ]
    for user in users:
        if not db.query(User).filter_by(username=user.username).first():
            db.add(user)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
