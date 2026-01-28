import argparse

from requests import options

test_args = {'Url': "https://steamcommunity.com/market/listings/730/Gamma%202%20Case", 'amount': "2"}

def parsers():

    parser = argparse.ArgumentParser( 
        prog='SteamPricesParser_cmd', 
        description='This command and argument parser is created to parser control and manipulate the SPP ( SteamPriceParser )' 
        )

    subparsers = parser.add_subparsers ( 
        dest = 'command', 
        help = 'Avaliable commands', 
        required = True 
        )


    #====# inserting an item into db


    add_parser = subparsers.add_parser ( 
        'Insert', 
        help= 'This command allows you to insert an item into the database, takes Url and amount'
        )

    add_parser.add_argument ( 
        'Url', 
        type=str, 
        help= 'Insert a page URL that leads to the steam page of an item' 
        )

    add_parser.add_argument (
        'amount',
        type=int,
        default=0,
        help= 'Amount of items'
        )


    #====# list items     #====# work on this later


    list_parser = subparsers.add_parser ( 
        'List', 
        help= 'This command allows you to list all the items from DB' 
        )

    #====# removing an item from the db


    remove_parser = subparsers.add_parser (
        'Remove', 
        help= 'This command allows you to remove and item from the database with its related info, takes id'
        )

    remove_parser.add_argument (
        '-id',
        type=int,
        required=True,
        help= 'Provide an id of the item that needs to be removed from the db'
        )
    

    #====# create new table


    create_parser = subparsers.add_parser (
        'Create',
        help= 'This command allows you to create a SQL table with a custom name'
        )

    create_parser.add_argument (
        '-name',
        type=str,
        required=True,
        # metavar='table_name',
        help= 'Name of the table'
        )


    #====# adding columns 1 by 1


    column_add_parser = subparsers.add_parser  (
        'column_add',
        help= 'This command allows you to add columns to a spefic table'
        )

    column_add_parser.add_argument (
        '-table_name',
        type=str,
        required=True
        )

    column_add_parser.add_argument (
        '-column_name',
        type=str,
        required=True
        )

    column_add_parser.add_argument (
        '-column_data_type',
        type=str,
        required=True,
        default=int,
        choices= ['INTEGER', 'REAL', 'TEXT', 'BLOB', 'NUMERIC']
        )

    return parser