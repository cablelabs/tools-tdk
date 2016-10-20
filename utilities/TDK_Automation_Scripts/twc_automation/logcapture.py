#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

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
