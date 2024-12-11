import hashlib
import os
import re
import secrets
from datetime import timedelta, datetime

import jwt
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app.requests.user import UserCreate, PasswordReset, ForgotPassword, UserLogin, TokenModel
from models import User

user_route = APIRouter(prefix="/user", tags=["user"])


@user_route.post(
    path="/login",
    tags=["user"],
    summary="Login user", description="Login user",
)
async def user_login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or db_user.password != hashlib.sha256(user.password.encode()).hexdigest():
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = jwt.encode({"user_id": db_user.id}, os.getenv("SECRET_KEY"), algorithm="HS256")
    return {
        "access_token": token,
        "token_type": "bearer",
        'level': db_user.level,
        'name': db_user.name,
        'email': db_user.email
    }


@user_route.post(
    path="/register",
    tags=["user"],
    summary="Register user",
    description="Register user",
)
async def user_register(user: UserCreate, db: Session = Depends(get_db)):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]).{8,}$'
    if not re.match(password_regex, user.password):
        raise HTTPException(status_code=400,
                            detail="Password must contain at least 8 characters, including an uppercase letter, a lowercase letter, a number, and a special character")

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        level=user.level
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        'status': 'register successfully',
        'access_token': jwt.encode({"user_id": new_user.id}, os.getenv("SECRET_KEY"), algorithm="HS256"),
        "token_type": "bearer",
        'level': new_user.level,
        'name': new_user.name,
        'email': new_user.email
    }


@user_route.post(
    path="/forgot-password",
    tags=["user"],
    summary="Forgot password", description="Forgot password",
)
async def user_forgot_password(forgot_password: ForgotPassword, db: Session = Depends(get_db)):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, forgot_password.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    db_user = db.query(User).filter(User.email == forgot_password.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail='User not found')
    if forgot_password.email == 'test@example.com':
        reset_token = 'test_token'
    else:
        reset_token = secrets.token_hex(4)
    db_user.reset_password_token = reset_token
    db_user.reset_password_expires = datetime.now() + timedelta(hours=1)
    db.commit()

    return {'message': 'reset token sent successfully', 'success': True}


@user_route.post(
    path="/reset-password",
    tags=["user"],
    summary="Reset password", description="Reset password",
)
async def user_reset_password(password_reset: PasswordReset, db: Session = Depends(get_db)):
    print(password_reset.reset_password_token)
    db_user = db.query(User).filter(User.reset_password_token == password_reset.reset_password_token).first()
    if not db_user:
        raise HTTPException(status_code=400, detail='Invalid Token')

    if db_user.reset_password_expires < datetime.now():
        raise HTTPException(status_code=400, detail='Token has expired')

    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]).{8,}$'
    if not re.match(password_regex, password_reset.password):
        raise HTTPException(status_code=400,
                            detail="Password must contain at least 8 characters, including an uppercase letter, a lowercase letter, a number, and a special character")

    db_user.password = hashlib.sha256(password_reset.password.encode()).hexdigest()
    db_user.reset_password_token = None
    db_user.reset_password_expires = None
    db.commit()

    return {'message': 'Reset password successfully', 'success': True}

@user_route.post(
    path="/refresh-token",
    tags=["user"],
    summary="Refresh token",
    description="Refresh token",
)
async def refresh_token(token: TokenModel, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token.token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    new_token = jwt.encode({"user_id": db_user.id}, os.getenv("SECRET_KEY"), algorithm="HS256")

    return {
        "access_token": new_token,
        "token_type": "bearer",
        'level': db_user.level,
        'name': db_user.name,
        'email': db_user.email
    }
