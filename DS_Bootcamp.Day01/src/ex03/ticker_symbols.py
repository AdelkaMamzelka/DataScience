#!/usr/bin/env python3

import sys

def companies_stocks(data):
    COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
    }

    STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90,
    'TSLA': 724.88,
    'NOK': 3.37
    }

    if data == 'comp':
        return COMPANIES
    elif data == 'st':
        return STOCKS

def main ():
    if len(sys.argv) != 2:
        return
    
    ticker_symbol = sys.argv[1].upper() #привести к верхнему регистру
    
    if ticker_symbol in companies_stocks('st').keys():
        company_name = next((name for name, symbol in companies_stocks('comp').items() if symbol == ticker_symbol), None)
    pr_ice = companies_stocks('st').get(ticker_symbol)
    if pr_ice is not None:
      print(f"{company_name} {pr_ice}")
    else:
        print("Unknown ticker")

if __name__ == "__main__":
    main()