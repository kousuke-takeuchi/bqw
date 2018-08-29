import os
from os.path import join, dirname
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# 環境変数のロード
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
base_email_1 = os.getenv('BASE_EMAIL_1')
base_password_1 = os.getenv('BASE_PASSWORD_1')
base_email_2 = os.getenv('BASE_EMAIL_2')
base_password_2 = os.getenv('BASE_PASSWORD_2')

# ヘッドレスドライバーの準備
user_agent = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36'
pjs_path = 'node_modules/phantomjs/bin/phantomjs'
dcap = {
    "phantomjs.page.settings.userAgent" : user_agent,
    'marionette' : True
}
driver = webdriver.PhantomJS(executable_path=pjs_path, desired_capabilities=dcap)
WebDriverWait(driver, 1)

# BASEのログインページに移動
login_url = 'https://admin.thebase.in/users/login'
driver.get(login_url)
# ログインフォームにアカウント情報を入力
email_form = driver.find_element_by_xpath("//input[@id='loginUserMailAddress']")
email_form.send_keys(base_email_1)
password_form = driver.find_element_by_xpath("//input[@id='UserPassword']")
password_form.send_keys(base_password_1)
# ログイン情報を入れてボタンを押す
login_button = driver.find_element_by_xpath("//form[@id='userLoginForm']/button")
login_button.click()
WebDriverWait(driver, 3)

# 商品一覧ページへ移動
items_url = 'https://admin.thebase.in/items'
driver.get(items_url)
WebDriverWait(driver, 2)

print(driver.page_source)
