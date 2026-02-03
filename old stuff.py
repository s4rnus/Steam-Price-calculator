# def find_prices ( items ):

#     for item in items:

#         item_name = list(item.keys ())[0]
#         item_data = item[item_name]

#         try:

#             driver.get ( item_data["url"] )
#             element = WebDriverWait( driver, 4 ).until( EC.presence_of_element_located(( By.CLASS_NAME, "market_commodity_orders_header_promote" )))
#             html_source = driver.page_source
#             soup = BeautifulSoup( html_source, 'html.parser' )

#             if element:

#                 prices = soup.find_all( 'span', class_='market_commodity_orders_header_promote' )
#                 price = prices[ 1 ].text.strip().replace( "$", "" )
#                 prices_final[item_name] = price

#             else:
#                 prices_final[item_name] = 0

#         except Exception as e:
#             print ( f"An error occured while parsing price: { str( e ) }" )

#     return prices_final


# def calculations (items, prices_final, rate):

#     for item in items:

#         item_name = list( item.keys () )[0]
#         item_data = item[item_name]
#         item_price = prices_final[item_name]

#         try:

#             total_price_RUB = round((float( item_price ) * int( item_data["amount"] ) * float( rate )),2)
#             total_price_USD = float( item_price ) * int( item_data["amount"] )
#             total_prices.append ( f"Total price of {item_name}: {total_price_RUB} RUB | {total_price_USD} USD" )
                
#         except Exception( TypeError, KeyError, ValueError ) as e:

#             print ( f"An error occured while processing: {item_name}: { str( e ) }" )

#     return total_prices