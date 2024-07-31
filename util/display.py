import matplotlib.pyplot as plt
def show_stock_data(df, colnames, title='stock data'):
    plt.figure(figsize=(14, 7))
    for col in colnames:
        plt.plot(df[col], label=col)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()