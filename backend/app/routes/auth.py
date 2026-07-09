from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import UserCreate, UserLogin
from app.services.auth_service import create_user, check_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(
    payload: UserCreate,
    db:Session = Depends(get_db)
):
    return create_user(db,payload)

@router.post("/login")
def login(
    payload:UserLogin,
    db:Session =Depends(get_db)
):
    return check_user(db,payload)



