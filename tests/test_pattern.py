import unittest
from stock.util import data, display
from stock.pattern import newhigh, box, pullback


class BoxTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ticker = "005930.KS"  # 삼성전자 주식 코드
        self.start_date = "2024-01-01"
        self.end_date = "2024-08-01"
        self.df = data.get_stock_data(self.ticker, self.start_date, self.end_date)
    def test_box(self):
        df = self.df.copy()
        df = box.identify_boxed_range(df)
        self.assertTrue('complete')
    def test_box_breakout(self):
        df = self.df.copy()
        df = box.identify_boxed_range(df)
        df = box.identify_breakout(df)
        self.assertTrue('complete')

    def test_box_breakout_plot(self):
        df = self.df.copy()
        title = 'box권 돌파/매수시점'
        save_path = 'test_output/box_pattern.png'
        df = box.identify_boxed_range(df)
        df = box.identify_breakout(df)
        plot = display.Plot(df, '2024-03-01', '2024-04-01')
        plot.box_pattern(title,save_path)
        self.assertTrue('complete')

class NewHighTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ticker = "NVDA"  # 삼성전자 주식 코드
        self.start_date = "2023-01-01"
        self.end_date = "2024-08-01"
        self.df = data.get_stock_data(self.ticker, self.start_date, self.end_date)
    def test_newhigh(self):
        df = self.df.copy()
        df = newhigh.generate_buy_signals(df)
        self.assertTrue('complete')

    def test_plot_newhigh(self):
        df = self.df.copy()
        df = newhigh.generate_buy_signals(df)

        self.assertTrue('complete')

class PullBackTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ticker = "NVDA"  # 삼성전자 주식 코드
        self.start_date = "2023-01-01"
        self.end_date = "2024-08-01"
        self.df = data.get_stock_data(self.ticker, self.start_date, self.end_date)

    def test_pullback(self):
        df = self.df.copy()
        df = pullback.pullback(df)
        self.assertTrue('complete')


if __name__ == '__main__':
    unittest.main()
