import unittest
from util import data
from chart import basic
from pattern import newhigh
class ChartTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ticker = "005930.KS"  # 삼성전자 주식 코드
        self.start_date = "2023-7-1"
        self.end_date = "2024-08-01"
        self.df = data.get_stock_data(self.ticker,self.start_date,self.end_date)

    def test_candle(self):
        basic.candlestick_chart(self.df)
        self.assertTrue('complete')

    def test_newhighchart(self):
        df = newhigh.generate_buy_signals(self.df)
        basic.newhigh_chart(df)
        self.assertTrue('complete')


if __name__ == '__main__':
    unittest.main()
