def identify_boxed_range(df, window=20, threshold=0.05):
    """
    박스권을 식별하는 함수
    :param df: 주식 데이터 DataFrame
    :param window: 롤링 윈도우 크기
    :param threshold: 박스권 판단 임계값
    :return: 박스권이 식별된 DataFrame
    """
    df['rolling_high'] = df['High'].rolling(window=window).max()
    df['rolling_low'] = df['Low'].rolling(window=window).min()
    df['range'] = (df['rolling_high'] - df['rolling_low']) / df['rolling_low']
    df['is_boxed'] = df['range'] < threshold
    return df

def identify_breakout(df, breakout_threshold=0.02):
    """
    박스권 돌파를 식별하는 함수
    :param df: 전체 주식 데이터 DataFrame
    :param breakout_threshold: 돌파 판단 임계값
    :return: 돌파 시점이 표시된 DataFrame
    """
    boxed_range = df[df['is_boxed']]
    if not boxed_range.empty:
        last_boxed_date = boxed_range.index[-1]
        last_boxed_high = boxed_range['High'].max()

        df['breakout'] = False
        df['buy_signal'] = False
        df.loc[(df.index > last_boxed_date) & (df['Close'] > last_boxed_high * (1 + breakout_threshold)), 'breakout'] = True

        first_breakout = df[df['breakout']].first_valid_index()
        if first_breakout:
            df.loc[first_breakout, 'buy_signal'] = True

    return df