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
import numpy
import base64


from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import or_

sys.path.append('../')

from database.redis_connector import get_redis_session
from database.db_connector import get_session
from schemas.CV import undendified_facesDB
from io import BytesIO
from fastapi.responses import StreamingResponse

class undef_faces:
    def __init__(self, session_db: Client = Depends(get_session),
                 session_redis: Redis = Depends(get_redis_session)):
        self.session_db = session_db
        self.session_redis = session_redis

    def _request_to_db(self, query: str) -> Session:
        return self.session_db.query(query)

    def _check_user_in_redis(self, user_id: int) -> bool:
        if self.session_redis.get(user_id):
            return True

    def get_limit(self,limit: int, user_id):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(undendified_facesDB.time, undendified_facesDB.cam_id).order_by(undendified_facesDB.time.desc()).limit(limit).all()

        ans = []

        for i in answer:
            abc = i
            ans.append({"time": str(i.time), "cam_id": i.cam_id, })


        return JSONResponse(content=ans, status_code=200)


    def get_by_timestamp(self, timestamp: str, user_id):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(undendified_facesDB).filter(undendified_facesDB.time==timestamp).order_by(undendified_facesDB.time.desc()).all()

        ans = []

        for i in answer:
            abc = i
            ans.append({"cam_id": i.cam_id, "file": str(i.file)})

        sas = StreamingResponse(BytesIO(answer[0].file), media_type="image/png")
        return sas


        return JSONResponse(content={"ans":ans}, status_code=200)
