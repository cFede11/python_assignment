import sqlite3
from alpha_vantage.timeseries import TimeSeries
import os

#getAPI KEY for alpha vantage
api_key = os.environ.get('AV_API_KEY')

#check if the API key is available
if api_key is None:
    raise ValueError('AV_API_KEY environment variable is not set')

ts = TimeSeries(key=api_key, output_format='pandas')

#symbols to be used
symbols = ['IBM', 'AAPL']

conn = sqlite3.connect('schema.db')
cursor = conn.cursor()

# Create financial_data
create_table_query = '''
    CREATE TABLE IF NOT EXISTS financial_data (
        symbol TEXT,
        date TEXT,
        open_price REAL,
        close_price REAL,
        volume INTEGER,
        PRIMARY KEY (symbol, date)
    )
'''
cursor.execute(create_table_query)
conn.commit()

def upsert_stock_record(symbol, date, open_price, close_price, volume):

    #insert and check for repeated values (upsert operation)
    upsert_query = '''
        INSERT INTO financial_data (symbol, date, open_price, close_price, volume)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(symbol, date) DO UPDATE SET
        open_price = excluded.open_price,
        close_price = excluded.close_price,
        volume = excluded.volume
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

        #update the db
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