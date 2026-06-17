
from fastapi import APIRouter, HTTPException, Response, Request
from src.schemas.users import UserRequestAdd, UserAdd
from repositories.users import UsersRepository
from src.db import async_session_maker
from src.config import settings
from src.services.auth import AuthService


router = APIRouter(prefix='/auth', tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd, 
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd, 
    response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            return HTTPException(status_code=401, detail='Пользователь с таким email не зарегистирован')
        access_token = AuthService().create_access_token({"user_id" : user.id})
        if not AuthService().verify_password(data.password, user.hashed_password):
            return HTTPException(status_code=401, detail="Пароль неверный")
        response.set_cookies("access_token", access_token)
        return {"access_token" : access_token}
    

@router.get("/only_auth")
async def only_auth(
    request: Request,
):
    access_token = request.cookies.get("access_token", None)
  