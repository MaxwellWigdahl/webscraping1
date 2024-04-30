from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = 'https://coinmarketcap.com/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)
webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')
title = soup.title
print(title)

crypto_data1 = soup.findAll("td", attrs={"style": "text-align:start"})
crypto_data2 = soup.findAll("td", attrs={"style": "text-align:end"})

counter = 1
counter2 = 0
for x in range(5):
    name = crypto_data1[counter].text
    counter += 2

    last_price = float(crypto_data2[counter2].text.strip('$').replace(',', ''))
    percent_change = float(crypto_data2[counter2+2].text.strip("%"))
    previous_price = round(last_price / (1 + percent_change/100), 2)
    

    print(f"Company Name: {name}")
    print(f"Price: ${last_price}")
    print(f"Change: {percent_change} %")
    print(f"Previous price: ${previous_price}")
    print()

    counter2 += 8
    