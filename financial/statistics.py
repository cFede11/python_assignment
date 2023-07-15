from flask import Blueprint, request, jsonify
import mysql.connector
from datetime import datetime
import os

statistics_blueprint = Blueprint('statistics', __name__)

#MySQL database configuration
config = {
    'host': 'database',
    'user': f'root',
    'database': 'financial_db'
}

@statistics_blueprint.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        symbol = request.args.get('symbol')

        #validate all required parameters exist
        if not start_date or not end_date or not symbol:
            response = {
                "data": {},
                "info": {
                    "error": "Missing required parameters."
                }
            }
            return jsonify(response)

        #validate date format and valid dates
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

        #connect to the MySQL database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        #calculate the average of open_price, close_price, volume
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
        response = {
            "data": {},
            "info": {
                "error": f"An error occurred while processing the request: {str(e)}"
            }
        }
        return jsonify(response), 500
