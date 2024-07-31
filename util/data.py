import yfinance as yf
def get_year_data(ticker):
    # Define the stock symbol and period
    period = "1y"

    # Fetch the stock data
    stock_data = yf.download(ticker, period=period)
    return stock_data