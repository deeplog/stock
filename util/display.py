import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

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

    def plot_counterclock(self,df, title="역시계곡선"):
        '''
        역시계 곡선
        :param df:
        :return:
        '''
        days = df.index
        price = df['Close']
        volume = df['Volume']

        points = np.array([volume, price]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # 시간에 따른 색상 변화를 위한 설정
        cmap = plt.get_cmap('coolwarm')
        norm = plt.Normalize(mdates.date2num(days[0]), mdates.date2num(days[-1]))
        colors = cmap(norm(mdates.date2num(days)))

        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(mdates.date2num(days))
        lc.set_linewidth(2)

        line = self.ax.add_collection(lc)
        self.ax.set_xlim(volume.min(), volume.max())
        self.ax.set_ylim(price.min(), price.max())

        self.ax.set_xlabel('거래량')
        self.ax.set_ylabel('주가')
        self.ax.set_title(title)

        # 컬러바 추가 (10일 간격으로 날짜 표시)
        cbar = self.fig.colorbar(line, ax=self.ax)
        cbar.set_label('날짜')
        cbar.ax.yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        cbar.ax.yaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(cbar.ax.yaxis.get_majorticklabels(), rotation=0, ha='right')

        # 시작점과 끝점 표시
        self.ax.scatter(volume[0], price[0], color='green', s=100, label='시작')
        self.ax.scatter(volume[-1], price[-1], color='red', s=100, label='끝')
        self.ax.legend()

        plt.tight_layout()
        plt.show()



    def set_close(self,df):
        self.ax.plot(df.index, df['Close'],linewidth=1, linestyle='-.', label='종가', color='black')

