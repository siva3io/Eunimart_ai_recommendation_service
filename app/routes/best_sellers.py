import logging
from flask import Blueprint, jsonify, request
from app.services.best_sellers import BestSellingProducts

best_selling_products = Blueprint('best_selling_products', __name__)

logger = logging.getLogger(__name__)


@best_selling_products.route('/best_selling_products', methods=['GET'])
def get_best_sellers():
    query_parms = dict(request.args)
    data = BestSellingProducts.get_best_selling_products(query_parms)
    return jsonify(data)

