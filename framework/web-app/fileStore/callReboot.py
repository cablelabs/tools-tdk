#!/usr/bin/python

#============================================================================
#COMCAST CONFIDENTIAL AND PROPRIETARY
#============================================================================
#This file and its contents are the intellectual property of Comcast.  It may
#not be used, copied, distributed or otherwise  disclosed in whole or in part
#without the express written permission of Comcast.
#============================================================================
#Copyright (c) 2013 Comcast. All rights reserved.
#============================================================================

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import socket
import select
import json
import sys

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

def callReboot(deviceIP,devicePort):

        # Syntax       : callReboot.callReboot( deviceIP,devicePort )
        # Description  : Sends a json query to reboot connected STB.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 devicePort - Port Number of the device under test. 
        # Return Value : Nil

	try:
        	port = devicePort
		tcpClient = getSocketInstance(deviceIP)
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'RebootBox'}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()

		if "Method not found." in result:
                        print "METHOD_NOT_FOUND"
			sys.stdout.flush()

		else:
			resultIndex = result.find("result") + len("result"+"\":\"")
	                message = result[resultIndex:]
        	        message = message[:(message.find("\""))]
			print message
			sys.stdout.flush()

	except socket.error:
		print "AGENT_NOT_FOUND"
		sys.stdout.flush()

