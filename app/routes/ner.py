import logging
from flask import Blueprint, jsonify, request
from app.services.ner import GetNer

ner = Blueprint('ner', __name__)

logger = logging.getLogger(__name__)

@ner.route('/ner', methods=['POST'])
def get_competitive_products():
    request_data = request.get_json()
    data = GetNer.get_attributes(request_data)
    if not data:
        data = {}
    return jsonify(data)