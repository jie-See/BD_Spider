# coding=gbk
# Author: 'Matao'
# @Time: 2018/10/6 13:00
import datetime
import time
from redis import StrictRedis
from selenium.webdriver import ActionChains

import config
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
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
rds = StrictRedis(**config.REDIS_CONF)
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

# ��ȡÿ��ID�Ŵ���rds
info_id_key = 'bd_spider:{}'.format(datetime.date.today())
num_list = rds.smembers(info_id_key)
if not num_list:
    for i in range(1, 2):
        browser.get(config.LIST_URL.format(i))
        source_page = browser.page_source
        res_list = re.findall(r'normalthread_\d+', source_page)
        for _ in res_list:
            val = _.split('_')[-1]
            rds.sadd(info_id_key, val)
            rds.expire(info_id_key, 24*3600)

num_list = rds.smembers(info_id_key)
print(num_list)
for num in num_list:
    try:
        print(num)
        browser.get(config.DETAIL_URL.format(num))
        if '��������ظ�' in browser.page_source:
            submit3 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#myTypeTemplateDiv > div.sort_connect > p > a")))  # �жϰ�ť�Ƿ�ɵ��
            time.sleep(3)
            submit3.click()
            send_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#postmessage")))  # �ж�������Ƿ���سɹ�
            send_input.send_keys("����")
            submit4 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#postsubmit > span")))
            submit4.click()
            source_page = browser.page_source
            if '��������ظ�' in source_page or '�ظ��ɼ�������ϵ��ʽ' in source_page:
                submit1 = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#mycenter_menu > li:nth-child(12) > a")))  # �жϰ�ť�Ƿ�ɵ��
                submit1.click()
                continue
            elif '��Ϣ�޶���ʹ����' in source_page:
                xpath_button_add_condition = '//*[@id="nv_forum"]/div[5]/div/span/i/a[1]'
                move_on_to_add_condition = browser.find_element_by_xpath(xpath_button_add_condition)
                ActionChains(browser).move_to_element(move_on_to_add_condition).perform()
                submit2 = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#mycenter_menu > li:nth-child(12) > a")))  # �жϰ�ť�Ƿ�ɵ��
                submit2.click()
                time.sleep(2)
                continue
            res = re.search(r'<div class="sort_thread">([\s\S]*?)<div class="t_fsz t_fsz_f">', source_page).group(1)
            re_h = re.compile('</?\w+[^>]*>')
            s = re_h.sub('', res).replace('\n', '') + '\n\n'
            print(s)
            file = r'C:\Users\i5-Z\Desktop\bd_connect.txt'
            with open(file, 'a+', encoding='gbk') as f:
                f.write(s)
                print('OK!!!')
                rds.srem(info_id_key, num)

        elif '�ظ��ɼ�������ϵ��ʽ' in browser.page_source:
            submit1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#post_reply")))  # �жϰ�ť�Ƿ�ɵ��
            submit1.click()
            account_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))  # �ж��˺ſ��Ƿ���سɹ�
            pwd_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))  # �ж�������Ƿ���سɹ�
            account = config.ACCOUNT_LIST.pop()
            if not account:
                browser.close()
                break
            account_input.send_keys(account)
            pwd_input.send_keys('blegee1234')
            submit2 = wait.until(EC.element_to_be_clickable((By.NAME, "loginsubmit")))  # �жϰ�ť�Ƿ�ɵ��
            submit2.click()
            submit3 = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#myTypeTemplateDiv > div.sort_connect > p > a")))  # �жϰ�ť�Ƿ�ɵ��
            submit3.click()
            send_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#postmessage")))  # �ж��˺ſ��Ƿ���سɹ�
            send_input.send_keys("����")
            submit4 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#postsubmit > span")))
            submit4.click()
            source_page = browser.page_source
            res = re.search(r'<div class="sort_thread">([\s\S]*?)<div class="t_fsz t_fsz_f">', source_page).group(1)
            re_h = re.compile('</?\w+[^>]*>')
            s = re_h.sub('', res).replace('\n', '') + '\n\n'
            print(s)
            file = r'C:\Users\i5-Z\Desktop\bd_connect.txt'
            with open(file, 'a+', encoding='gbk') as f:
                f.write(s)
                rds.srem(info_id_key, num)
                print('OK!!!')
        elif '��Ϣ�޶���ʹ����' in browser.page_source:
            xpath_button_add_condition = '//*[@id="nv_forum"]/div[5]/div/span/i/a[1]'
            move_on_to_add_condition = browser.find_element_by_xpath(xpath_button_add_condition)
            ActionChains(browser).move_to_element(move_on_to_add_condition).perform()
            submit2 = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#mycenter_menu > li:nth-child(12) > a")))  # �жϰ�ť�Ƿ�ɵ��
            submit2.click()
            time.sleep(2)
            continue
        else:
            continue
    except TimeoutException as e:
        continue