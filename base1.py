import csv

import requests
from bs4 import BeautifulSoup


def get_categories():
    results = []
    base_url = 'https://komai0526.thebase.in/'
    resp = requests.get(base_url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    top_categories = soup.select('ul#appsItemCategoryTag li')
    for top_category in top_categories:
        link = top_category.select('a')[0]
        name = link.text
        url = link.get('href')
        sub_categories = top_category.select('ul li a')
        r = [dict(url=url, name=name)]
        if sub_categories:
            r = [dict(url=link.get('href'), name='{} {}'.format(name, link.text)) for link in sub_categories]
        results += r
    return results

def get_product(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    name = soup.select('h3.item__title')[0].text
    print(name)
    images = [img.get('src') for img in soup.select('.item__mainImage img')]
    description = str(soup.select('main .item .row > div > div')[0])
    price_tag = soup.select('span.item__price')
    if price_tag:
        price = price_tag[0].text
    else:
        price = soup.select('p.sale-price')[0].text
    return dict(
        name=name,
        images=images,
        price=price[2:]
    )


categories = get_categories()
for category in categories:
    category_name = category['name']
    print(category_name)
    url = category['url']
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    product_links = soup.select('li.itemListBox > a')
    products = [get_product(link.get('href')) for link in product_links]
    header = products[0].keys()
    with open('{}.csv'.format(category_name), 'w+') as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        for row in products:
            writer.writerow(row)
