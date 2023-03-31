from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer, TIMESTAMP, JSON


class Products(MySqlBase):
    __tablename__           = 'products'
    id                      = Column(String, primary_key=True)
    fid                     = Column(String)
    shipping_price          = Column(String)
    selling_price           = Column(String)
    shipping_price          = Column(String)


class CompetiveProducts(MySqlBase):
    __tablename__           = 'products'
    __table_args__ = {'extend_existing': True}
    other_sellers           = Column(JSON) 
    selling_price           = Column(String)
    shipping_price          = Column(String)
    url                     = Column(String)
    store_name              = Column(String)
    store_rating            = Column(String)