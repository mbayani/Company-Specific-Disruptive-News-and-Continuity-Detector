import pandas as pd
import pandas_datareader as pdr


def get_data(symbol, from_date_str, to_date_str):
    '''
    fetches stock prices from Yahoo
    :param symbol: Stock symbol
    :param from_date_str: date as string yyyy-mm-dd
    :param to_date_str: date as string yyyy-mm-dd
    :return: pandas dataframe
    '''
    # Get data
    start_date = pd.to_datetime(from_date_str)
    end_date = pd.to_datetime(to_date_str)

    data = pdr.data.get_data_yahoo(symbol, start_date, end_date)
    close_px = data['Adj Close']
    data['mavg'] = close_px.rolling(window=10).mean()
    data['returns'] = (close_px / close_px.shift(1) - 1)*100.0
    #data['PCT_change'] = (data['Close'] - data['Open']) / data['Open'] *100.0
    return data[['Open','Close','Adj Close','returns','mavg']]

def main():
    print(get_data('WFC','2018-01-20', '2018-02-28'))


if __name__ == '__main__':
    main()