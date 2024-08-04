def pullback(df, ma_period=20, threshold=0.03):
    # 이동평균 계산
    df['MA'] = df['Close'].rolling(window=ma_period).mean()

    # 상승 추세 확인 (현재 주가가 이동평균보다 높은지)
    df['Uptrend'] = df['Close'] > df['MA']

    # 눌림목 확인 (주가가 이동평균 근처로 내려왔는지)
    df['Pullback'] = (df['Close'] - df['MA']) / df['MA'] < threshold

    # 매수 신호 생성
    df['Buy_Signal'] = df['Uptrend'] & df['Pullback']

    return df