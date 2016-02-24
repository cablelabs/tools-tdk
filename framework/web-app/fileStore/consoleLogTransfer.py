#!/usr/bin/python
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

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import sys
import json
import socket

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


def consoleLogTransfer(deviceIP,agentMonitorPort,boxFileName,tmFileName):

        # Syntax       : consoleLogTransfer.consoleLogTransfer (deviceIP,agentMonitorPort,boxFileName,tmFileName)
        # Description  : Sends a json query to get path to console log file and transfer the same.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 agentMonitorPort - Port Number of the device under test.
	#		 boxFileName - Name of log file in box.
	#		 tmFileName - Name in which the file is saved in TM after transferring.
        # Return Value : Nil

	# Sending JSON request to get log path
	try:
		tcpClient = getSocketInstance(deviceIP)
		tcpClient.connect((deviceIP, agentMonitorPort))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'GetAgentConsoleLogPath'}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()

		resultIndex = result.find("result") + len("result"+"\":\"")

                message = result[resultIndex:]
                message = message[:(message.find("\""))]
		sys.stdout.flush()

	except socket.error:
		print "ERROR: Unable to connect agent.." 
		sys.stdout.flush()
		sys.exit()

	# Transferring file using TFTP
	try:

		boxFile = message + "/" + boxFileName
		tmFile = tmFileName
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

# End of File
