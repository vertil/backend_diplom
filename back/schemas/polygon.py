import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import CIDR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PolygonDB(Base):
    __tablename__ = "polygons"

    id = Column(Integer, primary_key=True)
    name = Column(String, )
    status = Column(String, )
    create_date = Column(DateTime, default=datetime.datetime.utcnow)


class MachineDB(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, )
    ip = Column(CIDR)
    vmid = Column(Integer)
    polygon_id = Column(Integer)
    type = Column(String)
    iptable_type = Column(String)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    node = Column(String)

class MachineTemplDB(Base):
    __tablename__ = "machine_templ"

    name = Column(String, primary_key=True,)
    type = Column(String)
    ram = Column(Integer)
    sockets = Column(Integer)
    cores = Column(Integer)
    proxmox_template = Column(String, )
    iptables_type = Column(String, )
    last_ip_decade = Column(Integer)
    amount = Column(Integer)

class MachineTempInitlDB(Base):
    __tablename__ = "init_machines"

    name = Column(String, primary_key=True,)
    type = Column(String)
    ram = Column(Integer)
    sockets = Column(Integer)
    cores = Column(Integer)
    proxmox_template = Column(String, )
    iptables_type = Column(String, )
    last_ip_decade = Column(Integer)
    amount = Column(Integer)

class VpnKeysDB(Base):
    __tablename__ = "vpn_keys"

    wg = Column(Integer,primary_key=True,)
    name = Column(String,)
    serv_key = Column(String,)
    user_key = Column(String,)
    pol_id = Column(Integer)
    
    



