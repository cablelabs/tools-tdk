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

def getConnectedDevices(deviceIP,devicePort):

        # Syntax       : getDevices.getConnectedDevices( deviceIP,devicePort )
        # Description  : Sends a json query to get the MAC address of connected devices from the json response.
        # Parameters   : deviceIP - IP address of the device under test(Gateway box).
	#		 devicePort - Port Number of the device under test(Gateway box). 
        # Return Value : Returns string which holds MAC address of connected devices.

	try:
        	port = devicePort
		tcpClient = getSocketInstance(deviceIP)
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'getConnectedDevices'}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		tcpClient.setblocking(0)
		recvStatus = select.select([tcpClient], [], [], 3) #Setting timeout for response(3 Sec)
		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close() 

		resultIndex = result.find("result") + len("result"+"\":\"")

                message = result[resultIndex:]
                message = message[:(message.find("\""))]
                print message

	except socket.error:
		print "AGENT_NOT_FOUND"

