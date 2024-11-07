import pandas as pd


def combiner(data):
    x = data.json()
    y = x.get('data').get('candles')
    df = pd.DataFrame(y, columns=['datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest'])

    # Convert the datetime column to datetime objects and set it as index
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    # Group by date and aggregate to calculate daily OHLC
    daily_ohlc = df.resample('D').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })


    return daily_ohlc
