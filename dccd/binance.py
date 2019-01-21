#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" 
Binance exchange class to download data. 

"""

# Import built-in packages
import os
import pathlib
import time

# Import extern packages
import requests
import json

# Import local packages
from dccd.time_tools import TimeTools
from dccd.exchange import ImportDataCryptoCurrencies

__all__ = ['FromBinance']

class FromBinance(ImportDataCryptoCurrencies):
    """ 
    Binance class to import crypto-currencies data.

    Methods
    -------
    - save : Save data by period (default is year) in the corresponding
        format and file. TO FINISH
    - get_data : Print the dataframe. 
    - set_hierarchy : You can determine the specific hierarchy of the files 
        where will save your data. TO FINISH
    - import_data : Download data since a specified date.

    Attributes
    ----------
    TO LIST
    
    """
    def __init__(self, path, crypto, span, fiat='USD', form='xlsx'):
        """ 
        Parameters
        ----------
        :path: str
            The path where data will be save.
        :crypto: str
            The abreviation of the crypto-currencie.
        :span: str ot int
            'weekly', 'daily', 'hourly', or the integer of the seconds 
            between each observations. Min 60 seconds.
        :fiat: str
            A fiat currency or a crypto-currency. Binance don't allow fiat 
            currencies, but USD theter.
        :form: str 
            Your favorit format. Only 'xlsx' for the moment.
        """
        if fiat in ['EUR', 'USD']:
            print("Binance don't allow fiat currencies, the equivalent of US dollar is Tether USD as USDT.")
            self.fiat = fiat = 'USDT'
        if crypto is 'XBT':
            crypto = 'BTC'
        ImportDataCryptoCurrencies.__init__(self, path, crypto, span, 'GDAX', fiat, form)
        self.pair = crypto + fiat
        self.full_path = self.path + '/Binance/Data/Clean_Data/' + str(self.per) + '/' + str(self.crypto) + str(self.fiat)
        
    
    def import_data(self, start = 'last', end = 'now'):
        """ Download data from Binance for specific time interval
        
        :start: int
            Timestamp of the first observation of you want.
        :end: int
            Timestamp of the last observation of you want.
        
        """
        self.start, self.end = self._time(start, end)
        param = {
            'symbol' : self.pair,
            'startTime': self.start * 1000,
            'endTime': self.end * 1000,
            'interval': self.tools.binance_interval(self.span),
        }
        r = requests.get('https://api.binance.com/api/v1/klines', param)
        text = json.loads(r.text)
        print(param)
        print(text)
        data = [{'date': float(e[0] / 1000), 'open': float(e[1]), 
                 'high': float(e[2]), 'low': float(e[3]), 'close': float(e[4]), 
                 'volume': float(e[5]), 'quoteVolume': float(e[7])} for e in text]
        return self._sort_data(data)