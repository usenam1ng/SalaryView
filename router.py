import typing
from schemas import SUser, SUserId, SUserAdd, SToken
from fastapi import Depends, APIRouter, HTTPException, status
from repo import UserRepository
from auth import verify_password, create_access_token, decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

bearer_scheme = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/register", response_model=SUserId)
async def register(user: SUserAdd):
    existing = await UserRepository.get_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    user_id = await UserRepository.add_one(user)
    return {"ok": True, "user_id": user_id}

@router.post("/login", response_model=SToken, tags=["users"])
async def login_json(data: LoginRequest):
    user = await UserRepository.get_by_username(data.username)
    if not user or not verify_password(data.password, user.password): 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя или пароль")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен авторизации")
    user = await UserRepository.get_by_id(int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    return user

@router.get("/me/salary", response_model=SUser)
async def get_my_salary(current_user = Depends(get_current_user)):
    return SUser(
        id=current_user.id,
        username=current_user.username,
        salary=current_user.salary,
        update_salary_at=current_user.update_salary_at
    )