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
from schemas.CV import cabinetsDB, facesDB, personalDB


class Cabinets:
    def __init__(self, session_db: Client = Depends(get_session),
                 session_redis: Redis = Depends(get_redis_session)):
        self.session_db = session_db
        self.session_redis = session_redis

    def _request_to_db(self, query: str) -> Session:
        return self.session_db.query(query)

    def _check_user_in_redis(self, user_id: int) -> bool:
        if self.session_redis.get(user_id):
            return True

    def get_one(self, cab_id: int, user_id: int,):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(cabinetsDB).filter(cabinetsDB.id == cab_id).first()

        return JSONResponse(content=[jsonable_encoder(answer)], status_code=200)

    def get_all(self,user_id: int):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(cabinetsDB.id,cabinetsDB.name,cabinetsDB.floor,cabinetsDB.dep_id).filter().all()

        ans=[]
        for i in answer:
            mystr=i
            print(mystr)
            mystr = {"id": mystr[0], "name": mystr[1], "floor": int(mystr[2]), "dep_id": mystr[3]}
            ans.append(mystr)


        return JSONResponse(content=ans, status_code=200)

    def get_cabinet_per_ids(self,cab_id: int,user_id: int):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(cabinetsDB.pers_ids).filter(cabinetsDB.id == cab_id).all()

        ans=[]

        ans = {"pers_ids": answer[0][0]}

        return JSONResponse(content=ans, status_code=200)

    def cab_visits(self, cab_id: int, date: str, user_id):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(func.cab_visits(date, cab_id)).all()

        ans=[]

        pers_a = self.session_db.query(personalDB.id,personalDB.last_name,personalDB.first_name,personalDB.father_name,personalDB.work_cabs).filter().all()



        pers={}

        for i in pers_a:
            mystr = i
            pers[mystr[0]]= f"{mystr[1]} {mystr[2]} {mystr[3]}"
            #mystr = {"id": mystr[0], "name": mystr[1], "floor": int(mystr[2]), "dep_id": mystr[3]}


        pers_times=[]
        pos = 0
        for i in answer:

            #prepare data
            mystr=i[0]
            mystr = mystr[1:-1].split(',')
            status = False
            print(mystr)
            if (mystr[2] == 't'):
                status = True


            #CALCULATING TIME IN CABINETS------------------------------------------------------------------------

            test = datetime.strptime(mystr[0][1:-1],"%Y-%m-%d %H:%M:%S.%f")

            if (status == False and pos == 0):

                secondst = test.hour * 3600 + test.minute * 60 + test.second
                hour = {mystr[1]: secondst}
                pers_times.append(hour)

            elif (status == True and pos == len(answer) - 1):

                per_id = mystr[1]

                found = False

                for i in pers_times:
                    keyys = list(i.keys())
                    if(per_id in keyys):
                        found=True
                        oldtime = i[keyys[0]]
                        currtime = test.hour * 3600 + test.minute * 60 + test.second
                        newtime = (86400 - currtime) + oldtime

                        i[keyys[0]] = newtime

                if found==False:
                    secondst = test.hour * 3600 + test.minute * 60 + test.second
                    hour = {mystr[1]: 86400 - secondst}
                    pers_times.append(hour)

            else:
                per_id = mystr[1]

                found = False
                for i in pers_times:
                    keyys = list(i.keys())
                    if (per_id in keyys):
                        found = True
                        oldtime = i[keyys[0]]

                        currtime = test.hour * 3600 + test.minute * 60 + test.second
                        newtime = currtime - oldtime

                        i[keyys[0]] = newtime

                if found==False:
                    secondst = test.hour * 3600 + test.minute * 60 + test.second
                    hour = {mystr[1]: secondst}
                    pers_times.append(hour)

            #-------------------------------------------------------------------------------------------

            #change per_id to full name

            mystr = {"datetime": mystr[0], "name": pers[int(mystr[1])], "direction": status}
            ans.append(mystr)
            pos+=1


        #CALCULATE HOW MANY WORKERS AND NON WORKERS HAS BEN ----------------------


        #-------------------------------------------------------------------------
        buff=[]
        for i in pers_times:

            key_i=int(list(i.keys())[0])

            buff.append( {pers[key_i]: i[list(i.keys())[0]]} )

        pers_times=buff
        print(pers_times)
        short={"total persons": len(pers_times),  }
        ans={"pers_times": pers_times, "full":ans}

        return JSONResponse(content=ans, status_code=200)

    def cab_visits_pos(self, cab_id: int, date: str,pos_bool: bool, user_id):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(func.cab_visits_pos(date, cab_id, pos_bool)).all()

        ans = []

        pers = self.session_db.query(personalDB).filter().all()

        for i in answer:
            mystr = i[0]
            mystr = mystr[1:-1].split(',')

            for i in pers:
                if (i.id == int(mystr[1])):
                    per_name = f"{i.last_name} {i.first_name} {i.father_name}"
                    break

            mystr = {"datetime": mystr[0], "name": per_name}
            #mystr = {"datetime": mystr[0], "per_id": int(mystr[1])}
            ans.append(mystr)

        return JSONResponse(content=ans, status_code=200)

    def pass_visits(self, date: str, cab_id: int, pass_num: int, user_id):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(func.pass_visits(date, pass_num, cab_id)).all()

        ans = []

        pers = self.session_db.query(personalDB).filter().all()

        for i in answer:
            mystr=i[0]
            mystr = mystr[1:-1].split(',')
            status = False
            if(mystr[2]=='t'):
                status=True
            for i in pers:
                if (i.id == int(mystr[1])):
                    per_name = f"{i.last_name} {i.first_name} {i.father_name}"
                    break
            mystr = {"datetime": mystr[0], "name": per_name, "direction": status}
            #mystr = {"datetime": mystr[0], "per_id": int(mystr[1]), "direction": status}
            ans.append(mystr)

        return JSONResponse(content=ans, status_code=200)

    def pass_visits_pos(self, date: str, cab_id: int, pass_num: int,pos_bool: bool, user_id):
        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        answer = self.session_db.query(func.pass_visits_pos(date,pass_num, cab_id,pos_bool )).all()

        ans = []

        pers = self.session_db.query(personalDB).filter().all()

        for i in answer:
            mystr = i[0]
            mystr = mystr[1:-1].split(',')
            for i in pers:
                if (i.id == int(mystr[1])):
                    per_name = f"{i.last_name} {i.first_name} {i.father_name}"
                    break

            mystr = {"datetime": mystr[0], "name": per_name}
            #mystr = {"datetime": mystr[0], "per_id": int(mystr[1])}
            ans.append(mystr)

        return JSONResponse(content=ans, status_code=200)

    def get_cabs_names(self,user_id):
        answer = self.session_db.query(cabinetsDB.id,cabinetsDB.name).all()

        ans = {}

        for i in answer:
            mystr = i
            ans[mystr[0]]= f"{mystr[1]}"


        return JSONResponse(content=ans, status_code=200)