from .db_base import MySqlBase
from sqlalchemy import Column, String, Integer, TIMESTAMP, JSON

class BestSellers(MySqlBase):
    __tablename__ = 'best_seller'
    id                          =   Column(Integer, primary_key=True)
    marketplace                 =   Column(String)
    category                    =   Column(String)
    sub_category_1              =   Column(String)
    sub_category_2              =   Column(String)
    product_link                =   Column(String)
    store_name                  =   Column(String)
    url                  =   Column(String)
    other_sellers               =   Column(JSON)  
    top_seller                  =   Column(String)
    position                    =   Column(String)
    best_selling_rank           =   Column(String)