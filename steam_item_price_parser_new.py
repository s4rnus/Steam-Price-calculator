#

import time
import random
import pandas as pd
import openpyxl as OP
import phantomjs
import bs4
import pathlib

#

from importlib.metadata import requires
from pathlib import Path
from locale import resetlocale
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from openpyxl import Workbook
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

items = [
    { "name": "Gamma 2 Case", "url": "https://steamcommunity.com/market/listings/730/Gamma%202%20Case", "bfp": "L3"},
    { "name": "Stockholm 2021 Legends Sticker Capsule", "url": "https://steamcommunity.com/market/listings/730/Stockholm%202021%20Legends%20Sticker%20Capsule", "bfp": "L4"},
    { "name": "Fracture Case", "url": "https://steamcommunity.com/market/listings/730/Fracture%20Case", "bfp": "L5"},
    { "name": "Revolution Case", "url": "https://steamcommunity.com/market/listings/730/Revolution%20Case?ysclid=mcjgbqzeed990445279", "bfp": "L6"},
    { "name": "Dreams & Nightmares Case", "url": "https://steamcommunity.com/market/listings/730/Dreams%20%26%20Nightmares%20Case", "bfp": "L7"},
    { "name": "Recoil Case", "url": "https://steamcommunity.com/market/listings/730/Recoil%20Case", "bfp": "L8"},
    { "name": "Kilowatt Case", "url": "https://steamcommunity.com/market/listings/730/Kilowatt%20Case", "bfp": "L9"},
    { "name": "Snakebite Case", "url": "https://steamcommunity.com/market/listings/730/Snakebite%20Case", "bfp": "L10"},
    { "name": "Operation Phoenix Weapon Case", "url": "https://steamcommunity.com/market/listings/730/Operation%20Phoenix%20Weapon%20Case", "bfp": "L11"},
    ]

rates = [
    { "name": "USD/RUB", "url": "https://cbr.ru", "bfr": "A1"}
    ]



class Parsers_with_BS_selenium:

    """This is a documentation for the Parsers class.
This is a class that represents parsers with an attribute of object to parse, prices or rates."""


    def __init_( self, purpose, driver ):
        self.purpose = purpose
        self.driver = driver

    def usd_rub_parser( self ):
        for currency in rates:
            self.driver.get( currency[ "url" ] )
            time.sleep( 5 )
            html_source = self.driver.page_source
            soup = BeautifulSoup( html_source, 'html.parser' )

            currency_rate = soup.find_all( 'div', class_='col-md-2 col-xs-9 _right mono-num' )
            currency_rate = currency_rate [ 3 ]
            currency_rate = currency_rate.text.strip()

        return currency_rate


    def items_prices_parser( self ):
        for item in items:
            self.driver.get ( item[ "url" ] )
            time.sleep(5)
            html_source = self.driver.page_source
            soup = BeautifulSoup( html_source, 'html.parser' )

            item_price = soup.find_all( 'span', class_='market_commodity_orders_header_promote' )
            item_price = item_price[ 1 ]
            item_price = item_price.text.strip()
            prices_final.append(item_price)
        
        return None


rate = Parsers_with_BS_selenium.usd_rub_parser
Parsers_with_BS_selenium.items_prices_parser

print (Parsers_with_BS_selenium.__doc__, "\n")
print ("Rate for USD|RUB : ", rate, "\n", "\n", "Prices of items : ", prices_final)
