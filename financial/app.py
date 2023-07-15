"""
This module initializes a Flask application and registers the blueprints for the financial data and statistics routes.

Module Dependencies:
    - flask.Flask
    - routes.financial_data_blueprint
    - routes.statistics_blueprint
"""
from flask import Flask
from routes import financial_data_blueprint, statistics_blueprint

app = Flask(__name__)
app.register_blueprint(financial_data_blueprint)
app.register_blueprint(statistics_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
