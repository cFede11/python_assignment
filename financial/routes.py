from flask import Blueprint
from financial_data import get_financial_data
from statistics import get_statistics

financial_data_blueprint = Blueprint('financial_data', __name__)
statistics_blueprint = Blueprint('statistics', __name__)

@financial_data_blueprint.route('/api/financial_data', methods=['GET'])
def financial_data_route():
    return get_financial_data()

@statistics_blueprint.route('/api/statistics', methods=['GET'])
def statistics_route():
    return get_statistics()
