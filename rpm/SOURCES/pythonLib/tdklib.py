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
#
"""
File        : tdklib.py
Description : Library, which provides a wrapper for tdk testcase script.
Version     : 1.0
Author      : Anoop Ravi, Gilda Baby, Sujeesh Lal      
Date        : 10/07/2013                
"""

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import socket
import urllib
import json
import streamlib
import dvrlib
import tftpy
import time
import os
from time import gmtime, strftime
from sys import exit

#------------------------------------------------------------------------------
# module class
#------------------------------------------------------------------------------

class PrimitiveTestCase:
	"""
	Class to hold a TestCase in TDK

    	Syntax       : OBJ = PrimitiveTestCase([testCaseName=]) 

    	Description  : This class stores the information about a testcase.
	"""	
    	#------------------------------------------------------------------------------
    	# __init__ and __del__ block
    	#------------------------------------------------------------------------------
	def __init__(self, name, _url, id, execResId, _ip, _realpath, _tcpClient, _logTransferPort):
		try:
			self.url = _url
			self.execID = id
			self.ip = _ip
			self.resultId = execResId
			self.realpath = _realpath
			self.tcpClient = _tcpClient
			self.testCaseName = name
			self.logTransferPort = _logTransferPort
			self.result = None
			self.streamID = None
			self.resultStatus = None
			self.expectedResult = None
			temp = self.url + "/primitiveTest/getJson?testName=&idVal=2"
			data = temp.split("&")
			url = data[0] + name + "&" + data[1]
			self.jsonMsgValue = urllib.urlopen(url).read() 
		except:
			print "An Error occured"
		else:
			return 

	def __del__(self):
		return

    	#------------------------------------------------------------------------------
    	# Public methods
    	#------------------------------------------------------------------------------

	def addParameter(self, paramName, paramValue):

	# Updates the JSON Message with new parameter values.

    	# Syntax       : OBJ.addParameter(paramName, paramValue)
    	# Description  : Checks for the paramName in JSON string 
        #                Replaces the value of paramName with paramValue
        # Parameters   : paramName  - The parameter whose value is to be replaced.
	#                paramValue - New value for the parameter
  	# Return Value : None 

		try:
			data = json.loads(self.jsonMsgValue)
		except:
			print "ERROR : Json Message is in Incorrect Format !!!"
			exit()
	
		self.replaceValueInJson(data, paramName, paramValue)
		jsonAscii = json.dumps(data, ensure_ascii = False) 
		self.jsonMsgValue = jsonAscii
		return

	########## End of Function ##########
	
	def replaceValueInJson(self, orgJson, searchKey, replaceValue):

	# Replaces the JSON Message with new values.

	# Description  : Search for the key in JSON string
	#                Replaces the value of corresponding key with new Value
	# Parameters   : orgJson      - Json message
        #                searchKey    - The key whose value to be replaced
	#                replaceValue - value to be replaced
	# Return Value : None

		flag = 0
		for key in orgJson.keys():
		  	if key.strip() == searchKey.strip():
		  		orgJson[key] = replaceValue
				flag = 1
		
		if (flag == 0):
			print "ERROR : Parameter (" + searchKey + ") not found in primitive test !!!"
			exit()
	
	    	return

	########## End of Function ##########

	def executeTestCase(self, expectedResult):

    	# Send the JSON Message to Server over TCP

    	# Syntax       : OBJ.executeTestCase()
    	# Description  : Send the JSON Message to Server over TCP
	#	         Receives the result of the execution send by the Server 
    	# Parameters   : expectedResult - Expected result for that particular test
  	# Return Value : None 

		print "Executing %s...." %self.testCaseName
		self.tcpClient.send(self.jsonMsgValue)
		self.result = self.tcpClient.recv(1024)
		self.expectedResult = expectedResult
		return

	########## End of Function ##########

	def getResult(self):

    	# Displays the result

    	# Syntax       : OBJ.getResult()
    	# Description  : Shows the result SUCCESS/FAILURE
    	# Parameters   : None
	# Return Value : Result of the test execution 
    	
		message = "[SCRIPTSTATUSRESULT]" + self.getValueFromJSON("result")
		return message

	########## End of Function ##########

	def setResultStatus(self, status):

	# Displays the result

        # Syntax       : OBJ.setResultStatus()
        # Description  : Shows the result status(SUCCESS/FAILURE)
        # Parameters   : status of the test 
        # Return Value : None

		try:
			self.resultStatus = status
			temp = self.url + "/execution/saveResultDetails?execId=&resultData=&execResult=&expectedResult=&resultStatus=&testCaseName=&"  
			data = temp.split("&")
			url = data[0] + str(self.execID) + "&" + data[1] + self.result + "&" + data[2] + str(self.resultId) + "&" + data[3] + str(self.expectedResult) + "&" + data[4] + str(self.resultStatus) + "&" + data[5] + str(self.testCaseName)
			loadstring = urllib.urlopen(url).read()
		except:
			print "ERROR : Unable to access url to save result details !!!" 
		return
		
	########## End of Function ##########
	
	def getResultDetails(self):
    	
	# Displays the result

    	# Syntax       : OBJ.getResultDetails()
    	# Description  : Shows the details of the result
    	# Parameters   : None
	# Return Value : Details of the test execution 
    	
		message = self.getValueFromJSON("details")
		return message

	########## End of Function ##########

	def getValue(self,key):
    	
	# Displays the value of given key

    	# Syntax       : OBJ.getValue(key)
    	# Description  : Shows the value of given key
    	# Parameters   : key to find value
	# Return Value : Value of given key
    	
		message = self.getValueFromJSON(key)
		return message

	########## End of Function ##########

	def getLogPath(self):

    	# Displays the result

    	# Syntax       : OBJ.getLogPath()
    	# Description  : Shows the path of log
    	# Parameters   : None
	# Return Value : Result path  of the result
 
		message = self.getValueFromJSON("log-path")# message
		return message

	########## End of Function ##########
   
	def getValueFromJSON(self, key):

 	# Displays the result

        # Syntax       : OBJ.getValueFromJSON(key)
        # Description  : Parse the string of corresponding key and fetch the value
        # Parameters   : key to find value
        # Return Value : value of the key

		resultIndex = self.result.find(key) + len(key+"\":\"")
		message = self.result[resultIndex:]
		message = message[:(message.find("\""))]
		return message
	
	########## End of Function ##########
 
	def downloadFile(self, IP, PORT, RemoteFile, LocalFile):
	
 	# Download a file

        # Syntax       : OBJ.downloadFile()
        # Description  : To download a file 
        # Parameters   : IP         - IP address of the remote machine where the file resides
	#                PORT       - Port using for download
        #                RemoteFile - Remote file location
        #                LocalFile  - Local file location where the file to be downloaded.
        # Return Value : returns status
            
        	status = 0
        	try:
                	client = tftpy.TftpClient(IP, PORT)
                	client.download(RemoteFile, LocalFile)
                	status = 1

       		except TypeError:
                	print "Connection Error!!! Transfer of " + RemoteFile + " Failed.."
        	except:
                	print "Error!!! Transfer of " + RemoteFile + " Failed.." 
        	return status

	########## End of Function ##########

    	def transferLogs(self, LogPath, MultiLog):
	
 	# For transfering logs using tftp

        # Syntax       : OBJ.transferLogs()
        # Description  : To transfer log files 
        # Parameters   : logpath  - Path of logfile in remote machine
        #                multilog - 'true' for multiple logs,'false' for single log
        # Return Value : none
            
        	IP = self.ip
        	PORT = self.logTransferPort
		LOCALLOGPATH = self.realpath + "logs/" + str(self.execID) + "/"
		TimeStamp = strftime("%d%m%y%H%M%S", gmtime())
                if not os.path.exists(LOCALLOGPATH):
                        os.makedirs(LOCALLOGPATH)

    	#
    	#  If there are multiple logs, logdetails file will be downloaded first. All the application logs
    	#  will be downloaded after getting the log path from logdetails file. All the application logs
    	#  are saved with application name and timestamp(GMT).
    	#

        	if( MultiLog == "true"):
			SummaryFile = LOCALLOGPATH + str(self.execID) + "_" + "TestSummary" + "_" + TimeStamp
          		self.downloadFile(IP, PORT, LogPath, SummaryFile)
            		logdetails = open(SummaryFile, "r")
            		logdetails.readline()
            		line = logdetails.readline()
            		while(line != ''):
                                time.sleep(1)
                		path = line.split(";")[-1]
                		path = path.replace('"', '').strip()
                		path = path.strip("\n")
				LocalFileName = path.split("/")[-1]
				LocalFileName = LOCALLOGPATH + str(self.execID) + "_" + LocalFileName + "_" + TimeStamp
                		self.downloadFile(IP, PORT, path, LocalFileName)
                		line = logdetails.readline()
                	logdetails.close()

    	#
    	#  If there is only single log, that file will be downloaded from the logpath and timestamp(GMT)
   	#  will be appended in the filename.
    	#

        	elif( MultiLog == "false"):
            		LocalFileName = LogPath.split("/")[-1]
			LocalFileName = LOCALLOGPATH + str(self.execID) + "_" + LocalFileName + "_" + TimeStamp
            		self.downloadFile(IP, PORT, LogPath, LocalFileName)
		return

	########## End of Function ##########

	def getDVRDetails(self, logFileName):

	# Create an object for DVR details 

    	# Syntax      : OBJ.getDVRDetails()
    	# Description : Create an object of DVR Details 
    	# Parameters  : logFileName - path to file name having the DVR details
	# Return Value: An instance of DVR Details
		
		IP = self.ip
        	PORT = self.logTransferPort
		RECORDED_URL_LOG_PATH = logFileName

		LOCALLOGPATH = self.realpath + "fileStore/" 
		LOCAL_PATH = LOCALLOGPATH + str(self.execID) + "_RecordedUrlsLog.txt"
		if self.downloadFile(IP, PORT, RECORDED_URL_LOG_PATH, LOCAL_PATH) == 0:
			print "[ERROR : ] UNABLE TO TRANSFER FILE "
			dvrObj = NULL
		else:
    			dvrObj = dvrlib.DVRDetails(LOCAL_PATH)

		return dvrObj
			
	########## End of Function ##########

	def getStreamDetails(self, streamId):

	# Create an object for Streaming details 

    	# Syntax      : OBJ.getStreamDetails(streamId)
   	# Description : Create an object of StreamingDetails 
    	# Parameters  : streamId - Id of the stream you want to use
	# Return Value: An instance of StreamingDetails
	
		self.streamID = streamId
		url = self.url + "/primitiveTest/getStreamDetails?idVal=" + str(streamId) + "&stbIp=" + self.ip
		try:
			loadstring = urllib.urlopen(url).read() 
			testObj = streamlib.StreamingDetails(loadstring)
		except:
			print "ERROR : Unable to access url for getting stream details !!!"

		return testObj 
			
	########## End of Function ##########
	
########## End of Class  ##########
		

#------------------------------------------------------------------------------
# module class
#------------------------------------------------------------------------------

class TDKScriptingLibrary:

	"""
	Class to act as a wrapper for the testcase script in TDK

	Description  : This class configures and gives an instance of a testcase 
	Syntax       : OBJ = TDKScriptingLibrary( componentName, version) 
        Parameters   : componentName   - Component Name
                       version         - RDK version
	"""	

    	#------------------------------------------------------------------------------
    	# __init__ and __del__ block
    	#------------------------------------------------------------------------------	

	def __init__(self, cName, version):
		self.serviceIp = None
		self.servicePort = None
		self.componentName = cName
		self.rdkversion = version
		self.url = None
		self.execID = None
		self.resultId = None
		self.result = None
		self.IP = None
		self.realpath = None
		self.tcpClient = None
		return 

	def __del__(self):
		return

    	#------------------------------------------------------------------------------
    	# Public methods
    	#------------------------------------------------------------------------------
		
	def configureTestCase(self, _url,path, id, execResId, deviceIp, devicePort, _logTransferPort, executionName):

    	# Configures the testcase for Execution

    	# Syntax       : OBJ.configureTestCase(url, path, id, resultId, ipAddress, portValue, executionName)
	#                obj.configureTestCase('http://192.168.161.200:8080/rdk-scripttest-m3',
        #                            '/opt/comcast/software/tomcat/current/webapps/rdk-scripttest-m3/',3333,29,ip,port,'E2E_DVRTrickPlay_01');
    	# Description  : Obtain the device ip and port number,
	#                Create a TCP connection to the device under Test
    	# Parameters   : url           - url to fetch webservice calls
	#		 path	       - Path to save the files tranferred from the box
	#		 id            - Execution id
	#		 resultId      - Result id
        #                ipAddress     - Device Ip.
	#                portValue     - Device Port
  	# 	         executionName - Test Execution Name
	# Return Value : None 
  	# Exceptions   : IOError      - File doesnot exist
	#                socket.error - Error while opening socket
    	
		try:
			self.url = _url
			self.execID = id
			self.resultId = execResId
			self.tcpClient = socket.socket()
			self.IP = deviceIp
			portValue = devicePort
			self.realpath = path
			self.logTransferPort = _logTransferPort
			self.tcpClient.connect((self.IP, portValue))
		
			#For DynamicLoading ....
			#Load the particular shared object  before executing
			print "Connected to "+ self.IP +" Box for testing "+ self.componentName
                	
			final = {'jsonrpc':'2.0','id':'2','method':'LoadModule','param1':self.componentName,'version':self.rdkversion}
			query = json.dumps(final)
			self.tcpClient.send(query)
			
		except socket.error:
			print "************************\nError while Connecting to Server ...Please ensure the Box "+ self.IP +" is up and Test Agent is running...\n************************\n"
		except IOError:
			print "ERROR : Configuration File Not Found!\n"
		except:
			print "ERROR : Unable to connect.. Please check box is up and agent is running.....\n"
		else:
			print "Connected to Server!\n"
			self.result = self.tcpClient.recv(1048)

		return

	########## End of Function ##########

	def getLoadModuleResult(self):

    	# Displays the result

	# Syntax       : OBJ.showResult()
    	# Description  : Shows the result
    	# Parameters   : None
  	# Return Value : Result of the test execution 
    	
		if self.result:
			resultIndex = self.result.find("result") + len("result\":\"")
			message = self.result[resultIndex:]
			message = message[:(message.find("\""))]
			return message
		else:
			return "Error in socket.. Please check STB is up and agent is running inside it"
			
	########## End of Function ##########

	def createTestStep(self, testcaseName):

    	# Create an object for testcase 

    	# Syntax      : OBJ.createTestStep(testcaseName)
    	# Description : Create an object of testcase 
    	# Parameters  : testcaseName - Name of test case
	# Return Value: An instance of PrimitiveTestCase 
    	
		testObj = PrimitiveTestCase(testcaseName, self.url, self.execID, self.resultId, self.IP, self.realpath, self.tcpClient, self.logTransferPort)
		return testObj
 
	########## End of Function ##########

	def unloadModule(self, cName):

    	# Unload the component test module

    	# Syntax       : OBJ.unloadModule(cName)
	# Description  : Unload module
    	# Parameters   : cName - Component name
	# Return Value : null
    		
		try:
			final = {'jsonrpc':'2.0','id':'2','method':'UnloadModule','param1':cName,'version':self.rdkversion}
			query = json.dumps(final)
			self.tcpClient.send(query)
		except:
			print "ERROR : exception in Unload module!\n"
		else:
			print "Unload module Success\n"
		return 

	########## End of Function ##########
	
########## End of Class  ##########

