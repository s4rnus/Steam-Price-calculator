from locale import resetlocale

#

from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#

from bs4 import BeautifulSoup
import pandas as pd
import openpyxl as OP
from openpyxl import load_workbook
from openpyxl import Workbook
import time
import random

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

def find_USD_to_RUB ( rates ):

    driver.get ( rates[0]["url"] )
    time.sleep ( 3 )
    html_source = driver.page_source
    soup = BeautifulSoup( html_source, 'html.parser' )

    usd_rates_pre = soup.find_all( 'div', class_='col-md-2 col-xs-9 _right mono-num' )
    usd_rate_pre = usd_rates_pre[ 3 ]
    usd_rate = usd_rate_pre.text.strip()

    return usd_rate


def find_price (items ):

    for item in items:

        driver.get( item["url"] )
        time.sleep( 5 )
        html_source = driver.page_source
        soup = BeautifulSoup( html_source, 'html.parser' )

        prices = soup.find_all( 'span', class_='market_commodity_orders_header_promote' )
        price = prices[ 1 ].text.strip()
        prices_final.append( price )

    return prices_final


usd_rate = find_USD_to_RUB ( rates )
find_price ( items )


for price in prices_final:
    print ( price )

print ( usd_rate )

input( "Press Enter to close the window" )
driver.quit ()

