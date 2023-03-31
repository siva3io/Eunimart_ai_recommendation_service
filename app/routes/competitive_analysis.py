import logging
from flask import Blueprint, jsonify, request
from app.services.competitive_analysis import CompetitiveProducts,CompetitiveSellers

competitive_analysis = Blueprint('competitive_analysis', __name__)

logger = logging.getLogger(__name__)


@competitive_analysis.route('/competitive_analysis/products', methods=['POST'])
def get_competitive_products():

    request_data = request.get_json()
    data = CompetitiveProducts.get_competitive_products(request_data)
    if not data:
        data = {}
    return jsonify(data)

@competitive_analysis.route('/competitive_analysis/sellers', methods=['POST'])
def get_competitive_sellers():

    request_data = request.get_json()
    data = CompetitiveSellers.get_competitive_sellers(request_data)
    if not data:
        data = {}
    return jsonify(data)

