from bs4 import BeautifulSoup
import requests
from requests import get
import time
import random
url = "https://flatfy.ua/uk/%D0%BE%D1%80%D0%B5%D0%BD%D0%B4%D0%B0-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BA%D0%B8%D1%97%D0%B2?page="
houses = []
page = 1
n_pages= int(input("How many pages?"))
while page <= n_pages:
    url = "https://flatfy.ua/uk/%D0%BE%D1%80%D0%B5%D0%BD%D0%B4%D0%B0-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BA%D0%B8%D1%97%D0%B2?page="+ str(page)
    print(url)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    houses_data = html_soup.find_all('div', class_="realty-preview__content-column")
    if houses_data != []:
        houses.extend(houses_data)
        value = random.random()
        scaled_value = 1 + (value * (9-5))
        print(scaled_value)
        time.sleep(scaled_value)
    else:
        print("Nothing find")
        break
    page += 1

print(len(houses))
print(houses[1])
print()
n = int(len(houses))-1
count = 0
n_price = int(input("The highest price"))
n_rooms = int(input("How many rooms"))

while count<=n:
    info = houses[int(count)]
    price = info.find('div', class_="realty-preview-price realty-preview-price--main").text
    discribe = info.find('div', class_= "rah-static rah-static--height-specific").text
    rooms = info.find('span', class_= "realty-preview-info").text
    price = price.encode("iso-8859-1")
    price = price.decode("utf-8")
    discribe = discribe.encode("iso-8859-1")
    discribe = discribe.decode("utf-8")
    rooms = rooms.encode("iso-8859-1")
    rooms = rooms.decode("utf-8")
    k_price = price.replace(price[-4], "")
    k_price = k_price.replace(k_price[-7], "")
    k_price = k_price[:-3]
    k_price = int(k_price)
    k_rooms = rooms[:1]
    k_rooms = int(k_rooms)
    if k_price <= n_price and k_rooms == n_rooms:
        print(price, " ", rooms, " ", discribe)
    count+=1
