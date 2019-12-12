import matplotlib.pyplot as plt
#import numpy as np
import datetime as dt

class Dataviewer:
    def __init__(self, db):
        self.__db = db

    def plot(self):

        # The X and Y values are hard coded below . After implementing the analyzer read these values from db_analyzed database

        dates = []
        #for year in range(2012, 2014):
        plt.xlabel('Month', fontsize=14)
        plt.ylabel('Severity', fontsize=14)
        plt.title('Wells Fargo (WFC)', fontsize=24)
        #plt.figtext(0.95, 0.01, 'incident 1: tex1 tex1 tex1 tex1 tex1 tex1 tex1 tex1 tex1  incident 2: tex2 tex2 tex2 tex2 tex2 tex2 tex2 tex2 tex2', horizontalalignment='left')
        plt.grid(True)
        for month in range(1, 8):
            dates.append(dt.datetime(year=2019, month=month, day=1))

        y = [3, 5, 2, 3, 4, 5, 9]
        plt.plot(dates[:9], y, label='Incident', color='red', marker='o')
        plt.show()

