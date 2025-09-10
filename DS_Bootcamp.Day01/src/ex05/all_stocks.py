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

def get_company_name(stock_code): 
    companies = companies_stocks('comp')
    return next((name for name, code in companies.items() if code == stock_code), "Unknown")


def main():
    if len(sys.argv) != 2:
        return

    expression = sys.argv[1].strip()

    if ',,' in expression:
        return
    
    if ', ,' in expression:
        return

    items = [item.strip() for item in expression.split(',')]

    for item in items:
        if not item:
            continue

        stock_code = item.upper()
        stocks = companies_stocks('st')

        if stock_code in stocks:
            company_name = get_company_name(stock_code)
            print(f"{stock_code} is a ticker symbol for {company_name}")
            continue

        company_name = item.capitalize()
        
        companies = companies_stocks('comp')
        if company_name in companies:
            stock_code = companies[company_name]
            price = stocks[stock_code]
            print(f"{company_name} stock price is {price}")
            continue

        print(f"{item} is an unknown company or an unknown ticker symbol")

if __name__ == "__main__":
    main()