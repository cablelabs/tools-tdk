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
import sys

#------------------------------------------------------------------------------
# module class
#------------------------------------------------------------------------------
class RecordingDetails:
	
	"""Class to hold Recording details

    	Syntax       : OBJ = RecordingDetails(logPath) 
    	Description  : This class stores the information of Recordings.
	"""
	
    	#------------------------------------------------------------------------------
    	# __init__ and __del__ block
    	#------------------------------------------------------------------------------

	def __init__(self, logPath):
		try:
			self.fileData = []
			self.url = ""
			self.duration = ""
			self.logPath = logPath
		except:
			print "#TDK_@error-ERROR : Unable to fetch Recording details"
			sys.stdout.flush()
			sys.exit()
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
			print "#TDK_@error-ERROR : Unable to retrieve details. File not in specified format."
			sys.stdout.flush()
			sys.exit()
		
	########## End of Function ##########

	def getSegmentName(self, index):

	# Returns the segmentName of corresponding recording.

    	# Syntax       : OBJ.getSegmentName(index)
    	# Description  : return SegmentName of the recording.
  	# Return Value : SegmentName

		line = self.getLine(index)
                segmentName = int(line.split(": ")[-1])
		return segmentName

	########## End of Function ##########
	
	def getDuration(self, index):

	# Returns the duration of corresponding recording.

    	# Syntax       : OBJ.getDuration(index)
    	# Description  : return duration of the recording.
  	# Return Value : duration

		line = self.getLine(index)
                duration = self.find_between(line, "Duration: ", "SegmentName")
		return int(duration[:-1])

	########## End of Function ##########

        def getRecordingId(self, index):

        # Returns the recording id of corresponding recording.

        # Syntax       : OBJ.getRecordingId(index)
        # Description  : return recording id of the recording.
        # Return Value : recording id

                line = self.getLine(index)
                recordingid = self.find_between(line, "id: ", "title")
                return recordingid

        ########## End of Function ##########

        def getRecordingTitle(self, index):

        # Returns the duration of corresponding recording id .

        # Syntax       : OBJ.getRecordingTitle(index)
        # Description  : return title of the recording index.
        # Return Value : title

                line = self.getLine(index)
                title = self.find_between(line, "title: ", " Duration:")
                return title

        ########## End of Function ##########

        def getTotalRecordings(self):

        # Returns the duration of corresponding recording id .

        # Syntax       : OBJ.getTotalRecordings()
        # Description  : return the total number of recordings.
        # Return Value : total number of recordings

		try:
                	recordingdetails = open(self.logPath, "r")
                	line = recordingdetails.readline()
			recordings = int(line.split(":")[-1])
			recordingdetails.close()
                	return recordings

		except ValueError:
			print "#TDK_@error-ERROR : File not in specified format. Unable to fetch total number of recordings."
			sys.stdout.flush()
			sys.exit()
		
	########## End of Function ##########

	def getLine(self, index):

	# Return the details of corresponding index.

    	# Syntax       : OBJ.getLine(index)
    	# Description  : return the line having the given index.
  	# Return Value : string

		flag = 0
		recordingdetails = open(self.logPath, "r")
		token = "Record: " + str(index)
            	line = recordingdetails.readline()
            	line = recordingdetails.readline()
            	while(line != ''):
			if token in line:
				flag = 1
				break
            		line = recordingdetails.readline()

		recordingdetails.close()
		if (flag == 0):
			print "#TDK_@error-ERROR : Unable to find the given recording index. ( Index : " + str(index) + " )"
			sys.stdout.flush()
			sys.exit()
		return line

		
	########## End of Function ##########


########## End of Class ##########


########## End of recordinglib ##########
	
	
