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
File        : streamlib.py
Description : Library, which provides a wrapper for getting stream details.
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
class StreamingDetails:
	
	"""Class to hold Streaming details

    	Syntax       : OBJ = StreamingDetails(url) 
    	Parameters   : url - 
    	Description  : This class stores the information of Stream.
	"""	

    	#------------------------------------------------------------------------------
    	# __init__ and __del__ block
    	#------------------------------------------------------------------------------

	def __init__(self, _url):
		try:
			self.url = _url
			self.data = json.loads(self.url)
		except :
			print "An Error occured"
		else:
			return 

	def __del__(self):
		return
		
	#------------------------------------------------------------------------------
    	# Public methods
    	#------------------------------------------------------------------------------

	def getGatewayIp(self):

    	# Returns the Gateway IP of corresponding stream.

    	# Syntax       : OBJ.getGatewayIp()
    	# Description  : returns the Gateway IP of corresponding stream
  	# Return Value : gateway IP 

		#self.data = json.loads(self.url)
		gateway = self.data['gatewayip']
		return gateway
		
	########## End of Function ##########
   
	def getChannelType(self):

	# Returns the Channel Type  of corresponding stream.

    	# Syntax       : OBJ.getChannelType()
    	# Description  : returns the Channel Type of corresponding stream.
  	# Return Value : Channel Type 

		channeltype = self.data['channeltype']
		return channeltype
		
	########## End of Function ##########
	
	def getOCAPID(self):

	# Returns the ocap id  of corresponding stream.

    	# Syntax       : OBJ.getOCAPID()
    	# Description  : return the ocap id of corresponding stream.
  	# Return Value : ocap id 

		ocapid = self.data['ocapid']
		return ocapid
		
	########## End of Function ##########
	
	def getRecorderID(self):

	# Returns the recorder id of corresponding stream.

    	# Syntax       : OBJ.getRecorderID()
    	# Description  : return the recorder id of corresponding stream.
  	# Return Value : recorder id 

		recorderid = self.data['recorderid']
		return recorderid
		
	########## End of Function ##########
	
	def getAudioFormat(self):

	# Returns the audio format of corresponding stream.

    	# Syntax       : OBJ.getAudioFormat()
    	# Description  : returns the audioformat of corresponding stream.
  	# Return Value : audioformat

		audioformat = self.data['audioformat']
		return audioformat
		
	########## End of Function ##########
	
	def getVideoFormat(self):

	# Returns the video format of corresponding stream.

    	# Syntax       : OBJ.getVideoFormat()
    	# Description  : returns the videoformat of corresponding stream.
  	# Return Value : videoformat

		videoformat = self.data['videoformat']
		return videoformat
		
	########## End of Function ##########

########## End of Class ##########
