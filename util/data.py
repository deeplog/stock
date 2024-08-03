import yfinance as yf
import pandas as pd
import config
def get_year_data(ticker):
    # Define the stock symbol and period
    period = "1y"

    # Fetch the stock data
    stock_data = yf.download(ticker, period=period)
    return stock_data

def process_transactions(group):
    buy_queue = []
    total_shares = 0
    total_cost = 0
    results = []
    for _, row in group.iterrows():
        if row['buy'] > 0:
            buy_queue.append((row['price'], row['buy']))
            total_shares += row['buy']
            total_cost += row['price'] * row['buy']
            avg_price = total_cost / total_shares
            results.append({
                'index': row['index'],
                'date': row['date'],
                'action': 'Buy',
                'shares': row['buy'],
                'price': row['price'],
                'avg_buy_price': avg_price
            })
        elif row['sell'] > 0:
            sell_shares = row['sell']
            sell_cost = 0
            while sell_shares > 0 and buy_queue:
                buy_price, buy_shares = buy_queue[0]
                if buy_shares <= sell_shares:
                    sell_shares -= buy_shares
                    sell_cost += buy_price * buy_shares
                    total_shares -= buy_shares
                    total_cost -= buy_price * buy_shares
                    buy_queue.pop(0)
                else:
                    buy_queue[0] = (buy_price, buy_shares - sell_shares)
                    sell_cost += buy_price * sell_shares
                    total_shares -= sell_shares
                    total_cost -= buy_price * sell_shares
                    sell_shares = 0

            avg_sell_price = sell_cost / row['sell']
            avg_price = total_cost / total_shares if total_shares > 0 else 0
            results.append({
                'index': row['index'],
                'date': row['date'],
                'action': 'Sell',
                'shares': row['sell'],
                'price': row['price'],
                'avg_buy_price': avg_sell_price
            })

    return pd.DataFrame(results)
def get_my_stocks():
    stock_df = pd.read_csv(config.myusstock)
    stock_df = stock_df.reset_index()
    results = stock_df.groupby('ticker').apply(process_transactions).reset_index(drop=False)
    stock_df = pd.merge(left=stock_df, right=results[['index', 'avg_buy_price']], how='inner', \
                  on=['index'], sort=False)
    stock_df=stock_df.set_index('index')
    return stock_df