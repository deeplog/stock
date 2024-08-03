import unittest
from util import display, data, indicator

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ticker = 'NVDA'
        self.col = 'Close'
        self.df = data.get_year_data(self.ticker)
    def test_MA(self):
        df = self.df.copy()
        window = 5
        ma_col = f'MA{self.col}{window}'
        df = indicator.ma(df,window)
        df = df[[self.col,ma_col]]
        display.show_stock_data(df, title='moving average')

    def test_close_golden_death(self):
        df = self.df.copy()
        target = 'Close'
        df=indicator.golden_death_cross(df,target=target, short=5, long=25)
        display.show_golden_death_cross(df,title=f'{self.ticker}_{target}')

    def test_vol_golden_death(self):
        df = self.df.copy()
        target = 'Volume'
        df=indicator.golden_death_cross(df,target='Volume', short=5, long=25)
        display.show_golden_death_cross(df,title=f'{self.ticker}_{target}')

if __name__ == '__main__':
    unittest.main()
