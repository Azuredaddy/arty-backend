from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Arty Backend is Live"}

@app.post("/api/add-user")
def add_user(user: dict, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user["email"]).first()
    if existing:
        return JSONResponse(status_code=400, content={"message": "User already exists"})
    new_user = User(email=user["email"], tenant_id=user["tenant_id"])
    db.add(new_user)
    db.commit()
    return {"message": "User added"}

@app.get("/api/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    return {
        "tickets": 120,
        "accuracy": "91%",
        "most_performed_task": "Password Reset",
        "average_time_per_task": "12s",
        "training_tasks": 5,
    }

