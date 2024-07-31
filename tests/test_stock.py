import unittest
from util import indicator, data, display

class MyTestCase(unittest.TestCase):
    def test_MA(self):
        df = data.get_year_data('NVDA')
        df['MA20']=indicator.ma(df['Close'],20)
        display.show_stock_data(df,['Close','MA20'],'moving average')

if __name__ == '__main__':
    unittest.main()
