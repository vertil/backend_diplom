from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import sys

from service.departments import Departments
from models.user import User
from service.auth import get_current_user

router = APIRouter(
    prefix='/departments',
    tags=['departments'],
)


@router.get('/all_deps')
async def get_departments(
        service: Departments = Depends(),
        current_user: User = Depends(get_current_user)
):
    return service.get_all(current_user.id)
