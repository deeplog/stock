from util import data, stats
from datetime import datetime

class DailyBatch:
    def main(self):
        self.make_summary()
        print('daily batch completed')
    def make_summary(self):
        df = data.get_my_stocks()
        summary_df = stats.summary(df)
        today = datetime.today().strftime("%Y%m%d")
        summary_df.to_csv(f'../data/{today}_summary.csv')


if __name__=="__main__":
    batch = DailyBatch()
    batch.main()