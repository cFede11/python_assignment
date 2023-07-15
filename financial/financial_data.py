"""
This module defines a Flask blueprint for retrieving financial data from a MySQL database.

Blueprint Routes:
    - GET /api/financial_data: Retrieves financial data based on the provided parameters.

Module Dependencies:
    - flask
    - mysql.connector
"""

from flask import Blueprint, request, jsonify
import mysql.connector

financial_data_blueprint = Blueprint('financial_data', __name__)

# MySQL database configuration
config = {
    'host': 'database',
    'user': f'root',
    'database': 'financial_db'
}

@financial_data_blueprint.route('/api/financial_data', methods=['GET'])
def get_financial_data():
    """
    Retrieves financial data from a MySQL database based on the provided parameters.

    Request Parameters:
        - start_date (str): The start date for the financial data (optional).
        - end_date (str): The end date for the financial data (optional).
        - symbol (str): The symbol for the financial data (optional).
        - limit (int): The maximum number of records to retrieve (default: 5).
        - page (int): The page number for pagination (default: 1).

    Returns:
        If successful, returns a JSON response containing the financial data, pagination information, and an empty error message.
        If an error occurs, returns a JSON response with an empty data field, empty pagination field, and an error message.

    Raises:
        Exception: If an error occurs while retrieving the financial data from the MySQL database.
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        symbol = request.args.get('symbol')
        limit = int(request.args.get('limit', 5))
        page = int(request.args.get('page', 1))

        # Connect to the MySQL database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        # Build the query based on the provided parameters
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

        # Execute the count query to get the total number of records
        cursor.execute(count_query, params)
        count_result = cursor.fetchone()
        count = count_result['COUNT(*)'] if count_result else 0

        # Perform pagination
        offset = (page - 1) * limit
        query += " ORDER BY date DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        # Execute the query to retrieve the financial data
        cursor.execute(query, params)
        records = cursor.fetchall()
        conn.close()

        # Prepare the response JSON
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

        # Prepare the error response JSON
        response = {
            "data": [],
            "pagination": {},
            "info": {
                "error": str(e)
            }
        }
        return jsonify(response), 500
