from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from models import init_db, SessionLocal, User

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/resolve-tenant")
def resolve_tenant(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "Tenant not found"})
    return { "tenant_id": user.tenant_id }

