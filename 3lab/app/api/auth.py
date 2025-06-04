from fastapi import APIRouter, HTTPException, status, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
# auth.py
#from .database import get_user_by_email  # на вскякий случай чтобы норм работали импорты с точками
#from .models import User
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.Graphs import GraphInput, Graph, ACO
from app.schemas.user import UserMeResponse,UserResponse,UserCreate
from app.models.models import User

from fastapi import WebSocket, APIRouter, Depends
from app.websocket.manager import manager

from app.models.models import User

from celery import chain
from app.celery.tasks import tsp_task
from celery.result import AsyncResult
from fastapi import BackgroundTasks

pwd_ctx = CryptContext(schemes=["bcrypt"])
SECRET = "kLq9!pR4$zX2@vN7"
ALGO = "HS256"
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjNAZ21haWwuY29tIiwiZXhwIjoxNzUwMTkxMTQyfQ.nuoG472rgq5mLS9g2zvdgdSEijT-tvAu0UblJkMBYXo'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")
payload = jwt.decode(token, SECRET, algorithms=[ALGO])

router = APIRouter(prefix="/ws", tags=["WebSocket"])
auth_router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
async def get_current_user(
    db: Session = Depends(get_db)
):
    print('rhfjekdol')
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])

        email = payload.get("sub")  # Исправлено на "sub"
        user_id = payload.get("user_id")
        if not email:
        #if not user_id:
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")
    #user = get_user_by_email(db, email)
    user = db.query(User).order_by(User.id.desc()).first()
    print('Ykfeookef')
    if not user:
        raise HTTPException(401, "User not found")
    return user
'''
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
'''
@router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket, current_user: User = Depends(get_current_user)):
    await manager.connect(websocket, current_user.email)
    try:
        while True:
            data = await websocket.receive_text()
            # Можно добавить обработку команд
            pass
    except:
        manager.disconnect(websocket, current_user.email)
'''
# app/api/auth.py

@router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    # Проверка токена
    payload = jwt.decode(token, SECRET, algorithms=[ALGO])
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        await websocket.close(code=4001)
        return

    await manager.connect(websocket, user.email)
    try:
        while True:
            data = await websocket.receive_text()

    except Exception:
        manager.disconnect(websocket, user.email)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def hash_pwd(p):
    return pwd_ctx.hash(p)


def verify_pwd(p, h):
    return pwd_ctx.verify(p, h)


def create_jwt(d):
    exp = datetime.utcnow() + timedelta(days=69)
    return jwt.encode({**d, "exp": exp}, SECRET, algorithm=ALGO)

@auth_router.get('/all_users')
async def allusers(db: Session = Depends(get_db)):
    return db.query(User).all()

@auth_router.get("/users/me/", response_model=UserMeResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@auth_router.post("/sign-up/", response_model=UserResponse)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(400, "Email exists")

    hashed = hash_pwd(data.password)
    new_user = User(email=data.email, password_hash=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_jwt({"sub": new_user.email})
    #return {"id": new_user.id, "email": new_user.email, "token": token}
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        token=token
    )

@auth_router.get('/sub/')
async def sub():
    payload = jwt.decode(token, SECRET, algorithms=[ALGO])

    return payload

@auth_router.post("/login/", response_model=UserResponse)
def login(data: UserCreate, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == data.email).first()
    if not u or not verify_pwd(data.password, u.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tkn = create_jwt({"sub": u.email})
    # return {"id": u.id, "email": u.email, "token": tkn}
    return UserResponse(
        id=u.id,
        email=u.email,
        token=tkn
    )


@auth_router.post("/shortest-path/")
async def shortest_path(graph_input: GraphInput, background_tasks: BackgroundTasks):
    task = tsp_task.delay(graph_input.nodes, graph_input.edges)
    return {"task_id": task.id}