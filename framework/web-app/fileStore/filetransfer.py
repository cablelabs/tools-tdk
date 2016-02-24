#============================================================================
#COMCAST CONFIDENTIAL AND PROPRIETARY
#============================================================================
#This file and its contents are the intellectual property of Comcast.  It may
#not be used, copied, distributed or otherwise  disclosed in whole or in part
#without the express written permission of Comcast.
#============================================================================
#Copyright (c) 2013 Comcast. All rights reserved.
#============================================================================

# Module Imports
import socket
import sys
import json

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

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

# Check the number of arguments and print the syntax if args not equal to 5
if((len(sys.argv))!=5):
        print "Usage : python " + sys.argv[0] + " DeviceIP AgentMonitorPortNumber BoxFileName TMFileName"
        print "eg    : python " + sys.argv[0] + " 192.168.160.189 8090 \"/version.txt\" \"111_222_333_version.txt\""
	sys.exit()

# Assigning IP address, port number and path of source and destination files
deviceIP = sys.argv[1]
agentMonitorPort = int (sys.argv[2])
boxFile = sys.argv[3]
tmFile = sys.argv[4]

try:
	tcpClient = getSocketInstance(deviceIP)
	tcpClient.connect((deviceIP, agentMonitorPort))

	# Sending message to push the logs from STB to TM
	jsonMsg = {'jsonrpc':'2.0','id':'2','method':'PushLog','STBfilename':boxFile,'TMfilename':tmFile}
	query = json.dumps(jsonMsg)
	tcpClient.send(query) #Sending json query

	result = tcpClient.recv(1048) #Receiving response
	tcpClient.close()

	resultIndex = result.find("result") + len("result"+"\":\"")
	message = result[resultIndex:]
	message = message[:(message.find("\""))]
	print message
	sys.stdout.flush()

except socket.error:
	print "ERROR: Unable to connect agent.."
	sys.stdout.flush()
	sys.exit()

except TypeError:
	print "Connection Error!!! Transfer of " + boxFile + " Failed: Make sure Agent is running"
	sys.exit()

except:
	print "Error!!! Transfer of " + boxFile + " Failed.."
	sys.exit()

#End of file
