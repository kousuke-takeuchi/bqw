import csv
import json

import requests
from bs4 import BeautifulSoup

import models
from settings import session


def get_or_create(sess, model, instance, id_name):
    result = sess.query(model).filter(getattr(model, id_name)==getattr(instance, id_name)).first()
    if result:
        return result
    sess.add(instance)
    sess.commit()
    return instance


def get_categories():
    # 一覧ページからカテゴリーを取得
    results = []
    base_url = 'https://komai0526.thebase.in/'
    resp = requests.get(base_url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    top_categories = soup.select('.leftSide ul#appsItemCategoryTag li')
    for top_category in top_categories[2:]:
        # 親カテゴリー取得
        link = top_category.select('a')[0]
        name = link.text
        url = link.get('href')
        category_id = url.split('/')[-1]
        # サブカテゴリー取得
        sub_categories = top_category.select('ul li a')
        # 一旦親カテゴリーを登録
        parent_category = models.Category(name=name, source_url=url, category_id=category_id)
        parent_category = get_or_create(session, models.Category, parent_category, 'category_id')
        session.add(parent_category)
        session.commit()
        if sub_categories:
            for link in sub_categories:
                url = link.get('href')
                category_id = url.split('/')[-1]
                category = models.Category(name=link.text, source_url=url, category_id=category_id, parent_id=parent_category.id)
                category = get_or_create(session, models.Category, category, 'category_id')
                results.append(category)
        else:
            results.append(parent_category)
    return results

def get_product(url):
    product_id = url.split('/')[-1]
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    name = soup.select('h3.item__title')[0].text
    images = [img.get('src') for img in soup.select('.item__mainImage img')]
    description = soup.select('main .item .row > div > div')[0].text
    # 割引していない場合の商品価格タグ
    sales_price_tag = soup.select('span.item__price')
    if sales_price_tag:
        # 割引していない場合
        proper_price = 0
        sales_price = int(sales_price_tag[0].text[2:].replace(',', ''))
    else:
        # 割引している場合
        proper_price = int(soup.select('p.proper-price')[0].contents[0][2:].replace(',', ''))
        sales_price = int(soup.select('p.sale-price')[0].text[2:].replace(',', ''))
    return dict(
        product_id=product_id,
        name=name,
        description=description,
        images=json.dumps(images),
        proper_price=proper_price,
        sales_price=sales_price,
        source_url=url,
        source='base-komai0526',
    )


categories = get_categories()
for category in categories:
    print(category.name)
    resp = requests.get(category.source_url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    product_links = soup.select('li.itemListBox > a')
    for link in product_links:
        url = link.get('href')
        product_id = url.split('/')[-1]
        product = session.query(models.Product).filter(models.Product.product_id==product_id).first()
        if not product:
            product_params = get_product(url)
            product = models.Product(category_id=category.id, **product_params)
            product = get_or_create(session, models.Product, product, 'product_id')



    # with open('{}.csv'.format(category_name), 'w+') as f:
    #     writer = csv.DictWriter(f, header)
    #     writer.writeheader()
    #     for row in products:
    #         writer.writerow(row)
