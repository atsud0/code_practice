import socket
import threading
import multiprocessing


# pool=None
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 套接字(端對端),客戶端只能建立一個連接.
def get_ips():
    d = []
    with open('./ip.txt', 'r') as f:
        for c in f.readlines():
            for i in c:
                if i.isdigit():
                    d.append(i)
                elif '.' in i:
                    d.append(i)
            d.append('/')
    host = "".join(d)
    hosts = host.split("/")
    return hosts.pop(-1)


def scan_once(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("[+] {0}\t{1} port is open".format(host,port))
        sock.close()
    except:
        pass


def scan_all(host):
    thrs = []
    #print("{0}正在扫描{1}\n{2}".format('-' * 100, host, '-' * 100))
    for port in range(1, 65536):
        th = threading.Thread(target=scan_once, args=(host, port,))
        thrs.append(th)
    for t in thrs:
        t.start()
    for t in thrs:
        t.join()


if __name__ == '__main__':
    socket.setdefaulttimeout(1)
    pool = multiprocessing.Pool()
    d = []
    with open('./ip.txt', 'r') as f:
        for c in f.readlines():
            for i in c:
                if i.isdigit():
                    d.append(i)
                elif '.' in i:
                    d.append(i)
            d.append('/')
    host = "".join(d)
    hosts = host.split("/")
    for host in hosts:
        print('正在掃描:{}'.format(host))
        r=pool.apply(scan_all, args=(host,))

#     th_host = threading.Thread(target=scan_all, args=(host,))
# for t in thrs_host:
#     t.start()
# for t in thrs_host:
#     t.join()

#     print("正在檢測{0}".format(port))
#     sock.connect((host, port))
#     print("[+] {0} port is open".format(port))
#
# print("{0}不開放".format(port))
