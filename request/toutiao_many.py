from urllib.parse import urlencode
import re
import requests
import threading,time


def get_img_url(url, head):
    res = requests.get(url, headers=head)
    a = re.findall('"large_image_url":"(.*?)"', res.text)
    return a


def download_img(img_url):
    name = img_url.split('/')[-1]
    img_res = requests.get(img_url)
    img_content = img_res.content
    print("正在下载\t{0}\n图片地址\t{1}".format(name, img_url))
    with open("./ppic/{0}".format(name), 'wb') as f:
        f.write(img_content)


def many_download(img_url_list):
    thrs = []
    for img_url in img_url_list:
        th = threading.Thread(target=download_img, args=(img_url,))
        thrs.append(th)
    for t in thrs:
        t.start()
    for t in thrs:
        t.join()


def main():
    start=time.time()
    offset = 80
    head = {
        'cookie': '你的登录cookie',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
    }
    for i in range(4):
        parms = {
            'aid': '24',
            'app_name': 'web_search',
            'offset': offset,
            'format': 'json',
            'keyword': '美女',
            'count': '20',
        }
        url = "https://www.toutiao.com/api/search/content/?{0}".format(urlencode(parms))
        offset += 20
        print("正在下载\t{0}".format(url))
        img_url_list = get_img_url(url, head)
        many_download(img_url_list)
        end=time.time()
        print(end-start)
        # print(img_url)

if __name__ == '__main__':
    main()
