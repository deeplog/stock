import matplotlib.pyplot as plt
def show_stock_data(df, title='stock data'):
    plt.figure(figsize=(14, 7))
    for col in df.columns:
        plt.plot(df[col], label=col)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def show_golden_death_cross(df, title='golden/death cross'):
    plt.figure(figsize=(14, 7))
    golden = df[df['Golden']]
    death = df[df['Death']]

    #plt.plot(df['MA05'], color='r', label='MA05')
    #plt.plot(df['MA25'], color='b', label='MA25')
    plt.plot(df['Close'], color='k',label='Close')
    plt.plot(golden['Close'], '^', markersize=10, color='r', label='Golden Cross')
    plt.plot(death['Close'], 'v', markersize=10, color='b', label='Death Cross')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def show_vol_golden_death_cross(df, title='golden/death cross'):
    fig, ax1 = plt.subplots(figsize=(14, 7))
    golden = df[df['Golden']]
    death = df[df['Death']]

    #ax1.plot(df['VOL05'], color='r', label='VOL05')
    #ax1.plot(df['VOL25'], color='b', label='VOL25')
    ax1.legend(loc = 'upper left')
    ax1.set_ylabel('Volume')

    ax2 = ax1.twinx()
    ax2.plot(df['Close'], color='k',label='Close')
    ax2.plot(golden['Close'], '^', markersize=10, color='r', label='Golden Cross')
    ax2.plot(death['Close'], 'v', markersize=10, color='b', label='Death Cross')
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Price')

    plt.title(title)
    plt.xlabel('Date')
    plt.grid(True)
    plt.show()