# coding: utf-8

import sys
sys.path.append("D:\myfiles\code\\front_end\\baijing_building_book_back_end")
sys.path.append("../")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.types import String,CHAR,Integer
from utils.config import SQL_CONFIG
def get_engine():
    db_name=SQL_CONFIG["DB_NAME"]
    db_host=SQL_CONFIG["DB_HOST"]
    db_port=SQL_CONFIG["DB_PORT"]
    db_user = SQL_CONFIG["DB_USER"]
    db_pwd = SQL_CONFIG["DB_PASSWORD"]
    
    _connectstr = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8"
    _connectstr = _connectstr.format(db_user, db_pwd, db_host, db_port, db_name)
    _engine = create_engine(_connectstr, echo=False, pool_size=10)
    return _engine

def get_session(engine):
    session = scoped_session(sessionmaker(bind=engine))
    return session

engine=get_engine()
Session=get_session(engine=engine)

Model=declarative_base(name="est_model")
Model.query=Session.query_property()

def insert_into_db(obj):
    try:
        Session.add(obj)
        Session.commit()
        return True
    except:
        Session.rollback()
        return False

def delete_from_db(obj):
    try:
        Session.delete(obj)
        Session.commit()
        return True
    except:
        Session.rollback()
        return False

class Categories(object):
    __tablename__="categories"
