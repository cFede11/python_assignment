CREATE TABLE IF NOT EXISTS financial_data (
    symbol TEXT(255),
    date DATE,
    open_price REAL,
    close_price REAL,
    volume INTEGER,
    PRIMARY KEY (symbol(255), date)
);

