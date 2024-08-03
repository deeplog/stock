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