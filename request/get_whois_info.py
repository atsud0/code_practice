"""
获取通过www.whois.com获取输入网站的Whois信息
"""


import requests
import re

rep_name = ['http://', 'https://', 'www.']
#name = 'https://www.baidu.com'
name = input("请输入你要查找的域名:")

'''其实没有这个处理也是可以的,因为提交数据后会网站会自动处理'''
for i in rep_name:
    if i in name:
        name = name.replace(i, '')

url = 'https://www.whois.com/whois/{0}'.format(name)

res = requests.get(url)

n = re.compile('id="registrarData">(.*)</pre></div>', re.S)
a = re.findall(n, res.text)
for i in a:
    print(i)
