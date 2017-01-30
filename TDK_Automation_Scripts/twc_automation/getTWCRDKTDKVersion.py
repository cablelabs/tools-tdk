#!/usr/bin/python
#
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
		if 'result' in decoded and 'details' in decoded :
			print "Result : ", decoded['result']
			version = decoded['details'].split(":")[-1].replace("\"","").replace(",","")
			print "Version : ", decoded['details'].split(":")[-1].replace("\"","").replace(",","").replace(" ","")
		else:
			print "Error in fetching RDK TDK Details.."
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

