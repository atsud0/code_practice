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


import socket
import time
import re


def Main():
    serverIP = '10.10.117.8'  # Get ip from user input
    serverPort = 1337
    oldNum = 0  # Start at 0 as per instruction

    while serverPort != 9765:
        try:  # try until port 1337 available
            if serverPort == 1337:
                print(f"Connecting to {serverIP} waiting for port {serverPort} to become available...")

            # Create socket and connect to server
            s = socket.socket()
            s.connect((serverIP, serverPort))

            # Send get request to server
            gRequest = f"GET / HTTP/1.0\r\nHost: {serverIP}:{serverPort}\r\n\r\n"
            s.send(gRequest.encode('utf8'))

            # Retrieve data from get request
            while True:
                response = s.recv(1024)
                if (len(response) < 1):
                    break
                data = response.decode("utf8")

            # Format and assign the data into usable variables
            op, newNum, nextPort = assignData(data)
            # Perform given calculations
            oldNum = doMath(op, oldNum, newNum)
            # Display output and move on
            print(f"Current number is {oldNum}, moving onto port {nextPort}")
            serverPort = nextPort

            s.close()

        except:
            s.close()
            time.sleep(3)  # Ports update every 4 sec
            pass

    print(f"The final answer is {round(oldNum, 2)}")


def doMath(op, oldNum, newNum):
    if op == 'add':
        return oldNum + newNum
    elif op == 'minus':
        return oldNum - newNum
    elif op == 'divide':
        return oldNum / newNum
    elif op == 'multiply':
        return oldNum * newNum
    else:
        return None


def assignData(data):
    dataArr = re.split(' |\*|\n', data)  # Split data with multi delim
    dataArr = list(filter(None, dataArr))  # Filter null strings
    # Assign the last 3 values of the data
    op = dataArr[-3]
    newNum = float(dataArr[-2])
    nextPort = int(dataArr[-1])

    return op, newNum, nextPort


if __name__ == '__main__':
    Main()
