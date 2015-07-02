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

def setTDKAvailablity(deviceIP,devicePort,option):

	# Syntax       : setTDKAvailablity.setTDKAvailablity( deviceIP,devicePort,option )
	# Description  : Sends a json query to enable/disable TDK in device under test.
	# Parameters   : deviceIP - IP address of the device under test.
	#		 devicePort - Port Number of the device under test.
	#                option - enable/disable
	# Return Value : Returns string which holds status.

	try:
        	port = devicePort
        	tcpClient = socket.socket()
        	tcpClient.connect((deviceIP, port))

		print "Option : " , option

		if "enable" in option:
			jsonMsg = {'jsonrpc':'2.0','id':'2','method':'callEnableTDK'}
		elif "disable" in option:
			jsonMsg = {'jsonrpc':'2.0','id':'2','method':'callDisableTDK'}
		else:
			print "Invalid Option. Option should be enable/disable"
			sys.exit()
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
			print "Status : ", message
			sys.stdout.flush()

                return message

	except socket.error:
		print "AGENT_NOT_FOUND"
		sys.stdout.flush()

