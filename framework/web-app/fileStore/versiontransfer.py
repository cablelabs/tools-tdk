import tftpy
import sys

IP = <ipaddress>
PORT = <port> 
RemoteFile = "/version.txt"
LocalFile = <localfile>

try:
	client = tftpy.TftpClient( IP, PORT )
	client.download( RemoteFile, LocalFile )
       
except TypeError:
       	print "Connection Error!!! Transfer of " + RemoteFile + " Failed: Make sure Agent is running"

except:
       	print "Error!!! Transfer of " + RemoteFile + " Failed.."
 

