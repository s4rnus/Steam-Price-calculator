from locale import resetlocale

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

#

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

prices_final = []

class parser_defs ():

    def find_USD_to_RUB ( self ):

        driver.get ( rates[0]["url"] )

        try:
            element = WebDriverWait( driver, 4 ).until(EC.presence_of_element_located( 'div', class_='col-md-2 col-xs-9 _right mono-num' ))
            
        finally: 
            html_source = driver.page_source
            soup = BeautifulSoup ( html_source, 'html.parser' )

            usd_rates_pre = soup.find_all( 'div', class_='col-md-2 col-xs-9 _right mono-num' )
            usd_rate_pre = usd_rates_pre[ 3 ]
            usd_rate = usd_rate_pre.text.strip()

        return usd_rate


    def find_price ( self ):

        for item in items:
            
            driver.get ( item["url"] )

            try:
                element = WebDriverWait ( driver, 6 ).until(EC.presence_of_element_located( 'span', class_='market_commodity_orders_header_promote' ))

            finally:
                html_source = driver.page_source
                soup = BeautifulSoup ( html_source, 'html.parser' )

                prices = soup.find_all( 'span', class_='market_commodity_orders_header_promote' )
                price = prices[ 1 ].text.strip()
                prices_final.append( price )

        return prices_final

prices = parser_defs.find_price ()
rate = parser_defs.find_USD_to_RUB ()

for price in prices_final:
    print ( price )

print ( rate )

input( "Press Enter to close the window" )
driver.quit ()

