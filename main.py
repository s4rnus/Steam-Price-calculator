from locale import setlocale
from os import replace
from token import AT
from typing import final
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
import re


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


class Config:
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    url_pattern = r'^https?://[^\s]+$'
    sql_keywords = {
        'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
        'TABLE', 'COLUMN', 'FROM', 'WHERE', 'AND', 'OR', 'UNION', 'JOIN'
    }
    url_alts = ['url', 'Url']

def universal_argument_validation(arguments):
    
    args_dict = vars(arguments)
    
    for key, value in args_dict.items():

        if value is None:
            continue
        
        if isinstance(value, str):

            if re.match(Config.url_pattern, value):
                if 'url' not in key.lower():
                    print(f'Wrong argument for Url...\n')
                    return False
                continue

            else:
                if not re.match(Config.pattern, value):
                    print(f'Wrong argument for table name...\n')
                    return False
        
        if isinstance(value, int):
            continue
    
    return True


class Parser:

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

        rate = Parser.find_currency_rates( currencies, id_to_char )

        try:
            element = WebDriverWait( driver, 4 ).until( EC.presence_of_element_located(( By.CLASS_NAME, "market_commodity_orders_header_promote" )))
            html_source = driver.page_source
            soup = BeautifulSoup( html_source, 'html.parser' )

            if element:

                prices = soup.find_all( 'span', class_='market_commodity_orders_header_promote' )
                price = prices[ 1 ].text.strip().replace( "$", "" )
                price_RUB = round((float(price)*float(rate)), 2)
                print ( f"Price found: { price }\n" )
           
            else:
                price = 0
                print ( f"Price not found, set to default { price }\n" )

        except Exception as e:
            print( f"An error occurred while parsing price: {e}" )
            return [price, price_RUB]


        return [price, price_RUB]


    def get_name(args):

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


class command_drivers:


    def insert_item(args):

        if not universal_argument_validation(args):
            print ( f'Invalid arguments, fuck off.' )
            return False

        try:

            price, price_RUB = Parser.get_price(args)
            name = Parser.get_name(args)

            connection = sqlite3.Connection ( 'itemsdb.db' )
            cursor = connection.cursor ()

            cursor.execute( '''
            SELECT name FROM sqlite_master WHERE name=?
            ''', ( args.add_table_name, ))

            if not cursor.fetchone():
                return (f"Wrong table name...")

            print ( f"Adding a new item with the following info: \n"
                    f"Name: {name}\n"
                    f"Url: {args.Url}\n"
                    f"Price at the start: {price} USD\n"
                    f"Amount: {args.amount}\n"
                    )

            query = f'''
            INSERT into {args.add_table_name} 
            ( name, url, amount, price_start_USD, price_latest_USD, price_latest_RUB ) 
            VALUES (?, ?, ?, ?, ?, ?)
            '''

            cursor.execute (query, (name, args.Url, args.amount, price, price, price_RUB))

        except sqlite3.Error as e:
            print(f"DB Error: {e}")
            connection.rollback()

        finally:

            connection.commit ()
            connection.close ()


    def list_items(args):

        if not universal_argument_validation(args):
            print ( f'Invalid arguments, fuck off.' )
            return False

        else:
            connection = sqlite3.Connection ( 'itemsdb.db' )
            cursor = connection.cursor ()

            cursor.execute (f'''
            SELECT name FROM sqlite_master WHERE name=?
            ''', (args.list_table_name,))

            if not cursor.fetchone():
                return (f"Wrong table name, buddy...")

            query = f'''
            SELECT * FROM {args.list_table_name}
            '''

            cursor.execute (query)

            items = cursor.fetchall()

            for item in items:
                print("\n",item)
          
            connection.commit ()
            connection.close ()


    def create_table(args):

        if not universal_argument_validation(args):
            print ( f'Invalid arguments, fuck off.' )
            return False

        try:    

            connection = sqlite3.Connection ( 'itemsdb.db' )
            cursor = connection.cursor ()

            column_def = f" {args.create_column_name} {args.create_column_data_type}"

            if args.create_PK and args.create_PK.upper() == 'PK':

                column_def += 'PRIMARY KEY'

            cursor.execute ( f'''
            CREATE TABLE IF NOT EXISTS 
            {args.create_table_name} 
            ({column_def})
            ''')

            print (f'Succesfully created table named: {args.create_table_name}')

        except sqlite3.Error as e:
            print(f"DB Error: {e}")
            connection.rollback()
            
        finally:
            connection.commit ()
            connection.close ()


    def add_columns(args):

        if not universal_argument_validation(args):
            print ( f'Invalid arguments, fuck off.' )
            return False

        try:

            connection = sqlite3.Connection ( 'itemsdb.db' )
            cursor = connection.cursor ()

            cursor.execute ( f'''
            SELECT name FROM sqlite_master WHERE type='table' AND name=?
            ''', ( { args.add_column_table.name } ) )

            if not cursor.fetchone():
                return ( f"Table does not exist..." )


            cursor.execute ( f'''
            PRAGMA table_info({args.add_column_table_name})
            ''')

            for col in cursor.fetchall():
                existing_col = col[1].lower()
                    
                if args.column_name.lower() == existing_col:
                    return (f'''Column already exists''')


            query = f'''
            ALTER TABLE {args.add_column_table_name} 
            ADD COLUMN {args.column_name} {args.column_data_type}
            '''
            cursor.execute (query)

        except sqlite3.Error as e:
            print(f"DB Error: {e}") 
            connection.rollback()
            
        finally:
            connection.commit ()
            connection.close ()


    def alter_columns (args):
        
        if not universal_argument_validation(args):
            print ( f'Invalid arguments, fuck off.' )
            return False

        try:

            connection = sqlite3.Connection ( 'itemsdb.db' )
            cursor = connection.cursor ()

            cursor.execute( f'''
            SELECT name FROM sqlite_master WHERE type='table' AND name=?
            ''', ( args.alter_table_name, ) )

            if not cursor.fetchone():
                print (f'Wrong table name...')
                return False

            cursor.execute( f'''
            
            ''' )




        except sqlite3.Error as e:
            print(f"DB Error: {e}")
            connection.rollback()

        finally:
            connection.commit ()
            connection.close ()


    def remove_items(args):

        if not universal_argument_validation(args):
            print ( f'Invalid arguments, fuck off.' )
            return False

        try:

            connection = sqlite3.Connection ( 'itemsdb.db' )
            cursor = connection.cursor ()

            cursor.execute( f'''
            SELECT name FROM sqlite_master WHERE type='table' AND name=?
            ''', ( args.remove_items_table_name, ) )

            if not cursor.fetchone():
                print (f'Wrong table name...')
                return False

            cursor.execute (f'''
            PRAGMA table_info({args.remove_items_table_name})
            ''')

            existing_column = []
            for col in cursor.fetchall():
                existing_column.append(col[1].lower())

                if args.param not in existing_column:
                    print ( f'Column doesnt exist...' )
                    return False

            cursor.execute (f'''
            DELETE FROM {args.remove_items_table_name} 
            WHERE {args.param} == ?
            ''', (args.value,))

            print (f'Successfuly deleted {args.param} {args.value} from {args.remove_items_table_name}...')
            
        except sqlite3.Error as e:
            print(f"DB Error: {e}")
            connection.rollback()

        finally:
            connection.commit ()
            connection.close ()


    def ShowTables (args):
        
        if not universal_argument_validation(args):
            print ( f'Invalid arguments, fuck off.' )
            return False

        try:

            connection = sqlite3.Connection('itemsdb.db')
            cursor=connection.cursor ()

            cursor.execute ('''
            SELECT name FROM sqlite_master WHERE type='table'
            ''')

            names = cursor.fetchall().pop(-1)

            i = 0
            for i, table_name in enumerate(names):
                print (f"""Table {i}: {table_name}""")
                i += 1


        except sqlite3.Error as e:
            print(f"DB Error: {e}")
            connection.rollback()

        finally:
            connection.commit ()
            connection.close ()


    def ShowColumns (args):

        if not universal_argument_validation(args):
            print ( f'Invalid arguments, fuck off.' )
            return False

        try:

            connection = sqlite3.Connection('itemsdb.db')
            cursor = connection.cursor ()

            cursor.execute ('''
            SELECT name FROM sqlite_master WHERE type='table' AND name= ?
            ''', (args.ShowC_table_name, ))

            if not cursor.fetchone():
                print (f'Wrong table name...')
                return False

            else:

                if args.ShowC_column_info == 'ext':

                    cursor.execute(f"""
                    PRAGMA table_info({args.ShowC_table_name})
                    """)

                    results = cursor.fetchall()

                    i=0

                    for i, column in enumerate(results):
                        print (f'''Column {i}: {column}''')
                        i += 1


                if args.ShowC_column_info == 'main':

                                        cursor.execute(f"""
                PRAGMA table_info({args.ShowC_table_name})
                """)

                results = cursor.fetchall()

                i=0
                filtered = []

                for col in results:
                    filtered.append( ( list(col)[1], list(col)[2] ) )

                for i, col in enumerate(filtered):
                    print (f'''Column {i}: {col}''')
                    i += 1

        except sqlite3.Error as e:
            print(f"DB Error: {e}")
            connection.rollback()

        finally:
            connection.commit ()
            connection.close ()   



#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====# main


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
                'Insert': command_drivers.insert_item,
                'List': command_drivers.list_items,
                'Remove': command_drivers.remove_items,
                'Create': command_drivers.create_table,
                'Add': command_drivers.add_columns,
                'Remove': command_drivers.remove_items,
                'ShowT': command_drivers.ShowTables,
                'ShowC': command_drivers.ShowColumns,
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


driver.quit ()


#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====#=====# left until further notice


    # def table_alter(args):
        
        
    #     if not universal_argument_validation(args):
    #         print ( f'Invalid arguments, fuck off.' )
    #         return False

    #     try:

    #         connection = sqlite3.Connection('itemsdb.db')
    #         cursor = connection.cursor ()

    #         cursor.execute ('''
    #         SELECT name FROM sqlite_master WHERE type='table' AND name= ?
    #         ''', (args.ShowC_table_name, ))

    #         if not cursor.fetchone():
    #             print (f'Wrong table name...')
    #             return False

    #         else:

                

    #             #realised the obseliteness of this command, this will remain here until further notice.



    #     except sqlite3.Error as e:
    #         print(f"DB Error: {e}")
    #         connection.rollback()

    #     finally:
    #         connection.commit ()
    #         connection.close ()        


