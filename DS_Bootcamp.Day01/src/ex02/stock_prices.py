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

def main():
    if len(sys.argv) != 2:
        return

    company_name = sys.argv[1].capitalize()

    if company_name in companies_stocks('comp').keys():
        stock_code = companies_stocks('comp').get(company_name)
        pr_ice = companies_stocks('st').get(stock_code)
        if pr_ice is not None:
            print(pr_ice)
    else:
        print("Unknown company")

if __name__ == "__main__":
    main()