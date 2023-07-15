"""
This module defines a Flask blueprint for retrieving statistics from a MySQL database.

Blueprint Routes:
    - GET /api/statistics: Retrieves statistics based on the provided parameters.

Module Dependencies:
    - flask
    - mysql.connector
    - datetime
    - os
"""

from flask import Blueprint, request, jsonify
import mysql.connector
from datetime import datetime
import os

statistics_blueprint = Blueprint('statistics', __name__)

# MySQL database configuration
config = {
    'host': 'database',
    'user': f'root',
    'database': 'financial_db'
}

@statistics_blueprint.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Retrieves statistics from a MySQL database based on the provided parameters.

    Request Parameters:
        - start_date (str): The start date for the statistics (required).
        - end_date (str): The end date for the statistics (required).
        - symbol (str): The symbol for the statistics (required).

    Returns:
        If successful, returns a JSON response containing the calculated statistics and an empty error message.
        If any of the required parameters are missing or the date format is invalid, returns a JSON response with an empty data field and an error message.
        If an error occurs while retrieving or processing the statistics, returns a JSON response with an empty data field and an error message.

    Raises:
        Exception: If an error occurs while retrieving or processing the statistics.
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        symbol = request.args.get('symbol')

        # Validate all required parameters exist
        if not start_date or not end_date or not symbol:
            response = {
                "data": {},
                "info": {
                    "error": "Missing required parameters."
                }
            }
            return jsonify(response)

        # Validate date format and valid dates
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            response = {
                "data": {},
                "info": {
                    "error": "Invalid date format or invalid date provided."
                }
            }
            return jsonify(response)

        # Connect to the MySQL database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        # Calculate the average of open_price, close_price, volume
        query = "SELECT AVG(open_price) AS avg_open_price, AVG(close_price) AS avg_close_price, AVG(volume) AS avg_volume FROM financial_data WHERE date >= %s AND date <= %s AND symbol = %s"
        cursor.execute(query, (start_date, end_date, symbol))
        result = cursor.fetchone()
        conn.close()

        statistics = {
            "start_date": start_date,
            "end_date": end_date,
            "symbol": symbol,
            "average_daily_open_price": result["avg_open_price"],
            "average_daily_close_price": result["avg_close_price"],
            "average_daily_volume": result["avg_volume"]
        }

        response = {
            "data": statistics,
            "info": {
                "error": ""
            }
        }

        return jsonify(response)
    except Exception as e:
        import traceback
        traceback.print_exc()

        # Prepare the error response JSON
        response = {
            "data": {},
            "info": {
                "error": f"An error occurred while processing the request: {str(e)}"
            }
        }
        return jsonify(response), 500
