import logging
from app.utils import catch_exceptions
from config import Config
import json
import requests

logger = logging.getLogger(name=__name__)

class GetNer(object):
    
    def __init__(self):
        pass
    
    @catch_exceptions
    def flow(self, request_data):
        try:
            get_vdezi_hierarchy = json.loads(requests.post(url = Config.GET_VDEZI_HIERARCHY,json= request_data).text)
            if get_vdezi_hierarchy["status"]:
                    request_data["data"].update(get_vdezi_hierarchy["data"])
           
            get_marketplace_hierarchy = json.loads(requests.post(url = Config.GET_HIERARCHY_ENDPOINT,json= request_data).text)
            if get_marketplace_hierarchy["status"]:
                    request_data["data"].update(get_marketplace_hierarchy["data"])
            
            similar_products_obj = json.loads(requests.post(url = Config.COMPETITIVE_PRODUCTS_ENDPOINT,json= request_data).text)
            if similar_products_obj["status"]:
                request_data["data"].update(similar_products_obj["data"])
            
            attributes_obj = json.loads(requests.post(url = Config.GET_NER_ATTRIBUTES,json= request_data).text)
            return attributes_obj      
        except Exception as e:
            logger.error(e,exc_info=True)    
        
    @catch_exceptions
    def get_attributes(self, request_data):
        try:
            response_data = {}
            mandatory_fields = ["image", "channel_id", "product_title", "highlights"]
            for field in mandatory_fields:
                if (not field in request_data["data"]) and (field=="highlights"):
                    request_data["data"]["highlights"] = ""
                else:
                    if not field in request_data["data"]:
                        response_data = {
                            "status":False,
                            "message":"Required field is missing",
                            "error_obj":{
                                "description":"{} is missing".format(field),
                                "error_code":"REQUIRED_FIELD_IS_MISSING"
                            }
                        }
            if not response_data:
                response_data = self.flow(request_data)
            return response_data
        except Exception as e:
            logger.error(e,exc_info=True)
    
GetNer = GetNer()