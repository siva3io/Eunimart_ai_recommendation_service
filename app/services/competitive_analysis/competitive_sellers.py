import re
import logging
from app.utils import catch_exceptions
from app.models.products import CompetiveProducts
import json
import requests
from config import Config
from constants import channel_id_currency_mapping

logger = logging.getLogger(name=__name__)


class GetCompetitiveSellers(object):

    def __init__(self):
        pass

    @catch_exceptions
    def fetch_competitive_sellers(self, similar_fids,channel_id):

        products_query = {
            "fid__in":similar_fids
        }
        products_list = CompetiveProducts.smart_query(filters=products_query).all()

        final_results = []

        for product in products_list:
            product = product.to_dict(nested=True)
            product["product_link"] = product.get("url","Not Available")
            product["image_url"] = product.get("image_1","")
            if not product["image_url"]:
                product["image_url"] = product.get("image_2","")
            del product["image_1"],product["image_2"],product["fid"],product["id"]
            del product["url"]
            if product["listing_price"] == "0":
                product["listing_price"] = "not_available"
            
            if product["selling_price"] == "0":
                product["selling_price"] = "not_available"

            if product["store_name"] == "not_available":
                product["store_name"] = "Amazon"       
            
            product["channel_id"] = channel_id
            
            final_results.append(product)
        
        return final_results
    
    @catch_exceptions
    def combine_other_sellers(self,competitive_sellers):
        
        for seller_index in range(len(competitive_sellers)):
            other_sellers_list = competitive_sellers[seller_index]["other_sellers"]
            if other_sellers_list and other_sellers_list[0]:
                for other_seller in other_sellers_list:
                    modified_seller = {
                        "image_url":competitive_sellers[seller_index]["image_url"],
                        "product_title":competitive_sellers[seller_index]["product_title"],
                        "listing_price":other_seller.get("price","Not Available"),
                        "selling_price":other_seller.get("price","Not Available"),
                        "saved_price":"0",
                        "shipping_price":other_seller.get("shipping_price","Not Available"),
                        "product_link":other_seller.get("url","Not Available"),
                        "store_name":other_seller.get("store_name","Not Available"),
                        "store_rating":other_seller.get("avg_rating","Not Available")
                    }
                    competitive_sellers.append(modified_seller)
                    
            del competitive_sellers[seller_index]["other_sellers"]

        return competitive_sellers 
                
    
    @catch_exceptions
    def get_similar_sellers(self,request_data):
        channel_id_list = []
        channel_id_list.append(request_data["data"]["channel_id"])
        competitive_sellers_list = []
        error_response_data = []
        count_errors = 0
        for channel_id in channel_id_list:
            request_data["data"]["channel_id"] = channel_id
            get_hierarchy_obj = json.loads(requests.post(url = Config.GET_HIERARCHY_ENDPOINT,json= request_data).text)
            if get_hierarchy_obj["status"]:
                request_data["data"].update(get_hierarchy_obj["data"])
            similar_fids_obj = json.loads(requests.post(url = Config.COMPETITIVE_PRODUCTS_ENDPOINT,json= request_data).text)
            if similar_fids_obj["status"]:
                competitive_sellers = self.fetch_competitive_sellers(similar_fids_obj["data"]["similar_products"],channel_id)
                competitive_sellers_list.extend(self.combine_other_sellers(competitive_sellers))
                
                for competitive_seller in competitive_sellers_list:
                    
                    if bool(re.match('^[0-9,.]*$',competitive_seller["listing_price"])):
                        competitive_seller["listing_price"] = channel_id_currency_mapping[channel_id]+competitive_seller["listing_price"]
                    
                    if bool(re.match('^[0-9,.]*$',competitive_seller["selling_price"])):
                        competitive_seller["selling_price"] = channel_id_currency_mapping[channel_id]+competitive_seller["selling_price"]

                    if bool(re.match('^[0-9,.]*$',competitive_seller["saved_price"])):
                        competitive_seller["saved_price"] = channel_id_currency_mapping[channel_id]+competitive_seller["saved_price"]

                    if bool(re.match('^[0-9,.]*$',competitive_seller["shipping_price"])):
                        competitive_seller["shipping_price"] = channel_id_currency_mapping[channel_id]+competitive_seller["shipping_price"]
            
            else:
                count_errors += 1
                error_response_data = similar_fids_obj
        if count_errors < len(channel_id_list):
            response_data = {
                "status" : True,
                "data" : competitive_sellers_list,
                "columns" : [
                    {
                        "column_key": "image_url",
                        "column_name": "Image",
                        "column_position": 1
                    },
                    {
                        "column_key": "listing_price",
                        "column_name": "Listing Price",
                        "column_position": 4
                    },
                    {
                        "column_key": "selling_price",
                        "column_name": "Selling Price",
                        "column_position": 5
                    },
                    {
                        "column_key": "saved_price",
                        "column_name": "Saved Price",
                        "column_position": 6
                    },
                    {
                        "column_key": "shipping_price",
                        "column_name": "Shipping Price",
                        "column_position": 7
                    },
                    {
                        "column_key": "product_link",
                        "column_name": "Product Link",
                        "column_position": 8
                    },
                    {
                        "column_key": "store_name",
                        "column_name": "Store Name",
                        "column_position": 9
                    },
                    {
                        "column_key": "store_rating",
                        "column_name": "Store Rating",
                        "column_position": 10
                    }
                ]
            }
        else:
            response_data = error_response_data
        return response_data
    
    @catch_exceptions
    def get_competitive_sellers(self, request_data):
        try:
            response_data = {}
            mandatory_fields = ["sku_id", "image","channel_id","product_title"]
            for field in mandatory_fields:
                if not field in request_data["data"]:
                    response_data = {
                        "status":False,
                        "message":"Required field is missing",
                        "error_obj":{
                            "description":"{} is missing".format(field),
                            "error_code":"REQUIRED_FIELD_IS_MISSING"
                        }
                    }
            """Code Updated on 18/01/2022. Added error response if any untrained marketplace is requested."""
            if not response_data: 
                if request_data["data"]["channel_id"] in ["1","3","12","14","15"]: #update channel id for trained marketplace here.
                    response_data = self.get_similar_sellers(request_data)
                else:
                    response_data = {
                        "status":False,
                        "message":"Similar Sellers for selected marketplace is not available. Similar Sellers is available only for Amazon_USA,Amazon_India,Flipkart,Bonanza,eBay.",
                        "error_obj":{
                            "description":"Service not available for {}. Service is available only for Amazon_USA,Amazon_India,Flipkart,Bonanza,eBay.".format(request_data["data"]["channel_id"]),
                            "error_code":"SERVICE_NOT_AVAILABLE_FOR_SELECTED_MARKETPLACE"
                        }
                    }
            return response_data
        except Exception as e:
            logger.error(e,exc_info=True)


    
CompetitiveSellers = GetCompetitiveSellers()