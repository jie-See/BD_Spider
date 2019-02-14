# coding=gbk
# Author: 'Matao'
# @Time: 2018/10/11 13:00
import datetime
import time
from redis import StrictRedis
from selenium.webdriver import ActionChains

import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

## get the Firefox profile object
# firefoxProfile = FirefoxProfile()
## Disable CSS
# firefoxProfile.set_preference('permissions.default.stylesheet', 2)
## Disable images
# firefoxProfile.set_preference('permissions.default.image', 2)
## Disable Flash
# firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
# browser = webdriver.Firefox(firefoxProfile)
from bd_zhijia_config import LIST_PAGE_URL, DETAIL_PAGE_URL, TOTAL_PAGE, ACCOUNT_LIST, REDIS_CONF, PASSWORD

rds = StrictRedis(**REDIS_CONF)
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
wait_tmp = WebDriverWait(browser, 1)

id_key = 'bd_zhijia_spider:id_list'
account_key = 'bd_zhijia_spider:account_list'

# 增加账号
for account in ACCOUNT_LIST:
    rds.sadd(account_key, account)

# 获取账号
def get_account():
    return rds.spop(account_key)

def del_account(account):
    rds.hdel(account_key, account)

# 翻页获取网页ID_LIST[123,123,123,123]
ID_LIST = []
for page in range(1,TOTAL_PAGE):
    list_url = LIST_PAGE_URL.format(page)
    browser.get(list_url)
    source_page = browser.page_source
    res_list = re.findall(r'"c-trade-card__link" target="_blank" href="demand-\d+', source_page)
    num_list = re.findall("\d+", str(res_list))
    ID_LIST.extend(num_list)

# 判断ID是否存在rds中，存在即删除
for id in set(ID_LIST):
    if rds.sismember(id_key, id):
        ID_LIST.remove(id)
print('当前需要爬取的网页id:',ID_LIST)


# 爬取详情页
count = 1
ac = get_account()

for detail_id in ID_LIST:
    detail_page_url = DETAIL_PAGE_URL.format(detail_id)
    browser.get(detail_page_url)
    source_page = browser.page_source
    try:
        if '回复可见合作联系方式' in source_page:
            if not ac:
                browser.close()
                print('数据爬取完毕~~~')
                break
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#post_reply"))).click()
            # 切换子页面
            browser.switch_to.frame("layui-layer-iframe1")
            try:
                # 第一次登陆
                wait_tmp.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div > a"))).click()
                # 跳转句柄
                all = browser.window_handles  # 显示句柄
                z = browser.current_window_handle  # 当前页句柄
                browser.switch_to_window(browser.window_handles[1])  # 移动句柄
                ##登陆账号
                account_input = wait.until(EC.presence_of_element_located((By.NAME, "phone")))
                pwd_input = wait.until(EC.presence_of_element_located((By.NAME, "pass")))
                account_input.send_keys(ac)
                pwd_input.send_keys(PASSWORD)
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "body > main > div > div.c-auth__content > form > div:nth-child(4) > a"))).click()
                # 关闭当前句柄
                browser.close()
                # 移动句柄
                browser.switch_to_window(browser.window_handles[0])
                browser.refresh()
            except:
                # cookie登陆
                wait_tmp.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > form > textarea"))).click()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > form > textarea"))).send_input.send_keys("合作")
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > form > button"))).click()
                # 等待两秒自动刷新
                time.sleep(2.2)
                if '今日回帖数量已达上限' in browser.page_source:
                    # 退出登录
                    browser.refresh()
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div > div > ul > li: nth - child(1) > a"))).click()
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > div > div.c-user__aside > nav > ul > li:nth-child(7) > a"))).click()
                    del_account(ac)
                    ac = get_account()
                    continue
            # 获取数据写入文件
            source_page = browser.page_source
            res = re.search(r'<div class="c-post-overview__main">([\s\S]*?)<style>', source_page).group(1)
            old_text = re.sub(r'</?\w+[^>]*>', '', res)
            text = re.sub(r'\s', '', old_text) + '\n\n'
            file = r'C:\Users\i5-Z\Desktop\bd_zhijia_{}.txt'.format(datetime.date.today())
            with open(file, 'a+', encoding='gbk') as f:
                f.write(text)
                print('第{}条数据爬取完成！'.format(count))
                count += 1
                rds.sadd(id_key, detail_id)
                rds.expire(id_key, 24 * 3600 * 7)
        else:
            print('当前页没有信息哦~~~')
            continue
    except:
        print('当前页出错啦~~~')
        continue

browser.close()
print('列表循环完成，爬取完毕~~~')