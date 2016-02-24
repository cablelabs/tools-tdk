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
import sys
import socket
import json

def isValidIpv6Address(ip):
                try:
                        socket.inet_pton(socket.AF_INET6, ip)
                except socket.error:  # not a valid address
                        return False
                return True

def getSocketInstance(ip):
                if isValidIpv6Address(ip):
                        tcpClient = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
                else:
                        tcpClient = socket.socket()
                return tcpClient

def tftpDownload(ipaddrs,agentmonitorport,boxFile,tmFile):

	# Connect to TFTP server and download the file
	try:
		tcpClient = getSocketInstance(ipaddrs)
		tcpClient.connect((ipaddrs, agentmonitorport))

		# Sending message to push the logs from STB to TM
		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'PushLog','STBfilename':boxFile,'TMfilename':tmFile}
		query = json.dumps(jsonMsg)
		tcpClient.send(query) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()

		resultIndex = result.find("result") + len("result"+"\":\"")
		message = result[resultIndex:]
		message = message[:(message.find("\""))]
		print message.upper()
		sys.stdout.flush()

	except TypeError:
		print "Connection Error!!! Transfer of " + boxFile + " Failed: Make sure Agent is running"
		sys.exit()

	except:
		print "Error!!! Transfer of " + boxFile + " Failed.."
		sys.exit()


# Check the number of arguments and print the syntax if args not equal to 6
if ( (len(sys.argv)) != 6):
	print "Usage : python " + sys.argv[0] + " Device_IP_Address Agent_Port_Number Agent_Monitor_Port RPC_Method TM_File_Name"
	print "eg    : python " + sys.argv[0] + " 192.168.160.130 8087 8090 RPC_Method_Name(PerformanceBenchMarking/PerformanceSystemDiagnostics) \"11_22_33_44version.txt\""
	exit()

# Assigning IP address, port numbers, path of destination files and rpcmethod to be invoked
ipaddrs = sys.argv[1]
deviceport = int (sys.argv[2])
agentmonitorport = int (sys.argv[3])
rpcmethod = sys.argv[4]
tmfilename = sys.argv[5]

# Sending json request and receiving response
try:
	tcpClient = getSocketInstance(ipaddrs)
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
	print message.upper()

	resultIndex = result.find("logpath") + len("logpath"+"\":\"")
	message = result[resultIndex:]
	message = message[:(message.find("\""))]
	logpath = message
	print "Log Path : " + logpath

except socket.error:
	print "Unable to reach agent"
	exit()


if "PerformanceSystemDiagnostics" in rpcmethod:

	# Constructing path for remote and local files
	boxFile = logpath + "/cpu.log"
	tmFile = tmfilename + "_cpu.log"

	tftpDownload(ipaddrs, agentmonitorport, boxFile, tmFile)

	# Constructing path for remote and local files
	boxFile = logpath + "/memused.log"
	tmFile = tmfilename + "_memused.log"

	tftpDownload(ipaddrs, agentmonitorport, boxFile, tmFile)

else:
	# Constructing path for remote and local files
	filename = logpath.split("/")[-1]
	boxFile = logpath
	tmFile = tmfilename + "_" +filename

        tftpDownload(ipaddrs, agentmonitorport, boxFile, tmFile)

# End of File
