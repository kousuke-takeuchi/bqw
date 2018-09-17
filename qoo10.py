import os
import csv
import json

from settings import session
import models

def import_categories():
    filename = 'Qoo10GoodsDataLinkageMgt_CategoryInfo.csv'
    filepath = os.path.join(os.path.dirname(__file__), 'templates', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            category = models.Qoo10Category()
            category.l_category_id = row[0]
            category.l_category_name = row[1]
            category.m_category_id = row[2]
            category.m_category_name = row[3]
            category.s_category_id = row[4]
            category.s_category_name = row[5]
            session.add(category)
            session.commit()

def export_product_csv():
    # Qoo10のフォーマットの商品CSVを作成する
    with open('qoo10_products.csv', 'w+') as f:
        writer = csv.writer(f)
        headers = [
            'Item Code', 'Seller Code', 'Status', '2nd Cat Code', 'Item Name',
            'Item Description', 'Short Title', 'Item Detail Header',
            'Item Detail Footer', 'Brief Description', 'Image URL', 'Sell Price',
            'Sell Qty', 'Shipping Group No', 'Item Weight', 'Option Info',
            'Inventory Info', 'Maker No', 'Brand No', 'Product Model Name',
            'Retail Price', 'Origin Type', 'Place of Origin', 'Industrial Code',
            'Item Condition', 'Manufacture Date', 'Adult Product Y/N', 'A/S Info',
            'Available Date', 'Gift', 'Additional Item Image',
            'Inventory Cover Image', 'Multi Shipping Rate'
        ]
        writer.writerow(headers)

        for product in session.query(models.Product).all():
            # Qoo10商品コード
            item_code = ''
            # 販売者商品コード
            seller_code = product.id
            # 取引待ち : S1
            # 取引可能 : S2
            # 取引廃止 : S4
            status = 'S1'
            # カテゴリーコード
            cat_code = product.category.qoo10_categories[0].s_category_id
            # 商品名
            item_name = product.name
            # 商品詳細
            item_description = product.description.replace('\n', '')
            # 短絡商品名
            short_title = product.name[:20]
            item_detail_header = product.name
            item_detail_footer = product.name
            # 商品説明
            brief_description = product.name
            image_url = json.loads(product.images)[0]
            sell_price = product.sales_price
            sell_qty = product.proper_price
            # 送料無料
            shipping_group_no = ''
            item_weight = ''
            option_info = ''
            inventory_info = ''
            maker_no = ''
            brand_no = ''
            product_model_name = ''
            retail_price = product.proper_price
            # 国内
            origin_type = 1
            # 国家名
            place_of_origin = ''
            # JANコード
            industrial_code = ''
            # 新品 : 1
            # 中古品 (未使用) : 2
            # 中古品 (新古品) : 3
            # 中古品 (ほぼ新品) : 4
            # 中古品 (状態良好) : 5
            # 中古品 (少々古め) : 6
            # 中古品 (使用不可(収集家用)) : 7
            item_condition = 1
            manufacture_date = ''
            adult_product = 'N'
            as_info = ''
            # - 数字を入力する場合、商品の準備日となります。 (商品の準備日の入力 ex: 1)
            # - 日時の形式で入力する場合、発売日となります。 (発売日の入力 ex: 2013-09-26)
            # - 入力しない場合はすぐに配送できる一般の商品となります。
            available_date = ''
            # おまけ
            gift = ''
            # 商品の追加イメージ
            # 最大 11個のイメージを追加することが可能
            # 例 ) http://gd.image-qoo10.jp/mi/307/990/422990307.jpg$$http://gd.image-qoo10.jp/mi/905/046/422046905.jpg
            additional_item_image = '$$'.join(json.loads(product.images)[0:])
            inventory_cover_image = ''
            # オプション送料の登録
            # 最大2個のコード登録機能
            # 例 ) 233982$$228507
            multi_shipping_rate = ''
            row = [
                item_code, seller_code, status, cat_code, item_name,
                item_description, short_title, item_detail_header,
                item_detail_footer, brief_description, image_url,
                sell_price, sell_qty, shipping_group_no, item_weight,
                option_info, inventory_info, maker_no, brand_no,
                product_model_name, retail_price, origin_type,
                place_of_origin, industrial_code, item_condition,
                manufacture_date, adult_product, as_info,
                available_date, gift, additional_item_image,
                inventory_cover_image, multi_shipping_rate,
            ]
            writer.writerow(row)


if __name__ == '__main__':
    export_product_csv()
