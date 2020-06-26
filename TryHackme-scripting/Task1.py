#!/usr/bin/python3
"""

房间链接:https://tryhackme.com/room/scripting

task_1
This file has been base64 encoded 50 times - write a script to retrieve the flag. Here is the general process to do this:

    read input from the file
    use function to decode the file
    do process in a loop

Try do this in both Bash and Python!

"""


import base64

#打开base64加密的文件,只读

with open("./b64.txt",mode='r') as f:
    # 一次性读取文本文件 将内容存入base_text
    base_text=f.read()

    #解密x次
    for i in range(0,50):
        base_text=base64.b64decode(base_text)
    print(base_text)

    """下面被注释的代码是另外一个房间解密15次的"""
    # base16解码
    # for i in range(0,5):
    #     base_text=base64.b16decode(base_text)
    #
    # # base32解码
    # for i in range(0,5):
    #     base_text=base64.b32decode(base_text)
    #
    # # base64解码
    # for i in range(0,5):
    #     base_text=base64.b64decode(base_text)
    #
    # print(base_text)




