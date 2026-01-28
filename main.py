from locale import setlocale
from os import replace
from token import AT
from urllib import request, response
from xml.dom.minidom import Element

#

import pandas as pd
import time
import random
import requests

#

from defs import items
from defs import currencies
from defs import id_to_char
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====# imports | from's


options = Options ()
options.add_argument( "--log-level=3" )
options.add_argument( "--disable-extensions" )
options.add_argument( "--disable-blink-features=AutomationControlled" )
options.add_argument( "--disable-features=msEdgeAccountConsistency" )
options.add_argument( "--guest" )

if __name__ == "__main__":
    service = Service( executable_path="./msedgedriver.exe", log_path='NUL' )
    driver = Edge( service=service, options=options )  


#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====# settings | options


rate = 1
total_prices = []
rates_final = []
prices_final = {}


def find_currency_rates( currencies, id_to_char ):

    try:

        response = requests.get( currencies[ 0 ][ "url" ], timeout=10 )
        response.raise_for_status ()

        print(f"Response status code for currency rate parser: { response.status_code } ", "\n" )
        soup = BeautifulSoup( response.content, 'xml' )
        currency_id = id_to_char[ 0 ][ "id" ]
        valute = soup.find( 'Valute', ID=currency_id )

        rate = valute.Value.text.replace( "$", "" ).replace( ",", "." )

    except Exception as e:
        print ( f"An error occured while parsing currency rate: { str (e) }" )

    return rate


def find_prices ( items ):

    for item in items:

        item_name = list(item.keys ())[0]
        item_data = item[item_name]

        try:

            driver.get ( item_data["url"] )
            element = WebDriverWait( driver, 4 ).until( EC.presence_of_element_located(( By.CLASS_NAME, "market_commodity_orders_header_promote" )))
            html_source = driver.page_source
            soup = BeautifulSoup( html_source, 'html.parser' )

            if element:

                prices = soup.find_all( 'span', class_='market_commodity_orders_header_promote' )
                price = prices[ 1 ].text.strip().replace( "$", "" )
                prices_final[item_name] = price

            else:
                prices_final[item_name] = 0

        except Exception as e:
            print ( f"An error occured while parsing price: { str( e ) }" )

    return prices_final


def calculations (items, prices_final, rate):

    for item in items:

        item_name = list( item.keys () )[0]
        item_data = item[item_name]
        item_price = prices_final[item_name]

        try:

            total_price_RUB = round((float( item_price ) * int( item_data["amount"] ) * float( rate )),2)
            total_price_USD = float( item_price ) * int( item_data["amount"] )
            total_prices.append ( f"Total price of {item_name}: {total_price_RUB} RUB | {total_price_USD} USD" )
                
        
        except Exception( TypeError, KeyError, ValueError ) as e:

            print ( f"An error occured while processing: {item_name}: { str( e ) }" )

    return total_prices


#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====# def activations | prints


rate = find_currency_rates( currencies, id_to_char )
find_prices ( items )
total_prices = calculations( items, prices_final, rate )

print ( "USD | RUB rate: ", rate, "\n" )

for i in total_prices:
    print ( i, '\n' )

driver.quit ()

