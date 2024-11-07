import cred
import intradayDataCombiner
import pandas as pd
import pandas_ta as ta
import requests


# input_CSV = cred.input
# df = pd.read_csv(input_CSV)
# # print(df.head())
# for sign in df['Symbol']:
#     print(sign)





url = 'https://api.upstox.com/v2/historical-candle/NSE_EQ%7CINE752E01010/day/2024-11-04/2024-10-25'
urltoday = 'https://api.upstox.com/v2/historical-candle/intraday/NSE_EQ%7CINE752E01010/30minute'

headers = {
    'Accept': 'application/json'
}


response = requests.get(url, headers=headers)
responsetoday = requests.get(urltoday, headers=headers)


def custom_round(value):
    remainder = value % 0.05
    if remainder >= 0.03:
        return round(value + (0.05 - remainder), 2)
    else:
        return round(value - remainder, 2)

if response.status_code == 200:
    print("Daily")
else:
    print(f"Error: {response.status_code} - {response.text}")


today_OLHC = intradayDataCombiner.combiner(responsetoday)


x = response.json()
y = x.get('data').get('candles')
df = pd.DataFrame(y, columns=['datetime', 'open',
                  'high', 'low', 'close', 'volume', 'openinterest'])
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)
df.drop(columns=["openinterest"], inplace=True)


df_combined = pd.concat([today_OLHC, df], ignore_index=True)
df_combined = df_combined.iloc[::-1].reset_index(drop=True)


ha = ta.ha(
    df_combined['open'],
    df_combined['high'],
    df_combined['low'],
    df_combined['close'],
).round(2)


df_combined[['HA_Open', 'HA_High', 'HA_Low',
             'HA_Close']] = ha.applymap(custom_round)


print(df_combined.to_string())
