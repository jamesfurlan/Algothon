from pandas_datareader import data as web
import pandas as pd


df = pd.DataFrame()


startDate = '2010-01-01'
endDate = '2020-09-30'
# startDate = '2016-06-15'
# endDate = '2020-09-30'

df['Price'] = web.DataReader('SPY', data_source='yahoo', start=startDate, end=endDate)['Close']

i = 1
pct_change = [0]
while i < len(df['Price'].to_list()):
    pct_change.append((df['Price'][i] - df['Price'][i - 1]) / df['Price'][i - 1])
    i += 1

df['pct_change'] = pct_change

df.to_csv('2010-2020.csv')