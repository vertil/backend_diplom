import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Date
from sqlalchemy.dialects.postgresql import BYTEA, CIDR
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class departmentDB(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True)
    name = Column(Text)


class personalDB(Base):
    __tablename__ = "personal"

    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)
    father_name = Column(Text)
    email = Column(Text)
    birth = Column(Date)
    dep_id = Column(Integer)


class facesDB(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True)
    file = Column(BYTEA)
    face_data = Column(BYTEA)
    personal_id = Column(Integer)


class cabinetsDB(Base):
    __tablename__ = "cabinets"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    floor = Column(Integer)
    dep_id = Column(Integer)


class camerasDB(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True)
    cam_model = Column(Text)
    ipaddr = Column(CIDR)
    cab_id = Column(Integer)
    in_pos = Column(Boolean)
    pass_num = Column(Integer)
    status = Column(Boolean)


class in_out_dateDB(Base):
    __tablename__ = "in_out_date"

    time = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    per_id = Column(Integer)
    cam_id = Column(Integer)


class undendified_facesDB(Base):
    __tablename__ = "undendified_faces"

    time = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    per_id = Column(Integer)
    file = Column(BYTEA)