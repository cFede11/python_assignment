from flask import Blueprint, request, jsonify
import mysql.connector

financial_data_blueprint = Blueprint('financial_data', __name__)

#MySQL database configuration
config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin',
    'database': 'test1'
}

@financial_data_blueprint.route('/api/financial_data', methods=['GET'])
def get_financial_data():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        symbol = request.args.get('symbol')
        limit = int(request.args.get('limit', 5))
        page = int(request.args.get('page', 1))

        #connect to the MySQL database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        #get the parameters
        query = "SELECT * FROM financial_data WHERE 1=1"
        if start_date:
            query += " AND date >= %s"
        if end_date:
            query += " AND date <= %s"
        if symbol:
            query += " AND symbol = %s"

        count_query = "SELECT COUNT(*) FROM ({}) AS subquery".format(query)
        params = []
        if start_date:
            params.append(start_date)
        if end_date:
            params.append(end_date)
        if symbol:
            params.append(symbol)

        cursor.execute(count_query, params)

        count_result = cursor.fetchone()
        count = count_result['COUNT(*)'] if count_result else 0

        #do the pagination
        offset = (page - 1) * limit
        query += " ORDER BY date DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cursor.execute(query, params)
        records = cursor.fetchall()
        conn.close()

        response = {
            "data": records,
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
        import traceback
        traceback.print_exc()
        response = {
            "data": [],
            "pagination": {},
            "info": {
                "error": str(e)
            }
        }
        return jsonify(response), 500
