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
        df = df[['Close', 'MAClose5']]
        plot = display.Plot(df, '2024-07-01', '2024-08-05')
        plot.stock_data('moving average')
        plot.fig.savefig('test_output/ma.png')

    def test_close_golden_death(self):
        df = self.df.copy()
        df=indicator.golden_death_cross(df,target='Close', short=5, long=25)
        plot = display.Plot(df, '2024-07-01', '2024-08-05')
        plot.golden_death_cross('test_output/close_golden_death.png')

    def test_vol_golden_death(self):
        df = self.df.copy()
        target = 'Volume'
        df=indicator.golden_death_cross(df,target='Volume', short=5, long=25)
        plot = display.Plot(df, '2024-07-01', '2024-08-05')
        plot.vol_golden_death_cross('volume golden cross')
        plot.fig.savefig('test_output/vol_golden_death.png')

    def test_ilmok(self):
        df = self.df.copy()
        df = indicator.ichimoku(df)
        plot = display.Plot(df, '2024-07-01', '2024-08-05')
        plot.ichimoku()
        plot.fig.savefig('test_output/ilmok.png')

    def test_counterclock(self):
        df = self.df.copy()
        df = indicator.ma(df, 20)
        df['Price']=df['MAClose20']
        plot = display.Plot(df, '2024-05-01', '2024-08-05')
        plot.counterclock(title='20일 이동평균 역시계곡선')
        plot.fig.savefig('test_output/역시계곡선.png')


if __name__ == '__main__':
    unittest.main()
