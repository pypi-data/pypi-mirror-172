from thefirstock.firstockModules.timePriceSeriesFunctionality.functions import *


class FirstockTimePriceSeries:
    def __init__(self, exch, token, et, st, intrv):
        self.timePriceSeries = ApiRequests()

        self.exch = exch
        self.token = token
        self.et = et
        self.st = st
        self.intrv = intrv

    def firstockTimePriceSeries(self):
        result = self.timePriceSeries.firstockTimePriceSeries(self.exch, self.token, self.st, self.et, self.intrv)
        return result
