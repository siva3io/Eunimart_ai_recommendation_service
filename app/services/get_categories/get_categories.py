import os
import logging
from app.models.categories import Categories
from app.utils import catch_exceptions

logger = logging.getLogger(name=__name__)

class QueryCategories(object):

    def __init__(self):
        self.columns = {
            "category":Categories.category,
            "sub_category_1":Categories.sub_category_1,
            "sub_category_2":Categories.sub_category_2
        }
        
    
    def get_selected_coulmn(self, query_params):
        selection_order = ["category", "sub_category_1", "sub_category_2" ]
        column = self.columns["category"]
        column_name = "category"
        for current_selection ,next_selection in zip( selection_order, selection_order[1:] ):
            if current_selection in query_params:
                column = self.columns[next_selection]
                column_name = next_selection
        return column_name, column

    @catch_exceptions
    def get_categories_list(self,query_params):
        logger.request_debug("Query Params %s", query_params)
        column_name, selected_column = self.get_selected_coulmn(query_params)
        if query_params:
            category_list = Categories.smart_query(filters=query_params).with_entities(selected_column).group_by(selected_column).order_by(selected_column).all()
            result_obj = dict(query_params)
            result_obj[column_name] = [category_name[0] for category_name in category_list]
            result_obj = [result_obj]
        else:
            category_list = Categories.smart_query(filters={}).with_entities(Categories.marketplace, Categories.category).group_by(Categories.marketplace, Categories.category).order_by(Categories.marketplace, Categories.category).all()
            result_obj = {}
            for category in category_list:
                temp = result_obj.get(category[0],{ "marketplace": category[0]})
                temp["category"] = temp.get("category",[])
                temp["category"].append(category[1])
                result_obj[category[0]] = temp
            result_obj = [ result_obj[key] for key in result_obj.keys() ]
        return result_obj
    
    @catch_exceptions
    def get_marketplaces_list(self):
        marketplaces_list = Categories.smart_query(filters={}).with_entities(Categories.marketplace).group_by(Categories.marketplace).all()
        response = {}
        temp_list = []
        for marketplace in marketplaces_list:
            if (marketplace[0]):
                temp_list.append(marketplace[0])
        response["marketplaces"] = temp_list
        return response

GetCategories = QueryCategories()