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
import sys
import json
import tftpy
import socket
import select

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def consoleLogTransfer(deviceIP,agentPort,logTransferPort,fileName,localFilePath):

        # Syntax       : consoleLogTransfer.consoleLogTransfer (deviceIP,agentPort,logTransferPort,fileName,localFilePath)
        # Description  : Sends a json query to get path to console log file and transfer the same.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 agentPort - Port Number of the device under test. 
	#		 logTransferPort - Port Number for log transfer using TFTP.
	#		 fileName - Name of log file.
	#		 localFilePath - Path to which the file is transferred.
        # Return Value : Nil

	# Sending JSON request to get log path
	try:
        	tcpClient = socket.socket()
        	tcpClient.connect((deviceIP, agentPort))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'GetAgentConsoleLogPath'}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()

		resultIndex = result.find("result") + len("result"+"\":\"")

                message = result[resultIndex:]
                message = message[:(message.find("\""))]
		sys.stdout.flush()

	except socket.error:
		print "ERROR: Unable to connect agent.." 
		sys.stdout.flush()
		sys.exit()

	# Transferring file using TFTP
	try:

		remoteFile = message + "/" + fileName
		localFile = localFilePath + "/" + fileName
		print localFile
		print remoteFile
		client = tftpy.TftpClient( deviceIP, logTransferPort )
		client.download( remoteFile, localFile, timeout=20 )
	except TypeError:
      		print "Connection Error!!! Transfer of " + remoteFile + " Failed: Make sure Agent is running"
		sys.exit()

	except:
      		print "Error!!! Transfer of " + remoteFile + " Failed.."
		sys.exit()

# End of File
