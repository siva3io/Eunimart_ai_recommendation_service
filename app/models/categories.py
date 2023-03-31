from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer, DateTime, JSON
import datetime

class Categories(MySqlBase):
    __tablename__           = 'categories'
    id                      = Column(Integer, primary_key=True)
    marketplace             = Column(String)
    category                = Column(String)
    sub_category_1          = Column(String)
    sub_category_2          = Column(String)   
    created_date            = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date            = Column(DateTime, default=datetime.datetime.utcnow)
