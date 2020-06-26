 # README
 
 房间链接:[Scripting](https://tryhackme.com/room/scripting)
 
 只完成了前两个题目.
 
 第三题为
``` 
The VM you have to connect to has a UDP server running on port 4000. Once connected to this UDP server, send a UDP message with the payload "hello" to receive more information. You will find some sort of encryption(using the AES-GCM cipher). Using the information from the server, write a script to retrieve the flag. Here are some useful thingsto keep in mind:

    sending and receiving data over a network is done in bytes
    the PyCA encryption library and functions takes its inputs as bytes
    AES GCM sends both encrypted plaintext and tag, and the server sends these values sequentially in the form of the encrypted plaintext followed by the tag

This machine may take up to 5 minutes to configure once deployed. Please be patient. 

Use this general approach(use Python3 here as well):

    Use the Python sockets library to create a UDP socket and send the aforementioned packets to the server
    use the PyCA encyption library and follow the instructions from the server

 ```
 
