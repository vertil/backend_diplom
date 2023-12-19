from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


import sys

from service.in_out_status import In_out_status
from models.user import User
from service.auth import get_current_user

router = APIRouter(
    prefix='/in_out_status',
    tags=['in_out_status'],
)

@router.get('/get_limit')
async def get_user(
        limit: int,
        service: In_out_status = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_limit(limit, current_user.id)