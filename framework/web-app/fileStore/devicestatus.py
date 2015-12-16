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
import socket
import select
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

def getStatus(deviceIP,managerIP,boxName,statusPort):

        # Syntax       : devicestatus.getStatus( deviceIP, managerIP, boxName, statusPort)
        # Description  : Sends a json query and decides the status of device from the json response.
        # Parameters   : deviceIP - IP address of the device whose status to be checked.
	#		 managerIP - IP address of test manager.
	#		 boxName - Box friendly name.
	#		 statusPort - port used for status checking.
        # Return Value : Returns string which holds status of device.

	try:
        	port = statusPort
		tcpClient = getSocketInstance(deviceIP)
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'getHostStatus','managerIP':managerIP,'boxName':boxName}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		tcpClient.setblocking(0)
		recvStatus = select.select([tcpClient], [], [], 5) #Setting timeout for response(3 Sec)
		if recvStatus[0]:
	       		result = tcpClient.recv(1048) #Receiving response
			tcpClient.close()
			if "Free" in result:
        			return "FREE"
			if "Busy" in result:
        			return "BUSY"
			if "TDK Disabled" in result:
				return "TDK_DISABLED"

		else:
			tcpClient.close()
			return "HANG"

	except socket.error:
		return "NOT_FOUND"

