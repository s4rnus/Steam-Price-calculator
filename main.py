from locale import resetlocale
from urllib import response
from xml.dom.minidom import Element

#

import pandas as pd
import time
import random
import requests

#

from defs import items
from defs import currencies
from defs import needed_currencies
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

rates_final = []
prices_final = []


def get_response_code ( logs ):
    driver.get_log ( "performance" )

    return logs



def find_currency_rates ( currencies ):

    response = requests.get ( currencies[0]["url"] )
    soup = BeautifulSoup ( response.content, 'xml' )

    valutes = soup.find_all ( 'Valute' )
    currency = soup.find ( 'Valute', ID = 'R01235' )
    currency_stripped = currency.Value.text

    rates_final.append ( currency_stripped )

    return rates_final



def find_prices ( items ):

    for item in items:

        try:
            driver.get ( item["url"] )
            element = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "market_commodity_orders_header_promote")))
            html_source = driver.page_source
            soup = BeautifulSoup( html_source, 'html.parser' )

            if element:

                prices = soup.find_all( 'span', class_='market_commodity_orders_header_promote' )
                price = prices[ 1 ].text.strip()
                prices_final.append( price )

        except Exception as e:
            print ( f"An error occured while parsing price: { str( e ) }" )

    return prices_final

find_currency_rates ( currencies )
find_prices ( items )

for rate in rates_final:
    print ( rate )

for price in prices_final:
    print ( price )


input( "Press Enter to close the window" )
driver.quit ()

