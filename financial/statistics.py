from flask import Blueprint, request, jsonify
import sqlite3
import os

statistics_blueprint = Blueprint('statistics', __name__)

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'schema.db')

@statistics_blueprint.route('/api/statistics', methods=['GET'])
def get_statistics():
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

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Calculate the average of open_price, close_price, volume
        query = "SELECT AVG(open_price) AS avg_open_price, AVG(close_price) AS avg_close_price, AVG(volume) AS avg_volume FROM financial_data WHERE date >= ? AND date <= ? AND symbol = ?"
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
        response = {
            "data": {},
            "info": {
                "error": str(e)
            }
        }
        return jsonify(response), 500

