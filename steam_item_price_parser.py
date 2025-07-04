from locale import resetlocale
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

prices = []
counter = 1

items = [
    { "name": "Gamma 2 Case", "url": "https://steamcommunity.com/market/listings/730/Gamma%202%20Case"},
    { "name": "Stockholm 2021 Legends Sticker Capsule", "url": "https://steamcommunity.com/market/listings/730/Stockholm%202021%20Legends%20Sticker%20Capsule"},
    { "name": "Fracture Case", "url": "https://steamcommunity.com/market/listings/730/Fracture%20Case"},
    { "name": "Revolution Case", "url": "https://steamcommunity.com/market/listings/730/Revolution%20Case?ysclid=mcjgbqzeed990445279"},
    { "name": "Dreams & Nightmares Case", "url": "https://steamcommunity.com/market/listings/730/Dreams%20%26%20Nightmares%20Case"},
    { "name": "Recoil Case", "url": "https://steamcommunity.com/market/listings/730/Recoil%20Case"},
    { "name": "Kilowatt Case", "url": "https://steamcommunity.com/market/listings/730/Kilowatt%20Case"},
    { "name": "Snakebite Case", "url": "https://steamcommunity.com/market/listings/730/Snakebite%20Case"},
    { "name": "Operation Phoenix Weapon Case", "url": "https://steamcommunity.com/market/listings/730/Operation%20Phoenix%20Weapon%20Case"},
    #{ "name": "USD/RUB", "url": ""}
    ]

selectors = [
    'span.market_commodity_orders_header_promote',
    'div.market_commodity_order_summary',
    'span.normal_price'
    ]


response = requests.get(items[0]["url"], headers = headers)
if str(response.status_code) == 200:
    print ("Code 200, good to parse.")
elif str(response.status_code) == 429:
    print ("Code 429, wait.")
else:
    print (response.status_code)


def parse_steam_price(url):
    response = requests.get(url, headers = headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    #price = (soup.find('span', class_='market_commodity_orders_header_promote') or soup.find('div', class_='market_commodity_order_summary') or soup.find('span', class_='normal_price'))

    for selector in selectors:
        price_elem = soup.find(selector)
        if price_elem:
            price = price_elem.get_text(strip=True)
            break
        else:
            price= "Not Found"

    return price


with open ("codes and prices.txt", "w", encoding = "utf-8") as file:
    for item in items:
        indiv_resp = requests.get(item["url"], headers = headers)
        price = str(parse_steam_price (item["url"]))
        code = str(indiv_resp.status_code)
        file.write (f"{counter}. Price of:  {item['name']} --- {price}\n")

        time.sleep (random.uniform(1, 5))
        counter += 1

