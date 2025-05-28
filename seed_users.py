from models import SessionLocal, User, init_db

init_db()
db = SessionLocal()

# Add demo users
users = [
    User(email="user@company1.com", tenant_id="tenant_company1"),
    User(email="admin@org2.io", tenant_id="tenant_org2"),
     User(email="bill.bridle39@gmail.com", tenant_id="tenant_org22"),
]

db.add_all(users)
db.commit()
db.close()

print("✅ Demo users seeded.")
