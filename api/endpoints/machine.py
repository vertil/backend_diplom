from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import sys

sys.path.append('../')


from service.machine import Machine
from models.user import User
from service.auth import get_current_user

router = APIRouter(
    prefix='/machine',
    tags=['machine'],
)


@router.get('/')
async def machineinfo(
        id: int,
        service: Machine = Depends(),
        current_user: User = Depends(get_current_user)
):
    return service.get_info(id, current_user.id)

