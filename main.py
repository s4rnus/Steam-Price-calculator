from locale import resetlocale
from xml.dom.minidom import Element

#

import pandas as pd
import openpyxl as OP
import time
import random

#

from defs import items
from defs import rates
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====# imports | from's

options = Options()
options.add_argument( "--log-level=3" )
options.add_argument( "--disable-extensions" )
options.add_argument( "--disable-blink-features=AutomationControlled" )
options.add_argument( "--disable-features=msEdgeAccountConsistency" )
options.add_argument( "--guest" )

if __name__ == "__main__":
    service = Service( executable_path="./msedgedriver.exe", log_path='NUL' )
    driver = Edge( service=service, options=options )  

#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====# settings | options

rates = []
prices_final = []

#def get_response_code ( logs ):
#    driver.get_log ( "performance" )
#
#    return logs


def find_currency_rates ( rates ):

    try:

        driver.get ( rates[0]["url"] )
        element = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "col-md-2 col-xs-9 _right mono-num")))

        if element: 

            html_source = driver.page_source
            soup = BeautifulSoup( html_source, 'html.parser' )
    
    finally:

        rates_pre = soup.find_all( 'div', class_='col-md-2 col-xs-9 _right mono-num' )
        rate = rates_pre[ 3 ].text.strip()
        rates.append ( rate )

    return rates


def find_price ( items ):

    for item in items:

        try:

            driver.get ( item["url"] )
            element = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "market_commodity_orders_header_promote")))

            if element:
                html_source = driver.page_source
                soup = BeautifulSoup( html_source, 'html.parser' )

        finally:

            prices = soup.find_all( 'span', class_='market_commodity_orders_header_promote' )
            price = prices[ 1 ].text.strip()
            prices_final.append( price )

    return prices_final

prices = find_price (items)
rates = find_currency_rates ( rates )

for price in prices_final:
    print ( price )

print ( rates )

input( "Press Enter to close the window" )
driver.quit ()

