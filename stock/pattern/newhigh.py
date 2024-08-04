def generate_buy_signals(df, lookback_period=252):
    """
    전고점 돌파 후 신고가 갱신 시 매수 신호를 생성하는 함수
    :param df: 주식 데이터 DataFrame
    :param lookback_period: 전고점 판단 기준 기간 (기본값: 252일, 약 1년)
    :return: 매수 신호가 추가된 DataFrame
    """
    df['rolling_max'] = df['High'].rolling(window=lookback_period).max()
    df['prev_high'] = df['rolling_max'].shift(1)

    # 전고점 돌파 조건
    breakout_condition = (df['High'] > df['prev_high']) & (df['High'] != df['prev_high'])

    # 신고가 갱신 조건
    new_high_condition = df['High'] == df['rolling_max']

    # 매수 신호 생성
    df['buy_signal'] = breakout_condition & new_high_condition

    return df