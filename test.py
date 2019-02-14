# coding=gbk
# Author: 'Matao'
# @Time: 2018/10/6 13:00
import datetime
import time
import config
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)





browser.get('http://www.bdwork.com/forum.php?mod=viewthread&tid=234089&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline&_dsign=1cded0b0')
submit1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#post_reply")))  # 判断按钮是否可点击
submit1.click()
account_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))  # 判断账号框是否加载成功
pwd_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))  # 判断密码框是否加载成功
account = 18090181809
account_input.send_keys(account)
pwd_input.send_keys('nuli518.')
submit2 = wait.until(EC.element_to_be_clickable((By.NAME, "loginsubmit")))  # 判断按钮是否可点击
submit2.click()

print('退出帐号。。。。')
time.sleep(4)

xpath_button_add_condition = '//*[@id="nv_forum"]/div[5]/div/span/i/a[1]'
move_on_to_add_condition = browser.find_element_by_xpath(xpath_button_add_condition)
ActionChains(browser).move_to_element(move_on_to_add_condition).perform()
time.sleep(2)
submit2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mycenter_menu > li:nth-child(12) > a")))  # 判断按钮是否可点击
submit2.click()

print('重新登录。。。')
time.sleep(3)
submit1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#post_reply")))  # 判断按钮是否可点击
submit1.click()
account_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))  # 判断账号框是否加载成功
pwd_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))  # 判断密码框是否加载成功
account = 18090181809
account_input.send_keys(account)
pwd_input.send_keys('nuli518.')
submit2 = wait.until(EC.element_to_be_clickable((By.NAME, "loginsubmit")))  # 判断按钮是否可点击
submit2.click()
submit3 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#myTypeTemplateDiv > div.sort_connect > p > a")))  # 判断按钮是否可点击
submit3.click()
send_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#postmessage")))  # 判断账号框是否加载成功
send_input.send_keys("合作")
submit4 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#postsubmit > span")))
submit4.click()
browser.close()


