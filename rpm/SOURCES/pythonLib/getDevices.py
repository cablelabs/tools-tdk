#!/usr/bin/python
"""
File        : getDevices.py
Description : To get the list of connected devices
Version     : 1.0
Author      : ANOOP RAVI
Date        : 27/09/2013
"""

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import socket
import select
import json

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def getConnectedDevices(deviceIP,devicePort):

        # Syntax       : getDevices.getConnectedDevices( deviceIP,devicePort )
        # Description  : Sends a json query to get the MAC address of connected devices from the json response.
        # Parameters   : deviceIP - IP address of the device under test(Gateway box).
	#		 devicePort - Port Number of the device under test(Gateway box). 
        # Return Value : Returns string which holds MAC address of connected devices.

	try:
        	port = devicePort
        	tcpClient = socket.socket()
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'getConnectedDevices'}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		tcpClient.setblocking(0)
		recvStatus = select.select([tcpClient], [], [], 3) #Setting timeout for response(3 Sec)
		result = tcpClient.recv(1048) #Receiving response


		resultIndex = result.find("result") + len("result"+"\":\"")

                message = result[resultIndex:]
                message = message[:(message.find("\""))]
                print message

	except socket.error:
		print "AGENT_NOT_FOUND" 
