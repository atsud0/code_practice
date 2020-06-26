import re
import requests
import threading

"""
爬取猫眼电影top100
"""

def get_one_info(url, head):
    res = requests.get(url, headers=head)
    res.encoding = 'utf-8'
    info_og = res.text
    pattern = re.compile('name.*(films.*?)".*title="(.*?)".*\n\s*<p.*?\n\s*(.*)\n.*\n.*time">(.*?)<')
    info = re.findall(pattern, info_og)
    for i in range(len(info)):
        print("{1}{0}".format(info[i][0], 'https://maoyan.com/'), end="\t")
        print("电影名称:{0}".format(info[i][1]), end="\t\t")
        print("{0}".format(info[i][2]), end="\t\t")
        print("{0}".format(info[i][3]), end="\t\t")
        print()
        with open('dy.csv', 'r+', encoding='GBK') as f:
            print("电影名称:{0}\t\t{1}\t\t网页地址:https://maoyan.com/{2}\t\t{3}".format(info[i][1], info[i][2], info[i][0],
                                                                                  info[i][3]),
                  file=f,
                  sep='\n')


def get_many_info(head):
    thrs = []
    for i in range(10):
        page = i * 10
        url = 'https://maoyan.com/board/4?offset=' + '{0}'.format(page)
        th = threading.Thread(target=get_one_info, args=(url, head,))
        thrs.append(th)
    for t in thrs:
        t.start()
    for t in thrs:
        t.join()


def main():
    head = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    get_many_info(head)


if __name__ == '__main__':
    main()
