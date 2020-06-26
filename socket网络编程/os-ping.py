import os
import platform
import threading
from scan_open import *


lock = threading.Lock()
active_ips = 0
active_ip_list =[]

def check_os():
    os_str = platform.system()
    if os_str == 'Windows':
        return '-n'
    elif os_str == 'Linux':
        return '-c'


def ping_once(ip, packs):
    global active_ips
    global active_ip_list
    cmd = 'ping {0} {1} 2'.format(ip, packs)
    # if ip == '192.168.40.255':
    #     cmd='ping {0} -c 2 -b'.format(ip)
    res = os.popen(cmd)
    if 'ttl' not in res.read().lower():
        # print('{0}不成功'.format(ip))
        pass
    else:
        print("[+]{0}活跃".format(ip))
        scan_all(ip)
        # with open('./ip.txt', 'a') as f:
        #    print("[+]{0}活跃".format(ip), sep='\n', file=f)
        lock.acquire()
        active_ips += 1
        active_ip_list.append(ip)
        lock.release()


def ping(ips, packs):
    thrs = []
    for ip in ips:
        th = threading.Thread(target=ping_once, args=(ip, packs,))
        thrs.append(th)
    for t in thrs:
        t.start()
    for t in thrs:
        t.join()


def get_ips():
    ip = input('请输入IP\t例如:192.168.2.0\t :').strip()
    #ip='192.168.40.1'
    ip = ip.split('.')
    for i in ip:
        if int(i) < 0 or int(i) > 255:
            print('你输入的网段不正确')
    new_ip = "{0}.{1}.{2}.".format(ip[0], ip[1], ip[2])
    ips = []
    for i in range(1, 255):
        ip = '{0}{1}'.format(new_ip, i)
        ips.append(ip)
    return ips


def main():
    socket.setdefaulttimeout(1)     #必須設置超時時間,否則會因爲等待時間無法開啓新的進程
    print("输入一个ip ping 该ip网段下的所有主机,来获得存活主机数\n{0}".format('-' * 100))
    packs = check_os()
    ips = get_ips()
    ping(ips, packs)
    print('{1}\n总共活跃的主机数:{0}'.format(active_ips, '-' * 1))
    # ps=[]
    # pool = multiprocessing.Pool() # 初始化進程池
    # print("CPU内核数:{}".format(multiprocessing.cpu_count()))
    # print('当前母进程: {}'.format(os.getpid()))
    # for ip in active_ip_list:
    #     print('{0}\n正在掃描{1}\n{2}'.format('-'*100,ip,'-'*100))
    #     r=pool.apply(scan_all, args=(ip,))
    #     pool.apply_async(scan_all, args=(ip,))
    # pool.close()
    # pool.join()
        #scan_all(ip)
        # p=multiprocessing.Process(target=scan_all,args=(ip,))
        # ps.append(p)
        #r=pool.apply(scan_all, args=(ip,))
    # for p in ps:
    #     p.start()
    # for p in ps:
    #     p.join()
        #pool.map(scan_all,ip)
        #pool.join()


if __name__ == '__main__':
    main()
