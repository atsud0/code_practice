# coding:UTF-8
#!/usr/bin/python2
"""

基于<python黑帽子黑客与渗透测试编程之道>的python版netcat代码上做出了一点修改

1. 修改客户端连接显示错位的问题(执行之后显示上一条命令)
2. 原版代码处理接受参数有问题,无法正确处理-u的参数
3. 客户端可发送参数直接开shell,执行命令 (上传文件暂未做测试)

缺点:
受限于python 子线程不能切换目录,无法cd到指定目录
但是实际上是切换了,只是切换目录之后,又回到了原来的目录
造成了没有切换目录的效果

TODO:
客户端上传文件做测试
完善帮助菜单
添加加密,避免明文传输
修改客户端逻辑 实现能够在客户端用参数上传文件
添加服务端发送文件功能
"""

import sys
import socket
import getopt
import threading
import subprocess

# 初始化全局变量
listen = False
command = False
upload = False
execute = ''
target = ''
upload_source = ''
upload_destination = ''
port = 0

"""帮助菜单"""


def usage():
    print("""\t\t\tNet Tool
    
Usage:jetcat.py -t target_host -p port
-l \t\t --listen
-e \t\t --execute
-c \t\t --command
-u \t\t --upload

Examples:.....................
    """)

    sys.exit(0)


"""服务端函数"""


def server_loop():
    global target
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(2)  # 允许的连接数

    """等待连入,并分一个线程处理客户端"""
    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket, addr,))
        client_thread.start()
        # password=client_socket.recv(4096)
        # print(password)
        # if 'atsud0' in password:
        #     client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        #     client_thread.start()
        # else:
        #     client_socket.send("ACESS DENIED")
        #     client_socket.close()


"""原版客户端函数"""


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)  # 长度>1时就发送

        while True:
            recv_len = 1
            response = ''
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            print(response)

            buffer = raw_input("")
            buffer += "\n"
            client.send(buffer)

    except:
        print("[*] Exception Exiting")
        client.close()


def client_handler(client_socket, addr):
    global upload
    global execute
    global command
    global upload_destination
    print("Connected by {}".format(addr))
    buffer = ""

    """接受客户端的参数"""
    while True:
        buffer_tmp = client_socket.recv(4096)
        print(buffer_tmp)
        buffer += buffer_tmp
        if len(buffer_tmp) < 4096:
            break

    # 参数列表 处理-e 命令参数 水平不够,暂时只会这样处理
    param_list = buffer.split()
    for i in param_list:
        if '-e' in i:
            index = param_list.index(i)
            arg = param_list[index + 1::]
            param_list[index + 1] = " ".join(param_list[index + 1::])

    try:
        shortargs = "t:p:lce:u:h"
        longargs = ["target=", "port=", "listen", "commandshell", "execute=", "upload", "help"]
        opts, args = getopt.getopt(param_list, shortargs, longargs)
        print(opts)
    except Exception as error:
        print(error)
        usage()
        sys.exit(0)

    for o, a in opts:
        if o in ('-c', '--commandshell'):
            command = True
        elif o in ('-e', '--execute'):
            execute = a
            print(execute)
        elif o in ['-u', '--upload']:
            upload_destination = a.split(">")[1]
            print(upload_destination)

    if upload_destination:
        file_buffer = ""

        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            else:
                file_buffer += data
        try:
            if write_file(upload_destination, file_buffer):
                client_socket.send("Successfuly upload file{0}\r\n".format(upload_destination))
        except:
            client_socket.send("Failed to save file to{}\r\n".format(upload_destination))

    if execute:
        output = run_command(execute)
        client_socket.send(output)

    if command:
        client_socket.send("<Atsud0#:> ")
        while True:
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            response = run_command(cmd_buffer)
            client_socket.send(response)
            client_socket.send("<Atsud0#:> ")


"""执行命令函数"""


def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Faild to execute command \r\n"

    return output


"""写文件函数"""


def write_file(upload_destination, file_buffer):
    with open(upload_destination, "wb") as file:
        file.write(file_buffer)
    return True


"""读文件函数"""


def read_file(path):
    with open(path, "rb") as file:
        file_buffer = file.read()
    return file_buffer


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):  # sys.argv[0]=脚本名称 [1]->后面的就是参数 后面没有参数就直接输出帮助菜单
        usage()

    try:
        shortargs = "hle:u:t:p:c"  # 短参数
        longargs = ["help", "listen", "execute=", "upload=", "target=", "port=", "commandshell"]  # 长参数
        # opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:c:u",["help", "listen", "execute", "target", "port", "command", "upload"])
        opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)

    except getopt.GetoptError as error:
        print(error)
        usage()

    # print(opts)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-c', '--commandshell'):
            command = True
        elif o in ('-u', '--upload'):
            upload_destination = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert False, "Unhandled Option"

        # 判断监听还是发送数据
    if not listen and len(target) and port > 0:
        # buffer = sys.stdin.read()
        # buffer = raw_input("")
        # client_sender(buffer)
        client()

    if listen:
        server_loop()


def client():
    global port
    global execute
    global command
    global upload_source
    global target

    buffer = ""
    client_socket = socket.socket()
    try:
        client_socket.connect((target, port))
    except:
        print("[*] Exception Exiting")

    # 将客户端的参数传给服务端
    params = " ".join(sys.argv[1:])
    # print(params)
    # print(execute)
    client_socket.send(params)

    if upload_source:
        file_buffer = read_file(upload_source)
        client_socket.send(file_buffer)
        file_buffer = ""
        while True:
            file_tmp = client_socket.recv(1024)
            file_buffer += file_tmp
            if len(file_tmp) < 1024:
                break
        print(file_buffer)

    if execute:
        while True:
            output = client_socket.recv(1024)
            buffer += output
            if len(output) < 1024:
                break
        print(buffer)

    if command:
        print(client_socket.recv(1024))
        while True:
            buffer = ""
            cmd_buffer = raw_input("")
            cmd_buffer += "\n"
            client_socket.send(cmd_buffer)
            while True:
                buffer_tmp = client_socket.recv(1024)
                buffer += buffer_tmp
                if len(buffer_tmp) < 1024:
                    print(buffer)
                    break
                print(client_socket.recv(1024))
    client_socket.close()


if __name__ == '__main__':
    main()
