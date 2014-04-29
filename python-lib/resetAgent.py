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

def resetAgent(deviceIP,devicePort,enableReset):

        # Syntax       : getDevices.getConnectedDevices( deviceIP,devicePort )
        # Description  : Sends a json query to get the MAC address of connected devices from the json response.
        # Parameters   : deviceIP - IP address of the device under test(Gateway box).
	#		 devicePort - Port Number of the device under test(Gateway box). 
        # Return Value : Returns string which holds MAC address of connected devices.

	try:
        	port = devicePort
        	tcpClient = socket.socket()
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'ResetAgent','enableReset':enableReset}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()

		resultIndex = result.find("result") + len("result"+"\":\"")

                message = result[resultIndex:]
                message = message[:(message.find("\""))]
                if "SUCCESS" in message.upper():
			print "Test timed out.. Agent Reset.."
		else:
			print "Test timed out.. Failed to reset agent.."
		sys.stdout.flush()

	except socket.error:
		print "ERROR: Script timed out.. Unable to reach agent.." 
		sys.stdout.flush()

