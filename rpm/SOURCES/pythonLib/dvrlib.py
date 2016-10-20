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
File        : dvrlib.py
Description : Library, which provides a wrapper for DVR related test scripts.
Version     : 1.0
Author      : Anoop Ravi, Sujeesh Lal
Date        : 10/07/2013
"""


#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import json

#------------------------------------------------------------------------------
# module class
#------------------------------------------------------------------------------
class DVRDetails:
	
	"""Class to hold DVR details

    	Syntax       : OBJ = DVRDetails(logPath) 
    	Description  : This class stores the information of DVR test case.
	"""
	
    	#------------------------------------------------------------------------------
    	# __init__ and __del__ block
    	#------------------------------------------------------------------------------

	def __init__(self, _logPath):
		try:
			self.fileData = []
			self.url = ""
			self.duration = ""
			self.logPath = _logPath
		except:
			print "An Error occured"
		else:
			return 

	def __del__(self):
		return
		
	#------------------------------------------------------------------------------
    	# Public methods
    	#------------------------------------------------------------------------------
	
	def find_between(self, line, first, last):

	# return the string between two tokens.

    	# Syntax       : OBJ.find_between()
    	# Description  : return the string between first and last.
  	# Return Value : string

		try:
			start = line.index(first) + len(first)
			end = line.index(last, start)
			return line[start:end]

		except ValueError:
			return ""			
		
	########## End of Function ##########
	
	def getURLList(self):

	# returns the list of URLs.

    	# Syntax       : OBJ.getURLList()
    	# Description  : return the  list of DVR URLs after parsing the urllist file.
  	# Return Value : list of DVR URLs

		filedata = []
		urllist = []
		f = open(self.logPath, 'r')
		for line in f:
   			splitline = line.rstrip('\r\n').split('<code>')
				
			if len(splitline) > 1:
          			filedata.append(splitline [1])

		for url in range(len(filedata)):
			filedata[url] = filedata[url].strip("DTCP/IP URL :")
			filedata[url] = filedata[url].strip("</code><br />")
 
		return filedata			
		
	########## End of Function ##########
	
	def getURL(self, recordingId):

	# Returns DVR URL of the corresponding recording id .

    	# Syntax       : OBJ.getURL(recordingId)
    	# Description  : return DVR URL of the recording id.
  	# Return Value : url
			
		line = self.getLine(recordingId )
		splitline = line.split('<code>')
    		if len(splitline) > 1:
          		newline = splitline [1]

		return newline			
		
	########## End of Function ##########

	def getDuration(self, recordingId):

	# Returns the duration of corresponding recording id .

    	# Syntax       : OBJ.getURL(recordingId)
    	# Description  : return duration of the recording id.
  	# Return Value : duration

		line = self.getLine(recordingId)
		duration = self.find_between(line, "Duration :", "<br")
		return duration 			
		
	########## End of Function ##########

	def getLine(self, recordingId):

	# Return the recorder id of corresponding stream.

    	# Syntax       : OBJ.getLine()
    	# Description  : return the line having the given recording id.
  	# Return Value : string

		fh = open(self.logPath, "r")
 		result = [i for i in fh if recordingId in i]
		line = "\n".join(result)
		return line			
		
	########## End of Function ##########

########## End of Class ##########


	
	
