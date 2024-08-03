import pandas as pd
import numpy as np

def ma(df, window, col='Close'):
    colname = f'MA{col}{window}'
    df[colname] = df[col].rolling(window=window).mean()
    return df

    return res

def golden_death_cross(df, target='Close', short=5, long=25):
    '''
    shorterm은 전환상태를 확인하는 지표
    longterm은 기준지표
    Signal > 0 : 단기 > 장기
    Signal < 0 : 단기 < 장기
    '''
    short_col = f'MA{target}{short}'
    long_col = f'MA{target}{long}'
    df = ma(df, window=short, col=target)
    df = ma(df, window=long, col=target)
    df['Signal'] = 0
    df['Signal'] = np.where(df[short_col] > df[long_col], 1, 0)
    df['Position'] = df['Signal'].diff()
    df['Golden']=df['Position']>0
    df['Death']=df['Position']<0
    return df

def ichimoku(df):
    high_9 = df['High'].rolling(window=9).max()
    low_9 = df['Low'].rolling(window=9).min()
    df['conversion_line'] = (high_9 + low_9) / 2
    high_26 = df['High'].rolling(window=26).max()
    low_26 = df['Low'].rolling(window=26).min()
    df['base_line'] = (high_26 + low_26) / 2
    df['leading_span_a'] = ((df['conversion_line'] + df['base_line']) / 2).shift(26)
    high_52 = df['High'].rolling(window=52).max()
    low_52 = df['Low'].rolling(window=52).min()
    df['leading_span_b'] = ((high_52 + low_52) / 2).shift(26)
    df['lagging_span'] = df['Close'].shift(-26)
    return df