'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Victoria Cortes

@Date          : June 2021


'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

import datetime 
from scipy.stats import norm

from math import log, exp, sqrt

from utils import MyYahooFinancials 

class Stock(object):
    '''
    Stock class for getting financial statements as well as pricing data
    '''
    def __init__(self, symbol, spot_price = None, sigma = None, dividend_yield = 0, freq = 'annual'):
        self.symbol = symbol
        self.spot_price = spot_price
        self.sigma = sigma
        self.dividend_yield = dividend_yield
        self.yfinancial = MyYahooFinancials(symbol, freq)
        self.ohlcv_df = None        

    def get_daily_hist_price(self, start_date, end_date):
        '''
        Get historical OHLCV pricing dataframe
        '''
        #TODO
        info = self.yfinancial.get_historical_price_data(start_date, end_date, 'daily')
        self.ohlcv_df = pd.DataFrame(info[self.symbol]['prices'])
        #end TODO
        
    def calc_returns(self):
        '''
        '''
        self.ohlcv_df['prev_close'] = self.ohlcv_df['close'].shift(1)
        self.ohlcv_df['returns'] = (self.ohlcv_df['close'] - self.ohlcv_df['prev_close'])/ \
                                        self.ohlcv_df['prev_close']


    # financial statements related methods
    
    def get_total_debt(self):
        '''
        compute total_debt as long term debt + current debt 
        current debt = total current liabilities - accounts payables - other current liabilities (ignoring current deferred liabilities)
        '''
        result = None
        current_debt = None
        long_term_debt = None
        # TODO
        try:
            result = self.yfinancial.get_total_current_liabilities()
        except:
            print("No current liabilities")
            
        try:
            result -= self.yfinancial.get_account_payable()
        except:
            print("No accounts payable")
        
        try:
            result -= self.yfinancial.get_other_current_liabilities()
        except:
            print("No other current liabilities")
        
        try:
            result += self.yfinancial.get_long_term_debt()
        except:
            print("No long term debt")
        
        #result = long_term_debt + current_debt
        # end TODO
        return(result)

    def get_free_cashflow(self):
        '''
        get free cash flow as operating cashflow + capital expenditures (which will be negative)
        '''
        result = None
        # TODO
        try:
            cap_exp = self.yfinancial.get_capital_expenditures()
            op_cf = self.yfinancial.get_operating_cashflow()
            result = cap_exp + op_cf
        except:
            try:
                result = self.yfinancial.get_operating_cashflow()
            except:
                print("No free cashflow to report")
        # end TODO
        return(result)

    def get_cash_and_cash_equivalent(self):
        '''
        Return cash plus short term investment 
        '''
        result = None
        # TODO
        try:
            result = self.yfinancial.get_cash()
        except:
            print("No cash")
            
        try:
            result = result + self.yfinancial.get_short_term_investments()
        except:
            print("No short term investments")
        # end TODO
        return(result)

    def get_num_shares_outstanding(self):
        '''
        get current number of shares outstanding from Yahoo financial library
        '''
        result = None
        # TODO
        try:
            result = self.yfinancial.get_num_shares_outstanding()
        except:
            print("Not Available")
        # end TODO
        return(result)

    def get_beta(self):
        '''
        get beta from Yahoo financial
        '''
        result = None
        # TODO
        try:
            result = self.yfinancial.get_beta()
        except:
            print("No beta to report")
        # end TODO
        return(result)

    def lookup_wacc_by_beta(self, beta):
        '''
        lookup wacc by using the table in Slide 15 of the DiscountedCashFlowModel lecture powerpoint
        '''
        result = None
        # TODO:
        if beta < .80:
            result = .05
        elif beta >= .80 and beta < 1:
            result = .06
        elif beta >=1 and beta < 1.1:
            result = .065
        elif beta >= 1.1 and beta < 1.2:
            result = .07
        elif beta >= 1.2 and beta < 1.3:
            result = .075
        elif beta >= 1.3 and beta < 1.5:
            result = .08
        elif beta >= 1.5 and beta < 1.6:
            result = .085
        else:
            result = .09
        #end TODO
        return(result)
        



def _test():
    symbol = 'AAPL'

    stock = Stock(symbol, 'annual')
    beta = stock.get_beta();
    print(beta)
    wacc = stock.lookup_wacc_by_beta(beta)
    print(wacc)
    shares_out = stock.get_num_shares_outstanding()
    print(shares_out)
    start_date = '2019-08-06'
    end_date = '2020-08-06'
    stock.get_daily_hist_price(start_date, end_date)    




if __name__ == "__main__":
    _test()
