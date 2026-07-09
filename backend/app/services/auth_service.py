from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

def create_user(db:Session, data):
    
    existing_username = db.query(User).filter(User.username == data.username).first() 

    existing_email = db.query(User).filter(User.email == data.email).first() 

    if existing_username:
        raise HTTPException(status_code=404, detail="Username already exist!")
    
    if existing_email:
        raise HTTPException(status_code=404, detail="Email already exist!")

    new_user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    data = {"message":"User registered successfully!"}

    return data

def check_user(db:Session, data):

    existing_user = (
        db.query(User)
        .filter(User.email == data.email).first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )
    
    if not verify_password(data.password, existing_user.password): # type: ignore
    
        raise HTTPException(
        status_code=401,
        detail="Invalid password"
    )

    user_details = {
        "sub": existing_user.email,
        "username": existing_user.username
    }

    token = create_access_token(user_details)

    data = {
        "message": "Login Successfull!",
        "access_token": token,
        "token_type": "bearer"
    }

    return data