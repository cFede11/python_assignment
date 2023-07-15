import mysql.connector
from alpha_vantage.timeseries import TimeSeries
import os

#get API KEY for Alpha Vantage
api_key = os.environ.get('AV_API_KEY')

#check if the API key is available
if api_key is None:
    raise ValueError('AV_API_KEY environment variable is not set')

#initialize Alpha Vantage
ts = TimeSeries(key=api_key, output_format='pandas')

#symbols to be used
symbols = ['META']  # MSFT  symbols = ['IBM', 'AAPL']

try:
    #connect to the MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='admin',
        password='admin',
        database='test1'
    )

    cursor = conn.cursor()

    def upsert_stock_record(symbol, date, open_price, close_price, volume):
        #insert and check for repeated values (upsert operation)
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
        #get the last 14 days data
        recent_data = data.tail(14)

        for date, values in recent_data.iterrows():
            date = date.strftime('%Y-%m-%d')
            open_price = values['1. open']
            close_price = values['4. close']
            volume = values['6. volume']

            #update the database
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
    #handle MySQL connection errors
    error_code = e.errno
    error_msg = e.msg
    if error_code == 1045:
        print("Error: Access denied. Check the username and password.")
    elif error_code == 1049:
        print("Error: The specified database does not exist.")
    else:
        print(f"Error: {error_msg}")
except Exception as e:
    #handle other exceptions
    print(f"Error: {str(e)}")
