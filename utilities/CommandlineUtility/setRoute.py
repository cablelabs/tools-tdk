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

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def setRoute(deviceIP,devicePort,clientMAC,clientAgentPort,clientStatusPort,clientLogTransferPort,clientAgentMonitorPort):

        # Syntax       : devicestatus.setRoute(deviceIP,devicePort,clientMAC,clientAgentPort,clientStatusPort,clientLogTransferPort)
        # Description  : Sends a json message to set the route for device with given MAC address
        # Parameters   : deviceIP - IP address of the gateway device.
	#		 devicePort - Port number of the gateway device.
	#		 clientMAC - MAC address of device whose route to be set.
	#		 clientAgentPort - Port number of gateway box to be forwarded for agent execution.
	#		 clientStatusPort - Port number of gateway box to be forwarded for status checking.
	#		 clientLogTransferPort - Port number of gateway box to be forwarded for log transfer.
	#		 clientAgentMonitorPort - Port number of gateway box to be forwarded for agent monitoring.
        # Return Value : Returns string which holds success or failure.

	try:
        	port = devicePort
        	tcpClient = socket.socket()
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'setClientRoute','MACaddr':clientMAC,'agentPort':clientAgentPort,'statusPort':clientStatusPort,'logTransferPort':clientLogTransferPort,'agentMonitorPort':clientAgentMonitorPort}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		tcpClient.setblocking(0)
		recvStatus = select.select([tcpClient], [], [], 5) #Setting timeout for response(3 Sec)
		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()

		resultIndex = result.find("result") + len("result"+"\":\"")
                message = result[resultIndex:]
                message = message[:(message.find("\""))]
                print message

	except socket.error:
		print "NOT_FOUND"

