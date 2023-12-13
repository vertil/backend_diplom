import sys
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


from models.user import UserCreate, User
from models.token import Token
from service.auth import AuthService, get_current_user




router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


#@router.post('/sign-up')
#async def sign_up(
#        user_data: UserCreate,
#        service: AuthService = Depends()
#):
#    return service.register_new_user(user_data)


@router.post('/sign-in', response_model=Token)
def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return service.authenticate_user(
        form_data.username,
        form_data.password,
    )


@router.post("/logout")
def logout_user(
        current_user: User = Depends(get_current_user),
        service: AuthService = Depends(),
):
    return service.logout_user(current_user)


@router.get('/userinfo', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user
