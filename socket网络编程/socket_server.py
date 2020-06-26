import socket
import threading

"""收信息函數,默認接收值的大小爲1024字節,必須將收到的內容進行解碼,
如果收到exit時,關閉客戶端的套接字,但是服務端還是能持續運行"""


def recv_message(client_sock):
    while True:
        try:
            recv_msg = client_sock.recv(1024)
            decode_recv_msg = recv_msg.decode('UTF-8')
            print(">:" + decode_recv_msg)
            if 'exit' in decode_recv_msg:
                client_sock.close()

        except:
            break


'''
發信息函數,如果發送exit時,也關閉客戶端套接字.
'''


def send_message(client_sock):
    while True:
        try:
            msg = input("输入:")
            client_sock.send(msg.encode('UTF-8'))
            if 'exit' in msg:
                client_sock.close()
        except OSError:
            print("目前好像沒有客戶端連接上了")
            break


"""建立一個監聽的連接"""


def creaet_listen(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen()
    print("開始監聽:...")
    while True:
        client_sock, client_ip = sock.accept()  # 收到連接後會返回一個套接字和一個客戶端ip地址和端口的元組
        print("ip:{client_ip},port:{client_port}建立了連接".format(client_ip=client_ip[0], client_port=client_ip[1]))
        '''
        客戶端如果發送allow才開啓通信,發送信息要進行utf-8轉碼
        如果客戶端發送其他的值就關閉客戶端的連接,不過關閉的時候,在客戶端處會有延遲,不是立刻就關閉
        '''
        allow_str=input("请输入....")
        if 'allow' in allow_str:
            send_msg = "you can send message now.."
            client_sock.send(send_msg.encode('utf-8'))
            th_recv = threading.Thread(target=recv_message, args=(client_sock,))
            th_recv.start()
            th_send = threading.Thread(target=send_message, args=(client_sock,))
            th_send.start()
        else:
            break



def main():
    ip = '127.0.0.1'
    port = 1233
    creaet_listen(ip, port)


"""程序的主入口"""
if __name__ == '__main__':
    main()
