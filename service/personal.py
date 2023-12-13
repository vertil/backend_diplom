import sys, logging

from clickhouse_connect.driver.client import Client
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from passlib.hash import bcrypt
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from redis import Redis
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
import re


from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import or_

sys.path.append('../')

from database.redis_connector import get_redis_session
from database.db_connector import get_session
from schemas.CV import personalDB


class Personal:
    def __init__(self, session_db: Client = Depends(get_session),
                 session_redis: Redis = Depends(get_redis_session)):
        self.session_db = session_db
        self.session_redis = session_redis

    def _request_to_db(self, query: str) -> Session:
        return self.session_db.query(query)

    def _check_user_in_redis(self, user_id: int) -> bool:
        if self.session_redis.get(user_id):
            return True

    def get_one(self, per_id: int, user_id: int,):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(personalDB).filter(personalDB.id == per_id).first()

        return JSONResponse(content=[jsonable_encoder(answer)], status_code=200)

    def get_all(self,user_id: int):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(personalDB).filter().all()

        return JSONResponse(content=[jsonable_encoder(answer)], status_code=200)

    def worker_day_visits(self,per_id: int,date: str,user_id):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(func.worker_day_visits("20231205", 1)).all()

        ans = []

        #answer = [tuple(row) for row in answer]

        for i in answer:
            mystr=i[0]
            mystr = mystr[1:-1].split(',')
            status = False
            if(mystr[2]=='t'):
                status=True
            mystr = {"datetime": mystr[0], "cab_id": int(mystr[1]), "direction": status}
            ans.append(mystr)

        # mystr = answer[0][0]
        # mystr=mystr[1:-1].split(',')
        # mystr={"datetime":mystr[0], "cab_id": int(mystr[1]), "direction": mystr[2]}
        # ans.append(mystr)
        # print(mystr)

        return JSONResponse(content=ans, status_code=200)


