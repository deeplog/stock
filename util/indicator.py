import pandas as pd
import numpy as np

def ma(data, window):
    res = data.rolling(window=window).mean()
    return res

def golden_death_cross(shortterm,longterm):
    '''
    shorterm은 전환상태를 확인하는 지표
    longterm은 기준지표
    Signal > 0 : 단기 > 장기
    Signal < 0 : 단기 < 장기
    '''
    df = pd.DataFrame(index=shortterm.index)
    df['Signal'] = 0
    df['Signal'] = np.where(shortterm > longterm, 1, 0)
    df['Position'] = df['Signal'].diff()
    df['Golden']=df['Position']>0
    df['Death']=df['Position']<0
    return df[['Golden','Death']]