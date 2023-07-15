"""
This module defines Flask blueprints for financial data and statistics routes.

Module Dependencies:
    - flask
    - financial_data (module)
    - statistics (module)
"""
from flask import Blueprint
from financial_data import get_financial_data
from statistics import get_statistics

financial_data_blueprint = Blueprint('financial_data', __name__)
statistics_blueprint = Blueprint('statistics', __name__)

@financial_data_blueprint.route('/api/financial_data', methods=['GET'])
def financial_data_route():
    """
    Financial data route.
    
    Returns:
        The result of the `get_financial_data` function.
    """
    return get_financial_data()

@statistics_blueprint.route('/api/statistics', methods=['GET'])
def statistics_route():
    """
    Statistics route.
    
    Returns:
        The result of the `get_statistics` function.
    """
    return get_statistics()
