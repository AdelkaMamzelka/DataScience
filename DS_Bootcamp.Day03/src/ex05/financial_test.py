#!/usr/bin/env python3

import re
import sys
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import pytest


def test_get_total_revenue():
  html = get_response("MSFT")
  result = parse_page(html, "Total Revenue")
  assert 'Total Revenue' == result[0]

def test_is_result_tuple():
  html = get_response("MSFT")
  result = parse_page(html, "Total Revenue")
  isinstance(result, tuple)

def test_get_response_invalid_ticker_returns_empty():
  html = get_response("INVALIDTICKER")
  assert "<html" in html.lower()
  assert "INVALIDTICKER" not in html

def test_get_response_returns_html_for_valid_ticker():
  html = get_response("AAPL")
  assert "<html" in html.lower()

def test_get_response_returns_string_type():
  html = get_response("AAPL")
  assert isinstance(html, str)

def test_parse_page_returns_correct_tuple():
  html = '''
  <div class="row lv-0 yf-t22klz">
    <div class="rowTitle yf-t22klz">Общий доход</div>
    <div class="column yf-t22klz">1000</div>
    <div class="column yf-t22klz alt">2000</div>
  </div>
  '''
  result = parse_page(html, "Общий доход")
  expected = ("Общий доход", "1000", "2000")
  assert result == expected

def test_parse_page_breakdown_not_found():
  html = '''
  <div class="row lv-0 yf-t22klz">
    <div class="rowTitle yf-t22klz">Другое</div>
    <div class="column yf-t22klz">123</div>
  </div>
  '''
  with pytest.raises(Exception):
    parse_page(html, "Не существующий разбивка")



def get_response(ticker):
  # driver service settings
  chrome_options = Options()
  chrome_options.add_argument("--disable-enable-automation")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")  # Optional for Linux
  chrome_options.add_argument("--disable-dev-shm-usage")  # Optional for Linux
  service = Service(ChromeDriverManager().install())
  # driver settings
  driver = webdriver.Chrome(service=service, options=chrome_options)
  
  try:
    url = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"
    driver.execute_cdp_cmd('Emulation.setScriptExecutionDisabled', {'value': True})
    driver.get(url)
    html_content = driver.page_source

    if "noData yf-wnifss" in html_content:
      raise Exception("Unknown ticker")
    
  except Exception as e:
    print(f"An error occurred: {e}")
    html_content = ""
  finally:
    driver.quit() 
  return html_content


def parse_page(html, breakdown):
  soup = BeautifulSoup(html, "html.parser")
  breakdowns = soup.find_all("div", class_="row lv-0 yf-t22klz")
  breakdown_flag = 0
  res = []
  for item in breakdowns:
    title = item.find("div", class_="rowTitle yf-t22klz").text
    if title == breakdown:
      breakdown_flag = 1
      res.append(title)
      stats = item.find_all("div", class_=re.compile(r"column yf-t22klz( alt)?"))
      for stat in stats:
        res.append(stat.text.strip(" "))
      print(tuple(res))
      break
  if not breakdown_flag:
    raise Exception("Breakdown or ticker not found")
  return tuple(res)


def main():
  try:
    if len(sys.argv) != 3:
      raise Exception("Incorrect count of arguments. Try [py_script] [ticker] [breakdown]")
    field = sys.argv[2]
    ticker = sys.argv[1]
    html_content = get_response(ticker)
    # time.sleep(5)
    parse_page(html_content, field)
  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  main()