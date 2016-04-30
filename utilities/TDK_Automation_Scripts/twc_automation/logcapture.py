#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
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
import time

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def captureLogs(deviceIP,devicePort,Status,commandType,commandOutput):

        # Syntax       : captureLogs( deviceIP,devicePort )
        # Description  : Sends a json query to capture logs on STB.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 devicePort - Port Number of the device under test. 
        # Return Value : Returns string with true/false.

	try:
        	port = devicePort
       		tcpClient = socket.socket()
		tcpClient.connect((deviceIP, port))
		
	   	jsonMsg = {'jsonrpc':'2.0','id':'2','method':'LogCapture','logStatus':Status,'logType':commandType, 'logDestination':commandOutput}
		query = json.dumps(jsonMsg)
		print "Cmd to STB : " + str(jsonMsg)
		tcpClient.send(query) #Sending json query
		recvStatus = select.select([tcpClient], [], [], 3) #Setting timeout for response(3 Sec)
		result=""
		decoded=""
		value=""
		if recvStatus[0]:
			result = tcpClient.recv(1048) #Receiving response
			print "From Stub : " + result
		tcpClient.close()
		print "Response message : "+str(result)
		if result != "":
			decoded = json.loads(result)
			print decoded
		try :
			if 'result' in decoded and 'details' in decoded:
				print "Result : ", decoded['result']
				print "Details:",decoded['details']
				value = decoded['details']
			else:
				print "Error....."
		except:
			print "Error in fetching details.."
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
