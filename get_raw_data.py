"""
This module retrieves financial data from the Alpha Vantage API and upserts the data into a MySQL database.

Module Dependencies:
    - mysql.connector
    - alpha_vantage.timeseries.TimeSeries
    - os

Environment Variables:
    - AV_API_KEY: The API key for Alpha Vantage.

MySQL Database Configuration:
    - host (str): The hostname of the MySQL database.
    - user (str): The username for the MySQL database.
    - database (str): The name of the MySQL database.

Symbols:
    - symbols (list): The list of symbols for which to retrieve financial data.

Exceptions:
    - mysql.connector.Error: If there is an error with the MySQL connection.
    - ValueError: If the AV_API_KEY environment variable is not set.
    - Exception: For any other unexpected exceptions.
"""

import mysql.connector
from alpha_vantage.timeseries import TimeSeries
import os


# MySQL database configuration
config = {
    'host': 'database',
    'user': f'root',
    'database': 'financial_db'
}

# Get API KEY for Alpha Vantage
api_key = os.environ.get('AV_API_KEY')

# Check if the API key is available
if api_key is None:
    raise ValueError('AV_API_KEY environment variable is not set')

# Initialize Alpha Vantage
ts = TimeSeries(key=api_key, output_format='pandas')

# Symbols to be used (META MSFT)
symbols = ['IBM', 'AAPL']

try:
    # Connect to the MySQL database
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    def upsert_stock_record(symbol, date, open_price, close_price, volume):
        """
        Upserts a stock record into the financial_data table of the MySQL database.

        Args:
            symbol (str): The stock symbol.
            date (str): The date of the record.
            open_price (float): The opening price.
            close_price (float): The closing price.
            volume (float): The volume.

        Returns:
            None
        """
        # Insert and check for repeated values (upsert operation)
        upsert_query = '''
            INSERT INTO financial_data (symbol, date, open_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            open_price = VALUES(open_price),
            close_price = VALUES(close_price),
            volume = VALUES(volume)
        '''
        cursor.execute(upsert_query, (symbol, date, open_price, close_price, volume))
        conn.commit()

    for symbol in symbols:
        data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize='compact')
        # Get the last 14 days data
        recent_data = data.tail(14)

        for date, values in recent_data.iterrows():
            date = date.strftime('%Y-%m-%d')
            open_price = values['1. open']
            close_price = values['4. close']
            volume = values['6. volume']

            # Update the database
            upsert_stock_record(symbol, date, open_price, close_price, volume)

            stock_info = {
                "symbol": symbol,
                "date": date,
                "open_price": open_price,
                "close_price": close_price,
                "volume": volume
            }

            print(stock_info)

    conn.close()

except mysql.connector.Error as e:
    # Handle MySQL connection errors
    error_code = e.errno
    error_msg = e.msg
    if error_code == 1045:
        print("Error: Access denied. Check the username and password.")
    elif error_code == 1049:
        print("Error: The specified database does not exist.")
    else:
        print(f"Error: {error_msg}")
except Exception as e:
    # Handle other exceptions
    print(f"Error: {str(e)}")
