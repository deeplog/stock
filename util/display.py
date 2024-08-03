import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 한글 폰트 경로 설정 (예: 나눔고딕)
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

class Plot:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(14, 7))

    def show(self, title='plot'):
        self.ax.set_title(title)
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price')
        self.ax.legend()
        # x축 설정
        self.ax.xaxis.set_major_locator(mdates.DayLocator())  # 주 눈금을 일 단위로 설정
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 날짜 형식 설정

        # 그리드 설정
        self.ax.grid(True, which='major', axis='x', linestyle='--', color='gray', alpha=0.7)

        self.ax.grid(True)

        # x축 레이블 회전
        plt.xticks(rotation=45, ha='right')

        # 레이아웃 조정
        plt.tight_layout()
        self.fig.show()

    def set_stock_data(self, df):
        for col in df.columns:
            self.ax.plot(df[col], label=col)

    def set_golden_death_cross(self, df):
        golden = df[df['Golden']]
        death = df[df['Death']]
        self.ax.plot(df['Close'], color='k',label='Close')
        self.ax.plot(golden['Close'], '^', markersize=10, color='r', label='Golden Cross')
        self.ax.plot(death['Close'], 'v', markersize=10, color='b', label='Death Cross')

    def set_vol_golden_death_cross(self,df):
        golden = df[df['Golden']]
        death = df[df['Death']]
        self.ax.plot(df['Close'], color='k',label='Close')
        self.ax.plot(golden['Close'], '^', markersize=10, color='r', label='Golden Cross')
        self.ax.plot(death['Close'], 'v', markersize=10, color='b', label='Death Cross')
        self.ax.legend(loc = 'upper left')

        ax2 = self.ax.twinx()
        ax2.plot(df['Volume'], color='blue',label='Volume')
        ax2.legend(loc='upper right')


    def set_ichimoku(self, df, title="일목균형표"):
        # plt.plot(df.index, df['Close'],linewidth=1, linestyle='-.', label='종가', color='black')
        self.ax.plot(df.index, df['conversion_line'], label='전환선', color='gray')
        self.ax.plot(df.index, df['base_line'], label='기준선', color='purple')
        self.ax.plot(df.index, df['leading_span_a'], label='선행스팬1', color='red')
        self.ax.plot(df.index, df['leading_span_b'], label='선행스팬2', color='blue')
        self.ax.plot(df.index, df['lagging_span'], label='후행스팬', color='orange')

        self.ax.fill_between(df.index, df['leading_span_a'], df['leading_span_b'],
                         where=df['leading_span_a'] >= df['leading_span_b'], facecolor='red', alpha=0.5)
        self.ax.fill_between(df.index, df['leading_span_a'], df['leading_span_b'],
                         where=df['leading_span_a'] < df['leading_span_b'], facecolor='blue', alpha=0.5)



    def set_close(self,df):
        self.ax.plot(df.index, df['Close'],linewidth=1, linestyle='-.', label='종가', color='black')

