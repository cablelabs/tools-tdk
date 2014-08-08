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
import sys

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def resetAgent(deviceIP,devicePort,enableReset):

        # Syntax       : resetAgent.resetAgent (deviceIP,devicePort,enableReset)
        # Description  : Sends a json message to reset agent.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 devicePort - Port Number of the device under test.
	#		 enableReset - true/false 
	#		 true - To restart agent
	#		 false - To reset device state to FREE
        # Return Value : Nil

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

