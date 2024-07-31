def ma(data, window):
    res = data.rolling(window=window).mean()
    return res
