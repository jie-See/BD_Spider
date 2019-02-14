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

# �����˺�
for account in ACCOUNT_LIST:
    rds.sadd(account_key, account)

# ��ȡ�˺�
def get_account():
    return rds.spop(account_key)

def del_account(account):
    rds.hdel(account_key, account)

# ��ҳ��ȡ��ҳID_LIST[123,123,123,123]
ID_LIST = []
for page in range(1,TOTAL_PAGE):
    list_url = LIST_PAGE_URL.format(page)
    browser.get(list_url)
    source_page = browser.page_source
    res_list = re.findall(r'"c-trade-card__link" target="_blank" href="demand-\d+', source_page)
    num_list = re.findall("\d+", str(res_list))
    ID_LIST.extend(num_list)

# �ж�ID�Ƿ����rds�У����ڼ�ɾ��
for id in set(ID_LIST):
    if rds.sismember(id_key, id):
        ID_LIST.remove(id)
print('��ǰ��Ҫ��ȡ����ҳid:',ID_LIST)


# ��ȡ����ҳ
count = 1
ac = get_account()

for detail_id in ID_LIST:
    detail_page_url = DETAIL_PAGE_URL.format(detail_id)
    browser.get(detail_page_url)
    source_page = browser.page_source
    try:
        if '�ظ��ɼ�������ϵ��ʽ' in source_page:
            if not ac:
                browser.close()
                print('������ȡ���~~~')
                break
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#post_reply"))).click()
            # �л���ҳ��
            browser.switch_to.frame("layui-layer-iframe1")
            try:
                # ��һ�ε�½
                wait_tmp.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div > a"))).click()
                # ��ת���
                all = browser.window_handles  # ��ʾ���
                z = browser.current_window_handle  # ��ǰҳ���
                browser.switch_to_window(browser.window_handles[1])  # �ƶ����
                ##��½�˺�
                account_input = wait.until(EC.presence_of_element_located((By.NAME, "phone")))
                pwd_input = wait.until(EC.presence_of_element_located((By.NAME, "pass")))
                account_input.send_keys(ac)
                pwd_input.send_keys(PASSWORD)
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "body > main > div > div.c-auth__content > form > div:nth-child(4) > a"))).click()
                # �رյ�ǰ���
                browser.close()
                # �ƶ����
                browser.switch_to_window(browser.window_handles[0])
                browser.refresh()
            except:
                # cookie��½
                wait_tmp.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > form > textarea"))).click()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > form > textarea"))).send_input.send_keys("����")
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > form > button"))).click()
                # �ȴ������Զ�ˢ��
                time.sleep(2.2)
                if '���ջ��������Ѵ�����' in browser.page_source:
                    # �˳���¼
                    browser.refresh()
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div > div > ul > li: nth - child(1) > a"))).click()
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > div > div.c-user__aside > nav > ul > li:nth-child(7) > a"))).click()
                    del_account(ac)
                    ac = get_account()
                    continue
            # ��ȡ����д���ļ�
            source_page = browser.page_source
            res = re.search(r'<div class="c-post-overview__main">([\s\S]*?)<style>', source_page).group(1)
            old_text = re.sub(r'</?\w+[^>]*>', '', res)
            text = re.sub(r'\s', '', old_text) + '\n\n'
            file = r'C:\Users\i5-Z\Desktop\bd_zhijia_{}.txt'.format(datetime.date.today())
            with open(file, 'a+', encoding='gbk') as f:
                f.write(text)
                print('��{}��������ȡ��ɣ�'.format(count))
                count += 1
                rds.sadd(id_key, detail_id)
                rds.expire(id_key, 24 * 3600 * 7)
        else:
            print('��ǰҳû����ϢŶ~~~')
            continue
    except:
        print('��ǰҳ������~~~')
        continue

browser.close()
print('�б�ѭ����ɣ���ȡ���~~~')