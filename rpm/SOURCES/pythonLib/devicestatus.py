#!/usr/bin/python
"""
File        : devicestatus.py
Description : To get status of device
Version     : 1.0
Author      : ANOOP RAVI
Date        : 19/07/2013
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

def getStatus(deviceIP,managerIP,boxName,statusPort):

        # Syntax       : devicestatus.getStatus( deviceIP, managerIP, boxName, statusPort)
        # Description  : Sends a json query and decides the status of device from the json response.
        # Parameters   : deviceIP - IP address of the device whose status to be checked.
		#				 managerIP - IP address of test manager.
		#				 boxName - Box friendly name.
		#				 statusPort - port used for status checking.
        # Return Value : Returns string which holds status of device.

	try:
        	port = statusPort
        	tcpClient = socket.socket()
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'getHostStatus','managerIP':managerIP,'boxName':boxName}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		tcpClient.setblocking(0)
		recvStatus = select.select([tcpClient], [], [], 5) #Setting timeout for response(3 Sec)
		if recvStatus[0]:
	       		result = tcpClient.recv(1048) #Receiving response
			if "Free" in result:
        			return "FREE"
			if "Busy" in result:
        			return "BUSY"

		else:
			return "HANG"

	except socket.error:
		return "NOT_FOUND"
