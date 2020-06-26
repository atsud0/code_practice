import socket
import threading

"""收信息函數,默認接收值的大小爲1024字節,必須將收到的內容進行解碼,
如果收到exit時,關閉自己連接的套接字"""


def recv_message(sock):
    while True:
        try:
            recv_msg = sock.recv(1024)
            decode_recv_msg = recv_msg.decode('UTF-8')
            print(">:...." + decode_recv_msg)
            if 'exit' in decode_recv_msg:
                break
        except:
            print("對方服務器終結了你的連接.")
            break


'''連接函數,傳入一個ip和port,返回一個套接字####這裏還可以加個捕獲異常,...避免出現網絡異常等..'''


def connect(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock


'''
發信息函數,如果發送exit時,也關閉套接字.
'''


def send_message(sock):
    while True:
        try:
            mess = input("請輸入信息:")
            sock.send(mess.encode('utf-8'))
            if 'exit' in mess:
                sock.close()
        except:
            print("對方服務器終結了你的連接.")
            break


def main():
    ip = '127.0.0.1'
    port = 1233
    sock = connect(ip, port)
    th_send = threading.Thread(target=send_message, args=(sock,))
    th_send.start()
    th = threading.Thread(target=recv_message, args=(sock,))
    th.start()


"""程序的主入口"""
if __name__ == '__main__':
    main()
