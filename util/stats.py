import pandas as pd
from yahoo_fin import stock_info
def get_real_time_price(ticker):
    '''
    실시간 주식 가격
    :param ticker:
    :return:
    '''
    try:
        return stock_info.get_live_price(ticker)
    except Exception as e:
        print(f"Error retrieving data for {ticker}: {e}")
        return None  # 혹은 적절한 기본값 설정
def summary(df):
    '''
    주식 거래 데이터를 이용하여 수익/손실등을 계산
    :param
    df: 주식 거래 데이터
    :return
    summary: 요약 통계량
    '''
    df['real_profit'] = df['sell'] * (df['price'] - df['avg_buy_price'])
    summary_df = df.groupby('ticker').agg({'buy': 'sum', 'sell': 'sum', 'real_profit': 'sum'})
    latest_prices = df.sort_values('date').groupby('ticker').last()[['avg_buy_price']]
    summary_df['avg_buy_price'] = latest_prices
    summary_df = summary_df.reset_index()
    summary_df['current_price'] = summary_df['ticker'].apply(get_real_time_price)
    summary_df['holdings'] = summary_df['buy'] - summary_df['sell']
    summary_df['potential_profit'] = (summary_df['current_price'] - summary_df['avg_buy_price']) * (summary_df['holdings'])
    columns = ['ticker', 'buy', 'sell', 'holdings', 'avg_buy_price', 'current_price', 'real_profit', 'potential_profit']
    summary_df['real_profit'] = summary_df['real_profit'].round(2)
    summary_df['potential_profit'] = summary_df['potential_profit'].round(2)
    summary_df['current_price'] = summary_df['current_price'].round(2)
    summary_df['avg_buy_price'] = summary_df['avg_buy_price'].round(2)
    return summary_df[columns]


