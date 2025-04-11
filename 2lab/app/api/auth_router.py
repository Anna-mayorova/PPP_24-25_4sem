from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.cruds.user_crud import create_user, get_user_by_email
from app.services.auth_service import create_access_token
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.db.session import get_db
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/sign-up/", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user.email, user.password)
    token = create_access_token({"sub": new_user.email})
    return {"id": new_user.id, "email": new_user.email, "token": token}


@router.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return {"id": db_user.id, "email": db_user.email, "token": token}


@router.get("/users/me/", response_model=UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = get_user_by_email(db, payload.get("sub"))
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": db_user.id, "email": db_user.email}