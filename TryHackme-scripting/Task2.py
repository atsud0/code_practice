"""

房间链接:https://tryhackme.com/room/scripting

Task2:
You need to write a script that connects to this webserver on the correct port, do an operation on a number and then move onto the next port. Start your original number at 0.

The format is: operation, number, next port.

For example the website might display, add 900 3212 which would be: add 900 and move onto port 3212.

Then if it was minus 212 3499, you'd minus 212 (from the previous number which was 900) and move onto the next port 3499

Do this until you the page response is STOP (or you hit port 9765).

Each port is also only live for 4 seconds. After that it goes to the next port. You might have to wait until port 1337 becomes live again...

Go to: http://<machines_ip>:3010 to start...

General Approach(it's best to do this using the sockets library in Python):

    Create a socket in Python using the sockets library
    Connect to the port
    Send an operation
    View response and continue



"""

import socket, re, time


def server_connect(host, port):
    s = socket.socket()
    message = 0
    addr = (host, port)

    s.connect(addr)

    gRequest = f"GET / HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n"
    s.send(gRequest.encode('UTF-8'))
    while True:
        data = s.recv(4096)
        count = len(data)
        if count == 0:
            break
        message = str(data, encoding='UTF-8')
    s.close()

    return message


def get_port(message):
    message = message.split('\n')
    ret = message[-1].split(" ")
    return ret


host = '10.10.117.8'
port = 1337
num = 0
num_list = []
op_list = []
while 1:
    try:
        data = server_connect(host, port)
        do_list = get_port(data)
        print(do_list)
        new_port = int(do_list[2])
        num_list.append(float(do_list[1]))
        op_list.append(do_list[0])
        break
    except Exception as error:
        print("等待重置{0},{1}".format(port, error))
        time.sleep(2)
        pass

if new_port != 1337:
    while 1:
        try:
            data = server_connect(host, new_port)
            do_list = get_port(data)
            new_port = int(do_list[2])
            num_list.append(float(do_list[1]))
            op_list.append(do_list[0])
            print(do_list)
            if new_port == 9765:
                break
        except Exception as error:
            print("等待重置{0},{1}".format(new_port, error))
            time.sleep(2)
            pass

for i in range(len(op_list)):
    if op_list[i] == 'minus':
        num -= num_list[i]
    elif op_list[i] == 'multiply':
        num *= num_list[i]
    elif op_list[i] == 'add':
        num += num_list[i]
    elif op_list[i] == 'divide':
        num /= num_list[i]

print(num)
