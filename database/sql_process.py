# coding: utf-8
from os import remove
import sys

from sqlalchemy.sql.expression import insert

sys.path.append("D:\myfiles\code\\front_end\\baijing_building_book_back_end")
sys.path.append("../")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.types import String,Integer
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

class Categories(Model):
    __tablename__="Categories"

    cate_id = Column(Integer, primary_key=True)
    cate_name=Column(String(50))

    @property
    def json(self):
        return dict(cate_id=self.cate_id,
                    cate_name=self.cate_name)

    @classmethod
    def get_categories(cls):
        categories=cls.query.filter().all()
        category_list = list()
        for category in categories:
            category_list.append(dict(cate_id=category.cate_id,
                                      cate_name=category.cate_name))
        return category_list

    @classmethod
    def get_category_by_id(cls,cate_id):
        category=cls.query.filter(Categories.cate_id==cate_id).one()
        return True, dict(cate_id=category.cate_id,
                    cate_name=category.cate_name)


    @classmethod
    def remove_category(cls,cate_id):
        category=cls.query.filter(Categories.cate_id==cate_id).one()
        if delete_from_db(category):
            return True
        else:
            return False


    @classmethod
    def add_category(cls,cate_id,cate_name):
        club=Categories(cate_id=cate_id,cate_name=cate_name)
        if insert_into_db(club):
            return True
        else:
            return False

class Buildings(Model):
    __tablename__="Buildings"

    building_id=Column(Integer,primary_key=True)
    building_name=Column(String(50))
    building_img_url=Column(String(255))
    building_access_way=Column(String(255))

    @property
    def json(self):
        return dict(building_id=self.building_id,
                    building_name=self.building_name,
                    building_img_url=self.building_img_url,
                    building_access_way=self.building_access_way)
    
    @classmethod
    def get_homepage_buildings_info(cls):
        buildings=cls.query.filter().all()
        buildings_info_list=list()
        for building in buildings:
            buildings_info_list.append({"building_img_url":building.building_img_url,
                                        "building_name":building.building_name})
        return buildings_info_list

    @classmethod
    def get_building_by_id(cls,building_id):
        try:
            building=cls.query.filter(Buildings.building_id==building_id).one()
            return True,building.json
        except:
            return False,{}

    @classmethod
    def get_building_by_name(cls,building_name):
        try:
            building=cls.query.filter(Buildings.building_name==building_name).one()
            return True,building.json
        except:
            return False,{}

    @classmethod
    def remove_building(cls,building_id):
        building=cls.query.filter(Buildings.building_id==building_id).one()
        if delete_from_db(building):
            return True
        else:
            return False
    
    @classmethod
    def add_building(cls,building_id,building_name,building_img_url,building_access_way):
        building=Buildings(building_id=building_id,
                           building_name=building_name,
                           building_img_url=building_img_url,
                           building_access_way=building_access_way)
        if insert_into_db(building):
            return True
        else:
            return False
    
class BuildingMatch(Model):
    __tablename__="BuildingMatch"

    building_id=Column(Integer,ForeignKey("Buildings.building_id"),primary_key=True)
    match_url=Column(String(255),primary_key=True)

    @property
    def json(self):
        return dict(building_id=self.building_id,
                    match_url=self.match_url)
    
    @classmethod
    def get_match_url_by_building_id(cls,building_id):
        match_urls=cls.query.filter(BuildingMatch.building_id==building_id).all()
        match_url_list=list()
        for match_url in match_urls:
            match_url_list.append(match_url.match_url)
        return True,dict(building_id=building_id,
                    match_url_list=match_url_list)
    
    @classmethod
    def add_match(cls,building_id,match_url):
        building_match=BuildingMatch(building_id=building_id,
                                     match_url=match_url)
        if insert_into_db(building_match):
            return True
        else:
            return False

class BuildingCategory(Model):
    __tablename__="BuildingCategory"

    building_id=Column(Integer, ForeignKey("Buildings.building_id"), primary_key=True)
    cate_id = Column(Integer, ForeignKey("Categories.cate_id"), primary_key=True)

    @classmethod
    def get_category_by_building_id(cls,building_id):
        building_cate=cls.query.filter(BuildingCategory.building_id==building_id).one()
        category=Categories.get_category_by_id(building_cate.cate_id)
        return category
    
    @classmethod
    def add_building_to_category(cls,building_id,cate_id):
        building_category=BuildingCategory(building_id=building_id,cate_id=cate_id)
        if insert_into_db(building_category):
            return True
        else:
            return False

    @classmethod
    def get_building_list_by_category_id(cls,cate_id):
        building_cates=cls.query.filter(BuildingCategory.cate_id==cate_id).all()
        buildings_list=list()
        for building_cate in building_cates:
            status,building=Buildings.get_building_by_id(building_cate.building_id)
            buildings_list.append(building)
        return buildings_list
