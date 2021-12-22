# coding: utf-8
from sqlalchemy import create_engine
from utils.config import SQL_CONFIG

def get_engine():
    db_name=SQL_CONFIG["DB_NAME"]
    db_host=SQL_CONFIG["DB_HOST"]
    db_port=SQL_CONFIG["DB_PORT"]
    db_user = SQL_CONFIG["DB_USER"]
    db_passwd=SQL_CONFIG["DB_PASSWORD"]
    