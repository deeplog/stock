import pandas as pd
import numpy as np
import mplfinance as mpf
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()

def newhigh_chart(df, title='신고가 챠트'):
    '''
    신고가 데이터를 이용해서 매수가를 표현해주는 차트
    :param df:
    :param title:
    :return:
    '''
    df_plot = df.copy()
    df_plot.index.name = 'Date'
    # 매수 신호를 표시하기 위한 마커 생성
    buy_signals = df_plot[df_plot['buy_signal'] == True]

    # 모든 날짜에 대해 매수 신호 데이터 생성 (신호가 없는 날은 NaN)
    buy_signal_data = pd.Series(np.where(df_plot['buy_signal'], df_plot['Low'], np.nan), index=df_plot.index)

    if all(buy_signal_data.isna()):
        markers = []
    else:
        markers = [
            mpf.make_addplot(buy_signal_data, type='scatter', markersize=50, marker='*', color='r'),
        ]

    candlestick_chart(df_plot,'신고가차트', markers)
def candlestick_chart(df, title='candle chart', markers=[]):
    """
    캔들 차트를 그리고 매수 신호를 표시하는 함수
    :param df: 분석 결과가 포함된 DataFrame
    """

    style = mpf.make_mpf_style(base_mpf_style='yahoo', rc={'font.family': font_name, 'figure.figsize': (12, 8)})

    # 날짜 형식 지정
    date_format = '%Y-%m-%d'

    # 캔들 차트 그리기
    mpf.plot(df, type='candle', style=style,
             title=title,
             volume=False,
             figscale=1.5,
             datetime_format=date_format,
             addplot=markers,
             show_nontrading=True)