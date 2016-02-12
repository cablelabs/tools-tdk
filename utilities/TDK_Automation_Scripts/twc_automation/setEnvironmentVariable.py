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

def setEnvironmentVariable(deviceIP,devicePort,variablename,value):

        # Syntax       : getGetEnvironmentVariable.getGetEnvironmentVariable( deviceIP,devicePort )
        # Description  : Sends a json query to get the RDK version of device.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 devicePort - Port Number of the device under test. 
        # Return Value : Returns string which holds RDK version of connected devices.

	try:
        	port = devicePort
        	tcpClient = socket.socket()
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'SetEnvironmentVariable','variablename':variablename,'value':value}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		tcpClient.setblocking(0)
		recvStatus = select.select([tcpClient], [], [], 8) #Setting timeout for response(3 Sec)
		result=""
		decoded=""
		if recvStatus[0]:
			result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()
		print "Response message : "+str(result)
		if result != "":
			decoded = json.loads(result)
		#print json.dumps(decoded, sort_keys=True, indent=4)
		if 'result' in decoded :
			print "Result : ", decoded['result']
			print "Details:",decoded['details']
		else:
			print "Error in fetching Environment variables.."
			value = "Error"

		if "Method not found." in result:
                        print "METHOD_NOT_FOUND"
			sys.stdout.flush()

		else:
			print value
			sys.stdout.flush()

		return value

	except socket.error:
		print "AGENT_NOT_FOUND"
		sys.stdout.flush()

