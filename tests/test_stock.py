import unittest
from stock.util import data, stats
import yfinance as yf

class MyTestCase(unittest.TestCase):
    def test_real_time_stock(self):
        ticker = yf.Ticker("NVDA")
        todays_data = ticker.history(period='1d')
        res = todays_data['Close'][0]
        print(res)
    def test_summary(self):
        df = data.get_my_stocks()
        summary_df = stats.summary(df)
        self.assertTrue('completed')

    def test_get_mystock(self):
        df = data.get_my_stocks()
        self.assertTrue('completed')


if __name__ == '__main__':
    unittest.main()

