'''
It pulls stock prices from yahoo using pandas library.
'''
import datetime
from datetime import timedelta

import pandas_datareader as pdr
from dateutil.parser import parse


def get_data(symbol, event_date, days_before=1, days_after=1):
    '''
    fetches stock prices from Yahoo
    :param symbol: Stock symbol
    :param from_date_str: date as string yyyy-mm-dd
    :param to_date_str: date as string yyyy-mm-dd
    :return: pandas dataframe
    '''
    dt = event_date
    if isinstance(event_date, str):
        dt = parse(event_date)
    start_date = dt - timedelta(days=days_before)
    end_date = dt + timedelta(days=days_after)
    print('')
    print('Getting data[symbol=%s, start date=%s, end date=%s]' % (symbol, start_date, end_date))
    data = pdr.data.get_data_yahoo(symbol, start_date, end_date)
    close_px = data['Adj Close']
    data['mavg'] = close_px.rolling(window=1).mean()
    data['returns'] = (close_px / close_px.shift(1) - 1) * 100.0
    # data['PCT_change'] = (data['Close'] - data['Open']) / data['Open'] *100.0
    data['overnight_change'] = (data['Open'] - data['Close'].shift(1)) / data['Close'].shift(1) * 100.0
    return data[['Open', 'Close', 'returns', 'mavg', 'overnight_change']]

if __name__ == '__main__':
    print(get_data('WFC', '2018-01-20'))
    print(get_data('WFC', datetime.date(2018, 1, 20)))
    print(get_data('WFC', datetime.date(2018, 1, 20), 5, 5))
