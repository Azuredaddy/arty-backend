from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Base

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS for all origins (or restrict to your frontend if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request schema
class UserCreate(BaseModel):
    email: str
    tenant_id: str

# Create user endpoint
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(email=user.email, tenant_id=user.tenant_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "user": {"email": new_user.email, "tenant_id": new_user.tenant_id}}

# List all users
@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Delete all users under a tenant
@app.delete("/tenants/{tenant_id}")
def delete_tenant(tenant_id: str, db: Session = Depends(get_db)):
    deleted = db.query(User).filter(User.tenant_id == tenant_id).delete()
    db.commit()
    return {"message": f"Deleted {deleted} user(s) under tenant {tenant_id}"}

# Group users by tenant
@app.get("/tenants/")
def list_tenants(db: Session = Depends(get_db)):
    users = db.query(User).all()
    grouped = {}
    for user in users:
        grouped.setdefault(user.tenant_id, []).append(user.email)
    return grouped




