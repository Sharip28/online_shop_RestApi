import requests
from bs4 import BeautifulSoup

data_list = []


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'
    }
    response = requests.get(url, headers=headers)
    return response.text


def parsing_softech(html):
    soup = BeautifulSoup(html, 'lxml')
    products = soup.find('div', class_="content_bottom").find('div', class_="box featured").find('div', class_="box-content").find('div', class_="row").find_all('div', class_="product-layout col-lg-3 col-md-3 col-sm-3 col-xs-12")
    for product in products:
        try:
            title = product.find('div', class_="right col-sm-8").find('h2').text.strip()
        except:
            title = ''

        try:
            photo = product.find('div',class_="image").find('a',class_="lazy lazy-loaded").find('img').get('src')
        # except Exception as e:
        #     print(e)
        except:
            photo = ''
        try:
            price = product.find('div', class_="price").text.strip()
        except:
            price = ''

        data = {'title': title, 'photo': photo , 'price': price}
        data_list.append(data)

    return data_list


def parsing():
    url = 'https://softech.kg/'
    data_list.clear()
    return parsing_softech(get_html(url))