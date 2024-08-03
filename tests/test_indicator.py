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
        plot = display.Plot()
        plot.set_stock_data(df[['Close','MAClose5']])
        plot.show('moving average')
        print(df)

    def test_close_golden_death(self):
        df = self.df.copy()
        target = 'Close'
        df=indicator.golden_death_cross(df,target=target, short=5, long=25)
        plot = display.Plot()
        slice_df = df.loc['2024-07-01':'2024-08-05']
        plot.set_golden_death_cross(slice_df)
        plot.show('Close Golden/Death')
        print(df)

    def test_vol_golden_death(self):
        df = self.df.copy()
        target = 'Volume'
        df=indicator.golden_death_cross(df,target='Volume', short=5, long=25)
        plot = display.Plot()
        plot.set_vol_golden_death_cross(df)
        plot.show('Vol Golden/Death')
        print(df)

    def test_ilmok(self):
        df = self.df.copy()
        df = indicator.ichimoku(df)
        slice_df = df.loc['2024-07-01':'2024-08-05']
        plot = display.Plot()
        plot.set_ichimoku(slice_df)
        plot.set_close(slice_df)
        plot.show('일목요연표')
        print(df)

if __name__ == '__main__':
    unittest.main()
