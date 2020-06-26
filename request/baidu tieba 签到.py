from selenium import webdriver
from time import sleep

# 使用cookie的方式实现免登录，然后自动签到。
# 很久之前写的...不能用了也不奇怪..
#
#
'''
url="https://tieba.baidu.com/index.html#"
browser.get(url)
browser.implicitly_wait(3)
    ##
    #贴吧登录需要STOKEN,BAIDUID，BDUSS
'''

#geckodriver的位置
browser = webdriver.Firefox(executable_path="~/geckodriver")


def cookie_login():
    url = "https://tieba.baidu.com/index.html#"
    browser.get(url)
    browser.implicitly_wait(3)
    # 贴吧登录需要STOKEN,BAIDUID，BDUSS
    browser.add_cookie({'name': 'BAIDUID', 'value': '这里填入你的BAIDUID'})
    browser.add_cookie({'name': 'BDUSS',
                        'value': '这里填入你的BDUSS'})
    browser.add_cookie({'name': 'STOKEN', 'value': '这里填入你的STOKEN'})
    browser.implicitly_wait(3)
    browser.refresh()


def onekey_sign():
    onekey_sign = browser.find_element_by_class_name("onekey_btn")
    onekey_sign.click()
    j_sign_btn = browser.find_element_by_class_name("j_sign_btn.sign_btn.sign_btn_nonmember")
    j_sign_btn.click()


def br_quit():
    browser.implicitly_wait(3)
    browser.quit()


def main():
    cookie_login()
    onekey_sign()
    sleep(3)
    br_quit()


if __name__ == '__main__':
    main()

