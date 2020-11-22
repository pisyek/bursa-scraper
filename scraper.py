from bs4 import BeautifulSoup
from pandas import DataFrame
import requests


stock_name = []
stock_code = []
stock_last_done = []
stock_lacp = []
stock_change = []
stock_change_percent = []
stock_vol = []
stock_buy_vol = []
stock_sell_vol = []
stock_high = []
stock_low = []

def scrapping(url, page_number, max_page_number):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
        }

        url_with_page_number = url + str(page_number)
        response = requests.get(str(url_with_page_number), headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.findAll('tr', {'id':'data-1'})
        for i in range(len(table)):
            name = table[i].findAll('td')[1].text.strip()
            code = table[i].findAll('td')[2].text.strip()
            last_done = table[i].findAll('td')[4].text.strip()
            lacp = table[i].findAll('td')[5].text.strip()
            change = table[i].findAll('td')[6].text.strip()
            change_percent = table[i].findAll('td')[7].text.strip()
            vol = table[i].findAll('td')[8].text.strip()
            buy_vol = table[i].findAll('td')[9].text.strip()
            sell_vol = table[i].findAll('td')[12].text.strip()
            high = table[i].findAll('td')[13].text.strip()
            low = table[i].findAll('td')[14].text.strip()

            stock_name.append(name)
            stock_code.append(code)
            stock_last_done.append(last_done)
            stock_lacp.append(lacp)
            stock_change.append(change)
            stock_change_percent.append(change_percent)
            stock_vol.append(vol)
            stock_buy_vol.append(buy_vol)
            stock_sell_vol.append(sell_vol)
            stock_high.append(high)
            stock_low.append(low)

        # next page
        page_number += 1
        if page_number < max_page_number:
            scrapping(url, page_number, max_page_number)

    except:
        raise Exception('Program failed.')

# run function
scrapping('https://www.bursamalaysia.com/market_information/shariah_compliant_equities_prices?per_page=50&page=', 1, 19)

data = {
    'name': stock_name,
    'code': stock_code,
    'price': stock_last_done,
    'lacp': stock_lacp,
    'change': stock_change,
    'change_percent': stock_change_percent,
    'vol': stock_vol,
    'buy_vol': stock_buy_vol,
    'sell_vol': stock_sell_vol,
    'high': stock_high,
    'low': stock_low
}

columns = ['name', 'code', 'price', 'lacp', 'change', 'change_percent', 'vol', 'buy_vol', 'sell_vol', 'high', 'low']
df = DataFrame(data, columns=columns)
df.to_csv('output.csv')
