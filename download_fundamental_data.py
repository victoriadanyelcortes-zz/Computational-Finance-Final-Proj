'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : Victoria Cortes

https://github.com/JECSand/yahoofinancials

'''

import pandas as pd

from utils import MyYahooFinancials 


def download_fundamental_data(input_file_name, output_file_name):
    '''

    '''
    # read in input_file using read_csv
    df = pd.read_csv(input_file_name)
    # for each symbol in input file, get the financial data from yfinance
    for ind in df.index:
        symbol = df['Symbol'][ind]
        yfinance = MyYahooFinancials(symbol)
        df['Market Cap'][ind] = yfinance.get_market_cap()
        df['P/E Ratio'][ind] = yfinance.get_pe_ratio()
        df['Beta'][ind] = yfinance.get_beta()
        try:
            total_assets = yfinance._financial_statement_data('balance', 'balanceSheetHistory', 'totalAssets', 'annual')
        except:
            total_assets = "N/A"
            
        df['Total Assets'][ind] = total_assets
                
        try:
            cap_expend = yfinance.get_capital_expenditures()
            op_cash_flow = yfinance.get_operating_cashflow()
            fcf = cap_expend + op_cash_flow
        except:
            try:
                fcf = yfinance.get_operating_cashflow()
            except:
                fcf = "N/A"
        df['Free Cash Flow'][ind] = fcf
        total_debt = "N/A";
        try:
            total_debt = yfinance.get_total_current_liabilities()
        except:
            print("No current liabilities")
        try:
            total_debt = total_debt - yfinance.get_account_payable()
        except:
            print("No accounts payable")
        try:
            total_debt = total_debt - yfinance.get_other_current_liabilities()
        except:
            print("No other current liabilities")
            
        try:
            total_debt += yfinance.get_long_term_debt()
        except:
            print("No long term debt")
        
        df['Total Debts'][ind] = total_debt
    
    
    #  write to output file
    df.to_csv(output_file_name)
    # end TODO



def run():
    input_fname = "StockUniverse.csv"
    output_fname = "StockUniverseWithData.csv"

    download_fundamental_data(input_fname, output_fname)

    
if __name__ == "__main__":
    run()
