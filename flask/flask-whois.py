"""
可以做到的事情:
    输入域名获取whois信息
    输入IP 以ICMP方式探测存活主机

TODO:
    增加数据库记录
    增加生成缓冲区字符功能?
    分模块,不要把所有函数都挤在一块
"""

from flask import Flask, render_template, request  # 从 falsk 模块中导入Flask类,render_template
import requests
import re
import os
import threading

lock = threading.Lock()
active_ips = 0
active_ip_list = []
new_active_ip_list = []
app = Flask(__name__)

"""使用jinjia模板渲染"""


@app.route('/')
def get_url():
    return render_template('get_url.html')


@app.errorhandler(404)
def page_not_found(error):
    return '来到了没有知识的荒原', 404


"""從post處接受數據"""


@app.route('/whois', methods=['POST'])
def get_whois():
    url = request.form['url']
    get_whois_url = 'https://www.whois.com/whois/{0}'.format(str(url))
    res = requests.get(get_whois_url)
    re_expression = re.compile('id="registrarData">(.*)</pre></div>', re.S)
    whois_text = re.findall(re_expression, res.text)
    whois_text = whois_text[0].split("\n")
    return render_template('url_info.html', whois_texts=whois_text, the_url=url)


def ping_once(ip):
    global active_ips
    global active_ip_list
    global new_active_ip_list
    cmd = 'ping -c 1 {0} '.format(ip)
    res = os.popen(cmd)
    if 'ttl' not in res.read().lower():
        pass
    else:
        # print("[+]{0}活跃".format(ip))
        # with open('./ip.txt', 'a') as f:
        #    print("[+]{0}活跃".format(ip), sep='\n', file=f)
        lock.acquire()
        active_ips += 1
        active_ip_list.append(ip)
        lock.release()


def ping(ips):
    global active_ip_list
    global new_active_ip_list
    thrs = []
    for ip in ips:
        th = threading.Thread(target=ping_once, args=(ip,))
        thrs.append(th)
    for t in thrs:
        t.start()
    for t in thrs:
        t.join()
    new_active_ip_list = active_ip_list[::]
    active_ip_list = []  # 重置列表


@app.route('/ping', methods=['POST'])
def get_ip():
    ip = request.form['ip']
    try:
        ip = ip.split('.')
        for i in ip:
            if int(i) < 0 or int(i) > 255:
                return '你输入的IP不正确'
        new_ip = "{0}.{1}.{2}.".format(ip[0], ip[1], ip[2])
        ips = []
        for i in range(1, 255):
            ip = '{0}{1}'.format(new_ip, i)
            ips.append(ip)
        ping(ips)

        return render_template('live-ip.html', ips=new_active_ip_list)
    except:
        return page_not_found(404)


if __name__ == '__main__':
    app.run(debug=True)
