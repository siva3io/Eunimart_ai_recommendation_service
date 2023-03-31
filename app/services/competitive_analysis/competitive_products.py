import re
import logging
from app.utils import catch_exceptions
from app.models.products import Products
from config import Config
from constants import channel_id_currency_mapping
import json
import requests

logger = logging.getLogger(name=__name__)

class GetCompetitiveProducts(object):

    def __init__(self):
        pass
    
    @catch_exceptions
    def fetch_competitive_products(self, similar_fids, channel_id):
        products_query = {
            "fid__in":similar_fids
        }
        products_list = Products.smart_query(filters=products_query).all()
        final_results = []
        for product in products_list:
            product = product.to_dict(nested=True)
            product["image_url"] = product.get("image_1","")
            if not product["image_url"]:
                product["image_url"] = product.get("image_2","")
            del product["image_1"],product["image_2"],product["fid"],product["id"]
            
            if product["listing_price"] == "0":
                product["listing_price"] = "not_available"
            
            if product["selling_price"] == "0":
                product["selling_price"] = "not_available"

            if bool(re.match('^[0-9,.]*$',product["listing_price"])):
                product["listing_price"] = channel_id_currency_mapping[channel_id]+product["listing_price"]

            if bool(re.match('^[0-9,.]*$',product["selling_price"])):
                product["selling_price"] = channel_id_currency_mapping[channel_id]+product["selling_price"]

            if bool(re.match('^[0-9,.]*$',product["saved_price"])):
                product["saved_price"] = channel_id_currency_mapping[channel_id]+product["saved_price"]

            if bool(re.match('^[0-9,.]*$',product["shipping_price"])):
                product["shipping_price"] = channel_id_currency_mapping[channel_id]+product["shipping_price"]
             
            product["channel_id"] = channel_id
            final_results.append(product)
        return final_results
    
    @catch_exceptions
    def extract_attributes(self, request_data):
        try:
            attributes = json.loads(requests.post(url = Config.EXTRACT_ATTRIBUTES,json= request_data).text)
            return attributes
        except Exception as e:
            logger.error(e,exc_info=True)
    
    @catch_exceptions
    def get_common_attributes_count(self, product_attributes, similar_product_attributes):
        try:
                number_of_common_attributes = len(set(product_attributes.items()) & set(similar_product_attributes.items()))
                return number_of_common_attributes
        except Exception as e:
            logger.error(e,exc_info=True)
            
    @catch_exceptions
    def sort_similar_products(self, products_list, request_data):
        try:
            similarity_count = {}
            sorted_competetive_list = []
            product_attributes = self.extract_attributes(request_data)
            request_data["data"]["product_title"] = []
            for each_product_index in range(0,len(products_list)):
                request_data["data"]["product_title"].append(products_list[each_product_index]["product_title"])
            similar_products_attributes = self.extract_attributes(request_data)["data"]["product_details"] # sending a list of titles to the extract attr. api
            for each_similar_product_index in range(0, len(similar_products_attributes)): 
                common_atttibutes_count = self.get_common_attributes_count(product_attributes["data"]["product_details"][0], similar_products_attributes[each_similar_product_index])
                similarity_count[each_similar_product_index] = common_atttibutes_count
            sorted_count = sorted(similarity_count.items(), key=lambda item: item[1], reverse = True) #sort the dictionary based on values   
            for each_index in sorted_count:
                sorted_competetive_list.append(products_list[each_index[0]]) #appending the elements of products list based on the sorted indeces
            return sorted_competetive_list   
        except Exception as e:
            logger.error(e,exc_info=True)
            
    @catch_exceptions
    def get_similar_products(self,request_data):
        try:
            channel_id_list = []
            channel_id_list.append(request_data["data"]["channel_id"])
            competitive_products_list = []
            count_errors = 0
            # get_vdezi_hierarchy = json.loads(requests.post(url = Config.GET_VDEZI_HIERARCHY,json= request_data).text)
            # if get_vdezi_hierarchy["status"]:
                    # request_data["data"]["category_id"] = str(get_vdezi_hierarchy["data"]["category_id"])
                    # request_data["data"]["sub_category_id"] = str(get_vdezi_hierarchy["data"]["sub_category_id"]) 
            product_title = request_data["data"]["product_title"] + " " + request_data["data"]["highlights"]
            for channel_id in channel_id_list:
                request_data["data"]["product_title"] = product_title
                request_data["data"]["channel_id"] = channel_id
                # get_hierarchy_obj = json.loads(requests.post(url = Config.GET_HIERARCHY_ENDPOINT,json= request_data).text)
                # if get_hierarchy_obj["status"]:
                    # request_data["data"].update(get_hierarchy_obj["data"])
                similar_fids_obj = json.loads(requests.post(url = Config.COMPETITIVE_PRODUCTS_ENDPOINT,json= request_data).text)
                print(similar_fids_obj)
                if similar_fids_obj["status"]:
                    competetive_products = self.fetch_competitive_products(similar_fids_obj["data"]["similar_products"],channel_id)
                    # competitive_products_list.extend(self.sort_similar_products(competetive_products, request_data))
                else:
                    count_errors += 1
                    error_response_data = similar_fids_obj
                    
            if count_errors < len(channel_id_list):
                response_data = {
                    "status":True,
                    "data":competetive_products,
                    "columns": [
                        {
                            "column_key": "image_url",
                            "column_name": "Image",
                            "column_position": 1
                        },
                        {
                            "column_key": "product_title",
                            "column_name": "Product Title",
                            "column_position": 2
                        },
                        {
                            "column_key": "channel_id",
                            "column_name": "Channel id",
                            "column_position": 3
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
                        }
                    ]
                }
            else:
                response_data = error_response_data
            return response_data
        except Exception as e:
            logger.error(e,exc_info=True)

    @catch_exceptions
    def get_competitive_products(self, request_data):
        try:
            mandatory_fields = ["sku_id", "image", "channel_id", "product_title", "highlights","category_name","sub_category_name"]
            missing_fields = []
            for field in mandatory_fields:
                if (not field in request_data["data"]) and (field=="highlights"):
                    request_data["data"]["highlights"] = ""
                else:
                    if not field in request_data["data"]:
                        missing_fields.append(field)
            response_data = {
                "status":False,
                "message":"Required field is missing",
                "error_obj":{
                    "description":"{} missing".format(','.join(missing_fields)),
                    "error_code":"REQUIRED_FIELD_IS_MISSING"
                }
            }
            """Code Updated on 18/01/2022. Added error response if any untrained marketplace is requested."""
            if not missing_fields: 
                if request_data["data"]["channel_id"] in ["1","3","12","14","15"]: #update channel id for trained marketplace here.
                    response_data = self.get_similar_products(request_data)
                else:
                    response_data = {
                        "status":False,
                        "message":"Similar Products for selected marketplace is not available. Similar Products is available only for Amazon_USA,Amazon_India,Flipkart,Bonanza,eBay.",
                        "error_obj":{
                            "description":"Service not available for {}. Service is available only for Amazon_USA,Amazon_India,Flipkart,Bonanza,eBay.".format(request_data["data"]["channel_id"]),
                            "error_code":"SERVICE_NOT_AVAILABLE_FOR_SELECTED_MARKETPLACE"
                        }
                    }                    
            return response_data
        except Exception as e:
            logger.error(e,exc_info=True)
    
CompetitiveProducts = GetCompetitiveProducts()