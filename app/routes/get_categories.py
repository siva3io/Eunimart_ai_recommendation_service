import logging
from flask import Blueprint, jsonify, request
from app.services.get_categories import GetCategories

get_categories = Blueprint('get_categories', __name__)

logger = logging.getLogger(__name__)


@get_categories.route('/get_categories', methods=['GET'])
def category_route():
    query_parms = request.args
    data = GetCategories.get_categories_list(query_parms)
    return jsonify(data)

@get_categories.route('/get_marketplaces',methods= ['GET'])
def get_marketplaces():
    data = GetCategories.get_marketplaces_list()
    return jsonify(data)