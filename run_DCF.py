'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : first last

'''

import pandas as pd
import datetime

from stock import Stock
from discount_cf_model import DiscountedCashFlowModel

def run():
    input_fname = "StockUniverse.csv"
    output_fname = "StockUniverseWithDCF.csv"

    as_of_date = datetime.date(2021, 6, 15)
    df = pd.read_csv(input_fname)
    
    # TODO
    results = []
    for ind in df.index:
        
        try:
            symbol = df['Symbol'][ind]
            stock = Stock(symbol, 'annual')
            model = DiscountedCashFlowModel(stock, as_of_date)

            short_term_growth_rate = float(df['EPS Next 5Y'][ind])/100

            medium_term_growth_rate = short_term_growth_rate/2
            long_term_growth_rate = 0.04

            model.set_FCC_growth_rate(short_term_growth_rate, medium_term_growth_rate, long_term_growth_rate)
        
            fair_value = model.calc_fair_value()
            print(symbol, fair_value)
        except:
            print("Not included for comparison")
    # ....
    
    # end TODO

    
if __name__ == "__main__":
    run()
