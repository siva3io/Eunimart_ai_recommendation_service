import logging
from flask import Blueprint, jsonify, request
from app.services.get_categories_sub_categories import GetCategoriesList

get_categories_sub_categories = Blueprint('get_categories_sub_categories', __name__)

logger = logging.getLogger(__name__)


@get_categories_sub_categories.route('/get_categories_sub_categories', methods=['GET'])
def category_sub_category_route():
    query_parms = dict(request.args)
    data = GetCategoriesList.get_categories_sub_categories_list(query_parms)
    return jsonify(data)