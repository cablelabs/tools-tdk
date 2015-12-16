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

# Methods

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

# Check the number of arguments and print the syntax if args not equal to 4
if ( (len(sys.argv)) != 4):
        print "Usage : python " + sys.argv[0] + " Device_IP_Address Port_Number LogFile(Name of log file to be removed)"
	print "eg    : python " + sys.argv[0] + " 192.168.160.130 8088 log.zip"
	exit()

# Assigning IP address, port number and file to be reomved
ipaddrs = sys.argv[1]
deviceport = int (sys.argv[2])
filename = sys.argv[3]

# Sending json request and receiving response
try:
	tcpClient = getSocketInstance(ipaddrs)
	tcpClient.connect((ipaddrs, deviceport))

	jsonMsg = {'jsonrpc':'2.0','id':'2','method':'executeRemoveLogsScript','argument':filename}
	query = json.dumps(jsonMsg)
	tcpClient.send(query) #Sending json query

	result = tcpClient.recv(1048) #Receiving response

	tcpClient.close()

	if "Method not found" in result:
		print "Agent not registered with RPC Method"
		exit()

	# Extracting result from response message
	resultIndex = result.find("result") + len("result"+"\":\"")
	message = result[resultIndex:]
	message = message[:(message.find("\""))]
	print message.upper()

except socket.error:
	print "Unable to reach agent"
	exit()

# End of File
