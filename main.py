from locale import setlocale
from os import replace
from token import AT
from urllib import request, response
from xml.dom.minidom import Element

#

import pandas as pd
import sys
import random
import time
import random
import requests
import logging
import sqlite3
import command_prompt
import defs
from defs import currencies, id_to_char
from command_prompt import parsers

#

from defs import items
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

connection = sqlite3.connect( 'itemsdb.db' )
cursor = connection.cursor

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


def get_price(args):

    driver.get ( args.Url ) 

    rate = find_currency_rates( currencies, id_to_char )

    try:
        element = WebDriverWait( driver, 4 ).until( EC.presence_of_element_located(( By.CLASS_NAME, "market_commodity_orders_header_promote" )))
        html_source = driver.page_source
        soup = BeautifulSoup( html_source, 'html.parser' )

        if element:

            prices = soup.find_all( 'span', class_='market_commodity_orders_header_promote' )
            price = prices[ 1 ].text.strip().replace( "$", "" )
            price_RUB = float(price)*float(rate)
            print ( f"Price found: { price }\n" )
        
        else:
            price = 0
            print ( f"Price not found, set to default { price }\n" )

    except Exception as e:
        print( f"An error occurred while parsing price: {e}" )
        return [price, price_RUB]


    return [price, price_RUB]


def get_name(args):

    driver.get ( args.Url ) 

    try:
        element = WebDriverWait( driver, 4 ).until( EC.presence_of_element_located(( By.CLASS_NAME, "f6hU22EA7Z8peFWZVBJU" )))
        html_source = driver.page_source
        soup = BeautifulSoup( html_source, 'html.parser' )

        if element:

            name = soup.find ( 'span', class_='f6hU22EA7Z8peFWZVBJU' )
            name = name.text.strip()
            print ( f"Name found: { name }\n" )

        else:
            name = "NOTFOUND"
            print ( f"Name not found, set to default { name }\n" )

    except Exception as e:
        print( f"An error occurred while parsing name: { e }" )
        return name


    return name


def insert_item(args):

    price, price_RUB = get_price(args)
    name = get_name(args)

    connection = sqlite3.Connection ( 'itemsdb.db' )
    cursor = connection.cursor ()

    print ( f"Adding a new item with the following info: \n"
            f"Name: {name}\n"
            f"Url: {args.Url}\n"
            f"Price at the start: {price} USD\n"
            f"Amount: {args.amount}\n"
          )

    cursor.execute (f'''
    INSERT into Items ( name, url, amount, price_start_USD, price_latest_USD, price_latest_RUB ) 
    VALUES ( ?, ?, ?, ?, ?, ? )
    ''', ( name, args.Url, args.amount, price, price, price_RUB ))

    connection.commit ()
    connection.close ()


def list_items(args):

    connection = sqlite3.Connection ( 'itemsdb.db' )
    cursor = connection.cursor ()

    cursor.execute (f'''
    SELECT * FROM Items 
    ''')
    items = cursor.fetchall()

    for item in items:
        print(item)

    connection.commit ()
    connection.close ()


def create_table(args):

    connection = sqlite3.Connection ( 'itemsdb.db' )
    cursor = connection.cursor ()

    cursor.execute ( f'''
    CREATE TABLE IF NOT EXISTS {args.name}
    ''' )

    connection.commit ()
    connection.close ()


def add_columns(args):

    connection = sqlite3.Connection ( 'itemsdb.db' )
    cursor = connection.cursor ()

    cursor.execute ( f'''
    ALTER TABLE ? ADD COLUMN ? ?
    ''', ( args.table_name, args.column_name, args.column_data_type) )

    connection.commit ()
    connection.close ()


def remove_items(args):

    connection = sqlite3.Connection ( 'itemsdb.db' )
    cursor = connection.cursor ()

    cursor.execute ( f'''
    DELETE FROM ? WHERE ? 
    
    ''' ) #=====================================# остановился тут

    connection.commit ()
    connection.close ()


#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====# def activations | prints


def main():

    while True:
        try:
            user_input = input("\nType cmd or 'exit' to exit :").strip()

            if user_input.lower() == "exit":
                print ("Exiting the program... ")
                break
            
            if not user_input:
                continue

            args_list = user_input.split()

            parser = parsers()
            args = parser.parse_args(args_list)

            command_handlers = {
                'Insert': insert_item,
                'List': list_items,
                'Remove': remove_items,
                'Create': create_table,
                'Add': add_columns,
                'Remove': remove_items
                }

            handler = command_handlers.get(args.command)
            if handler:
                handler(args)
            else:
                print (f"Unknown command: {args.command}")
        
        except SystemExit:
            continue

        except KeyboardInterrupt:
            print ("\nExiting the program... ")
            break

if __name__ == "__main__":
    main() 
    input("\nPress Enter to exit...")
         


# rate = find_currency_rates( currencies, id_to_char )
# find_prices ( items )
# total_prices = calculations( items, prices_final, rate )

# print ( "USD | RUB rate: ", rate, "\n" )

# for i in total_prices:
#     print ( i, '\n' )

driver.quit ()

