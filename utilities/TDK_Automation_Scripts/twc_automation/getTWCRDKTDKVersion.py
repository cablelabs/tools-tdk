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

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def getTWCRDKTDKVersion(deviceIP,devicePort,FilePathToRead,SearchString):

        # Syntax       : getRDKTDKVersion.getRDKTDKVersion( deviceIP,devicePort )
        # Description  : Sends a json query to get the RDK version of device.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 devicePort - Port Number of the device under test. 
        # Return Value : Returns string which holds RDK version of connected devices.

	try:
        	port = devicePort
        	tcpClient = socket.socket()
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'GetTWCRDKTDKVersion','FilePathToRead':FilePathToRead,'SearchString':SearchString}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		tcpClient.setblocking(0)
		recvStatus = select.select([tcpClient], [], [], 3) #Setting timeout for response(3 Sec)
		result=""
		decoded=""
		if recvStatus[0]:
			result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()
		print "Response message : "+str(result)
		if result != "":
			decoded = json.loads(result)
		try :
			if 'result' in decoded and 'details' in decoded :
				print "Result : ", decoded['result']
				print "Version : ", decoded['details'].split(":")[-1].replace("\"","").replace(",","").replace(" ","")
				version = decoded['details'].split(":")[-1].replace("\"","").replace(",","")
			else:
				print "Error in fetching RDK TDK Details.."
				version = "Error"
		except:
                        print "Error in fetching RDK TDK version Details.."
                        version = "Error"

		if "Method not found." in result:
                        print "METHOD_NOT_FOUND"
			sys.stdout.flush()

		else:
			resultIndex = result.find("result") + len("result"+"\":\"")
	                message = result[resultIndex:]
        	        message = message[:(message.find("\""))]
			print message
			sys.stdout.flush()

		return version

	except socket.error:
		print "AGENT_NOT_FOUND"
		sys.stdout.flush()

