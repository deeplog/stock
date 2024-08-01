import unittest
import pandas as pd
from util import indicator, data, display
import config
import yfinance as yf
import requests
from yahoo_fin import stock_info
from alpha_vantage.timeseries import TimeSeries
import time
from datetime import datetime


class MyTestCase(unittest.TestCase):
    def test_MA(self):
        df = data.get_year_data('NVDA')
        df['MA20']=indicator.ma(df['Close'],20)
        display.show_stock_data(df,['Close','MA20'],'moving average')

    def test_golden_death(self):
        ticker = 'NVDA'
        df = data.get_year_data(ticker)
        df['MA05'] = indicator.ma(df['Close'], 5)
        df['MA25'] = indicator.ma(df['Close'], 25)
        indi=indicator.golden_death_cross(df['MA05'],df['MA25'])
        df['Golden'] = indi['Golden']
        df['Death'] = indi['Death']
        display.show_golden_death_cross(df,title=ticker )

    def test_vol_golden_death(self):
        ticker = 'NVDA'
        df = data.get_year_data(ticker)
        df['VOL05'] = indicator.ma(df['Volume'], 5)
        df['VOL25'] = indicator.ma(df['Volume'], 25)
        indi=indicator.golden_death_cross(df['VOL05'],df['VOL25'])
        df['Golden'] = indi['Golden']
        df['Death'] = indi['Death']
        display.show_vol_golden_death_cross(df,title=ticker )


    def test_real_time_stock(self):
        ticker = yf.Ticker("NVDA")
        todays_data = ticker.history(period='1d')
        res = todays_data['Close'][0]
        print(res)
    def test_my_summary(self):
        def get_real_time_price(ticker):
            try:
                return stock_info.get_live_price(ticker)
            except Exception as e:
                print(f"Error retrieving data for {ticker}: {e}")
                return None  # 혹은 적절한 기본값 설정

        df = pd.read_csv(config.myusstock)
        df['buy_price']= df['price']*df['buy']
        df['sell_price']=df['price']*df['sell']
        summary_df = df.groupby('ticker').agg({'buy': 'sum', 'sell': 'sum', 'buy_price':'sum', 'sell_price':'sum'}).reset_index()
        summary_df['current_price'] = summary_df['ticker'].apply(get_real_time_price)
        summary_df['avg_buy_price']=summary_df['buy_price']/summary_df['buy']
        summary_df['avg_sell_price'] = summary_df['sell_price'] / summary_df['sell']
        summary_df.fillna(0, inplace=True)
        print('complete')






if __name__ == '__main__':
    unittest.main()

