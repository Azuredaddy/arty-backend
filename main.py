from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from models import User, Base
from database import engine, SessionLocal

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request model
class UserCreate(BaseModel):
    email: str
    tenant_id: str

# POST endpoint to add a user
@app.post("/api/add-user")
def add_user(user: UserCreate):
    db = SessionLocal()
    existing = db.query(User).filter_by(email=user.email).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = User(email=user.email, tenant_id=user.tenant_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return {"message": "User added", "tenant_id": db_user.tenant_id}

# GET endpoint to list all tenants/users
@app.get("/api/tenants")
def list_tenants():
    db = SessionLocal()
    users = db.query(User).all()
    result = [{"email": u.email, "tenant_id": u.tenant_id} for u in users]
    db.close()
    return result

# Default route
@app.get("/")
def root():
    return {"status": "Arty backend is live"}


