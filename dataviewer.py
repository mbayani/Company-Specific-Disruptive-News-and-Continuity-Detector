'''
A utility class to plot graphs. It is used to show severity of Disruptive News and the Stock price.
'''
import datetime

import matplotlib.pyplot as plt
import pandas_datareader as pdr
from matplotlib.dates import DateFormatter
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


class Dataviewer(object):
    def __init__(self, db, config):
        self.__db = db
        self.__config = config
        self.__topictowatch = config['Settings']['topic-to-watch']

    def plot(self, topic):

        x, y = self.get_data_for_graph()

        if len(x) == 0:
            print("No news from interested topic: {} Skipping the graph . PLEASE TRY AGAIN .........".format(
                self.__topictowatch))

        if len(x) > 0:
            fig, ax = plt.subplots()
            ax.plot(x, y, label="Topic: {}".format(topic), color='red', marker='o')
            fig.autofmt_xdate()
            ax.set_xlim([datetime.date(2018, 1, 1), datetime.date(2018, 6, 1)])
            plt.legend(loc="upper left")
            ax.set(xlabel="Date", ylabel="Severity (1 to 5)",
                   title="Wells Fargo (WFC)")
            date_form = DateFormatter("%m/%d")
            ax.xaxis.set_major_formatter(date_form)
            ax.set_ylim([0, 6])
            ax.grid(True)
            plt.show()

    def get_data_for_graph(self):
        # db_analyzed = TinyDB('.\data\db_analyzed.json')
        recs = self.__db.db_analyzed.all()

        X = []
        Y = []

        for rec in recs:
            if rec['topic'] == self.__topictowatch:
                Xstr = (rec['published'])[0:10]
                Xdt = datetime.datetime.strptime(Xstr, '%Y-%m-%d')
                X.append(Xdt)

                Y.append(int(rec['severity']))

        return X, Y

    def get_data(self, symbol, start_date, end_date):
        data = pdr.data.get_data_yahoo(symbol, start_date, end_date)
        close_px = data['Adj Close']
        data['mavg'] = close_px.rolling(window=1).mean()
        data['returns'] = (close_px / close_px.shift(1) - 1) * 100.0
        # data['PCT_change'] = (data['Close'] - data['Open']) / data['Open'] *100.0
        data['overnight_change'] = (data['Open'] - data['Close'].shift(1)) / data['Close'].shift(1) * 100.0
        return data[['Low', 'Open', 'Close', 'returns', 'mavg', 'overnight_change']]

    def plot_stock(self, legent):

        stock_data = self.get_data('WFC', datetime.date(2018, 1, 1), datetime.date(2018, 6, 1))

        y = []
        # print(stock_data)
        y1 = list(stock_data['Low'])

        for yf in y1:
            y.append(int(yf))

        # print(y)

        stock_data.reset_index(inplace=True, drop=False)

        x1 = list(stock_data['Date'])
        # print(x1)

        x = []
        for pd_timestap in x1:
            x.append(pd_timestap.to_pydatetime())

        # print(x)

        # print(len(x))
        # print(len(y))

        fig, ax = plt.subplots()
        ax.plot(x, y, label=legent, color='blue')
        fig.autofmt_xdate()
        ax.set_xlim([datetime.date(2018, 1, 1), datetime.date(2018, 6, 1)])
        plt.legend(loc="upper left")
        ax.set(xlabel="Date", ylabel="Price",
               title="Wells Fargo (WFC)")
        date_form = DateFormatter("%m/%d")
        ax.xaxis.set_major_formatter(date_form)
        ax.set_ylim([0, 100])
        ax.grid(True)
        plt.show()

# def main():
#     dt = Dataviewer(None)
#
#     # x, y = dt.get_data_for_graph()
#     #
#     # print(x)
#     # print(y)
#
#     dt.plot_stock()
#
# if __name__ == '__main__':
#     main()


# def main():
#     dt = Dataviewer()
#
#     # x, y = dt.get_data_for_graph()
#     #
#     # print(x)
#     # print(y)
#
#     dt.plot()
#
# if __name__ == '__main__':
#     main()
