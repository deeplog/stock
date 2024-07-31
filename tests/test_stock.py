import unittest
from util import indicator, data, display

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


if __name__ == '__main__':
    unittest.main()
