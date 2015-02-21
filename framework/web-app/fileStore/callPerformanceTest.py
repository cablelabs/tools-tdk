#
# ============================================================================
# COMCAST C O N F I D E N T I A L AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of Comcast.  It may
# not be used, copied, distributed or otherwise  disclosed in whole or in part
# without the express written permission of Comcast.
# ============================================================================
# Copyright (c) 2014 Comcast. All rights reserved.
# ============================================================================
#

# Module Imports
import tftpy
import sys
import socket
import json

def tftpDownload(ipaddrs, logtransferport, remotefile, localfile):

	# Connect to TFTP server and download the file
	try:
		client = tftpy.TftpClient (ipaddrs, logtransferport)
		client.download (remotefile, localfile)

	except TypeError:
		print "Connection Error!!! Transfer of " + remotefile + " Failed: Make sure Agent is running"
		exit()

	except:
		print "Error!!! Transfer of " + remotefile + " Failed.."
		exit()


# Check the number of arguments and print the syntax if args not equal to 5
if ( (len(sys.argv)) != 6):
        print "Usage : python " + sys.argv[0] + " Device_IP_Address Agent_Port_Number Log_Transfer_Port RPC_Method Local_file_path"
	print "eg    : python " + sys.argv[0] + " 192.168.160.130 8087 69 RPC_Method_Name(PerformanceBenchMarking/PerformanceSystemDiagnostics) \"/filestore/version/version.txt\""
	exit()

# Assigning IP address, port numbers, path of destination files and rpcmethod to be invoked
ipaddrs = sys.argv[1]
deviceport = int (sys.argv[2])
logtransferport = int (sys.argv[3])
rpcmethod = sys.argv[4]
localfilepath = sys.argv[5]

# Sending json request and receiving response
try:
	tcpClient = socket.socket()
	tcpClient.connect((ipaddrs, deviceport))

	jsonMsg = {'jsonrpc':'2.0','id':'2','method':rpcmethod}
	query = json.dumps(jsonMsg)
	tcpClient.send(query) #Sending json query

	result = tcpClient.recv(1048) #Receiving response

	tcpClient.close()
	# Extracting result and logpath from response message
	resultIndex = result.find("result") + len("result"+"\":\"")
	message = result[resultIndex:]
	message = message[:(message.find("\""))]

	resultIndex = result.find("logpath") + len("logpath"+"\":\"")
	message = result[resultIndex:]
	message = message[:(message.find("\""))]
	logpath = message

except socket.error:
	print "Unable to reach agent"
	exit()

if "PerformanceSystemDiagnostics" in rpcmethod:

	# Constructing path for remote and local files
	remotefile = logpath + "/cpu.log"
	localfile = localfilepath + "/cpu.log"

	tftpDownload(ipaddrs, logtransferport, remotefile, localfile)

	# Constructing path for remote and local files
	remotefile = logpath + "/memused.log"
	localfile = localfilepath + "/memused.log"

	tftpDownload(ipaddrs, logtransferport, remotefile, localfile)

else:
	# Downloading files using TFTP
	filename = logpath.split("/")[-1]
	remotefile = logpath
	localfile = localfilepath + "/" + filename
	tftpDownload(ipaddrs, logtransferport, remotefile, localfile)

# End of File
