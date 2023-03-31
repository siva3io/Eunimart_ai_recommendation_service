from ast import Return
import os
import logging
from constants import channel_id_name_mapping,cat_subcat
from app.utils import catch_exceptions

logger = logging.getLogger(name=__name__)

class GetCategories(object):
    def __init__(self):
        pass
    
    def get_categories_sub_categories_list(self,query_parms):
        """Code Updated on 18/01/2022. Added error response if any untrained marketplace is requested."""
        if query_parms["channel_id"] in ["1","3","12","14","15","24"]: #update channel id for trained marketplace here.
            marketplace_name = channel_id_name_mapping.get(query_parms["channel_id"])
            category_sub_category_list = cat_subcat.get(marketplace_name)
            return category_sub_category_list
        else:
            response_data = {
                "status":False,
                "message":"Categories, Subcategories list for selected marketplace is not available. Categories, Subcategories list is available only for Amazon_USA,Amazon_India,Flipkart,Bonanza,eBay,Etsy",
                "error_obj":{
                    "description":"Service not available for {}. Service is available only for Amazon_USA,Amazon_India,Flipkart,Bonanza,eBay,Etsy.".format(query_parms["channel_id"]),
                    "error_code":"SERVICE_NOT_AVAILABLE_FOR_SELECTED_MARKETPLACE"
                }
            } 
            return response_data


GetCategoriesList = GetCategories()