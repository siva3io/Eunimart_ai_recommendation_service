import logging
from app.utils import catch_exceptions
from app.models.best_sellers import BestSellers
import json
import requests
from config import Config
import re
from constants import channel_id_name_mapping

logger = logging.getLogger(name=__name__)


class GetBestSellingProducts(object):
    def __init__(self):
        pass

    @catch_exceptions
    def fetch_best_selling_products(self, query_params):
        query_params['best_selling_rank__ne']='not_available'
        query_params['marketplace'] = channel_id_name_mapping[query_params['channel_id']]
        best_selling_products = []
        products_list = BestSellers.smart_query(filters=query_params).limit(10).all()
        for product in products_list:
            product = product.to_dict(nested=True)
            image = product.get("product_image_1","")

            if ".svg" in image or ".png" in image or image == "":
                product["product_image_1"] = product.get("product_image_2","")

            del product['id']
            del product["product_image_2"]
            
            try:
                product["product_image_1"] = re.sub(r"[.]_.*_[.]", ".", product["product_image_1"])

            except Exception as e:
                print(e)
                pass

            best_selling_products.append(product)
        return best_selling_products

    @catch_exceptions
    def get_best_selling_products(self, query_params):
        response_data = {}
        mandatory_fields = ["channel_id","category"]
        for field in mandatory_fields:
            if not field in query_params:
                response_data = {
                    "status":False,
                    "message":"Required field is missing",
                    "error_obj":{
                        "description":"{} is missing".format(field),
                        "error_code":"REQUIRED_FIELD_IS_MISSING"
                    }
                }
        if not response_data:
            best_selling_products = self.fetch_best_selling_products(query_params)
            response_data = {
                "status" : True,
                "data" : best_selling_products,
                "columns": [
                    {
                        "column_key": "best_selling_rank",
                        "column_name": "Best Selling Rank",
                        "column_position": 1
                    },
                    {
                        "column_key": "category",
                        "column_name": "Category",
                        "column_position": 2
                    },
                    {
                        "column_key": "sub_category_1",
                        "column_name": "Sub Category 1",
                        "column_position": 3
                    },
                    {
                        "column_key": "sub_category_2",
                        "column_name": "Sub Category 2",
                        "column_position": 4
                    },
                    {
                        "column_key": "marketplace",
                        "column_name": "Marketplace",
                        "column_position": 5
                    },
                    {
                        "column_key": "product_link",
                        "column_name": "Product Url",
                        "column_position": 6
                    },
                    {
                        "column_key": "product_image_1",
                        "column_name": "Image",
                        "column_position": 7
                    },
                    {
                        "column_key": "product_title",
                        "column_name": "Product Title",
                        "column_position": 8
                    },
                    {
                        "column_key": "product_rating",
                        "column_name": "Product Rating",
                        "column_position": 9
                    },
                    {
                        "column_key": "product_price",
                        "column_name": "Product Price",
                        "column_position": 10
                    },
                    {
                        "column_key": "store_name",
                        "column_name": "Store Name",
                        "column_position": 11
                    },
                    {
                        "column_key": "url",
                        "column_name": "Store Url",
                        "column_position": 12
                    },
                    {
                        "column_key": "top_seller",
                        "column_name": "Top Seller",
                        "column_position": 13
                    },
                    {
                        "column_key": "position",
                        "column_name": "Position",
                        "column_position": 14
                    },
                    {
                        "column_key": "other_sellers.avg_rating",
                        "column_name": "Average Rating",
                        "column_position": 15
                    },
                    {
                        "column_key": "other_sellers.condition",
                        "column_name": "Condition",
                        "column_position": 16
                    },
                    {
                        "column_key": "other_sellers.no_of_ratings",
                        "column_name": "No of ratings",
                        "column_position": 17
                    },
                    {
                        "column_key": "other_sellers.price",
                        "column_name": "Price",
                        "column_position": 18
                    },
                    {
                        "column_key": "other_sellers.shipping_price",
                        "column_name": "Shipping Price",
                        "column_position": 19
                    },
                    {
                        "column_key": "other_sellers.delivery_type",
                        "column_name": "Delivery Type",
                        "column_position": 20
                    },
                    {
                        "column_key": "other_sellers.rating",
                        "column_name": "Rating",
                        "column_position": 21
                    },
                    
                    {
                        "column_key": "other_sellers.url",
                        "column_name": "Store Link",
                        "column_position": 22
                    },
                    {
                        "column_key": "other_sellers.store_name",
                        "column_name": "Store Name",
                        "column_position": 23
                    }
                ]
            }

        return response_data

BestSellingProducts = GetBestSellingProducts()