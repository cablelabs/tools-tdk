# Python TFTP Client using tftpy module 

import tftpy
IPAddr='127.0.0.1'
port=69
remoteFileName='test.txt'
localFileName='TestReceived.txt'
client = tftpy.TftpClient(IPAddr, port)
client.download(remoteFileName,localFileName)
