from flask import Blueprint, request, jsonify
import sqlite3
import os

financial_data_blueprint = Blueprint('financial_data', __name__)

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'schema.db')

@financial_data_blueprint.route('/api/financial_data', methods=['GET'])
def get_financial_data():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        symbol = request.args.get('symbol')
        limit = int(request.args.get('limit', 5))
        page = int(request.args.get('page', 1))

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        #get the parameters
        query = "SELECT * FROM financial_data WHERE 1=1"
        if start_date:
            query += " AND date >= '{}'".format(start_date)
        if end_date:
            query += " AND date <= '{}'".format(end_date)
        if symbol:
            query += " AND symbol = '{}'".format(symbol)

        count_query = "SELECT COUNT(*) FROM ({})".format(query)
        cursor.execute(count_query)
        count = cursor.fetchone()[0]

        #calculate the pagination
        offset = (page - 1) * limit
        query += " ORDER BY date DESC LIMIT {} OFFSET {}".format(limit, offset)

        cursor.execute(query)
        records = cursor.fetchall()
        conn.close()

        response = {
            "data": [dict(record) for record in records],
            "pagination": {
                "count": count,
                "page": page,
                "limit": limit,
                "pages": (count + limit - 1) // limit
            },
            "info": {
                "error": ""
            }
        }

        return jsonify(response)
    except Exception as e:
        response = {
            "data": [],
            "pagination": {},
            "info": {
                "error": str(e)
            }
        }
        return jsonify(response), 500


