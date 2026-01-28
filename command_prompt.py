import argparse

from requests import options



class mss:

    def sqlkeyword_validation(name):

        sql_keywords = {
            'SELECT', 'INSERT', 'DELETE', 'UPDATE', 'DROP', 
            'CREATE', 'ALTER', 'UNION', 'WHERE', 'OR', 'AND'
        }

        if name.upper() in sql_keywords:
            return False

        return True


    def pattern_validation(name):

        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'

        if not re.match(pattern, name):
            return False

        return True



def parsers():

    parser = argparse.ArgumentParser( 
        prog='SteamPricesParser_cmd', 
        description='\nThis command and argument parser is created to control and manipulate the SPP ( SteamPriceParser ) and its DB \n',
        formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''

        '''
        )

    subparsers = parser.add_subparsers ( 
        dest = 'command', 
        help = 'Avaliable commands', 
        required = True 
        )


    #====# inserting an item into db


    add_parser = subparsers.add_parser ( 
        'Insert', 
        help= '\nThis command allows you to insert an item into the database \n takes: Url, amount \n'
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
        help= '\nThis command allows you to list all the items from DB \n takes: Table name \n' 
        )

    list_parser.add_argument (
        'list_table_name',
        help = 'Provide name of the table to list entries from'
        )


    #====# removing an item from the db


    remove_parser = subparsers.add_parser (
        'Remove', 
        help= '\nThis command allows you to remove an item from the database with its related info \n takes: table name, parameter, value \n'
        )

    remove_parser.add_argument (
        'remove_items_table_name',
        help= 'Provide name of the table to delete from'
        )

    remove_parser.add_argument (
        'param',
        help= 'Provide a parameter to search with'
        )

    remove_parser.add_argument (
        'value',
        type=int,
        help= 'Provide an id of the item that needs to be removed from the db'
        )
    

    #====# create new table


    create_parser = subparsers.add_parser (
        'Create',
        help= '\nThis command allows you to create a SQL table with a custom name \n takes: name of the new table \n'
        )

    create_parser.add_argument (
        'create_table_name',
        type=str,
        help= 'Name of the table'
        )


    #====# adding columns 1 by 1


    column_add_parser = subparsers.add_parser  (
        'CAdd',
        help= '\nThis command allows you to add columns to a spefic table \n takes: table name, column name, column data type \n'
        )

    column_add_parser.add_argument (
        'add_table_name',
        type=str,
        )

    column_add_parser.add_argument (
        'column_name',
        type=str,
        )

    column_add_parser.add_argument (
        'column_data_type',
        type=str,
        default=int,
        choices= ['INTEGER', 'REAL', 'TEXT', 'BLOB', 'NUMERIC']
        )

    return parser