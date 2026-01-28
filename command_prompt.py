import argparse

def parsers():

    parser = argparse.ArgumentParser( prog='SteamPricesParser_cmd', description='This command and argument parser is created to parser control and manipulate the SPP ( SteamPriceParser )' )

    subparsers = parser.add_subparsers ( dest = 'command', help = 'Avaliable commands', required = True )


    #====# inserting an item into db


    add_parser = subparsers.add_parser ( 
        'Insert', 
        help= 'This command allows you to insert an item into the database'
        )

    add_parser.add_argument ( 
        '--Url: ', 
        type=str, 
        required=True, 
        help= 'Insert a page URL that leads to the steam page of an item' 
        )

    add_parser.add_argument ( 
        '--Name: ', 
        type=str, 
        help= 'Item name'
        )


    #====# list items     #====# work on this later


    list_parser = subparsers.add_parser ( 
        'List', 
        help= 'This command allows you to list all the item from the DB' 
        )

    list_group = list_parser.add_mutually_exclusive_group (required=True)

    list_group.add_argument(
        '--all',
        help= 'Option lists all items stored in DB'
        )

    list_group.add_argument(
        '--id',
        type=int,
        metavar= 'item_id',
        help= 'Option show you an item with the provided ID'
        )


    #====# removing an item from the db


    remove_parser = subparsers.add_parser (
        'Remove', 
        help= 'This command allows you to remove and item from the database with its related info'
        )

    remove_parser.add_argument (
        '--id',
        type=int,
        required=True,
        help= 'Provide an id of the item that needs to be removed from the db'
        )
    
