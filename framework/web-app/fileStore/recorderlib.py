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
import os
import sys
import time
import signal
import subprocess

import socket
import fcntl
import struct
import json
import tdklib
from random import randint
from time import sleep

def startRecorderApp(realpath,arg):

	# To start recorder application

	# Syntax       : OBJ.startRecorderApp(realpath)
	# Description  : start recorder application and redirect the console output back to script
	# Parameters   : path of "filestore"
	# Return Value : console output of the app

		argument = str(arg)
		inputfile = realpath + "/fileStore/recorderfiles/schedule_one.json"
		classpath = realpath + "/fileStore/recorderfiles/"
		appname = "TDK_Recorder_Server"

		try:
    			outFile = open(inputfile,'w')
    			outFile.write(argument)
			outFile.flush()
    			outFile.close()
		except IOError as (errno,strerror):
    			print "#TDK_@error-ERROR : I/O error({0}): {1}".format(errno, strerror)
			sys.stdout.flush()
			sys.exit()
		except:
			print "#TDK_@error-ERROR : Unable to open " + inputfile + " file"
			sys.stdout.flush()
			sys.exit()

		# Constructing Command
		cmd = "java" + " " + "-classpath" + " " + classpath + " " + appname
		cmd = cmd + " " + inputfile

		class Timout(Exception):
    			pass

		def timeoutHandler(signum, frame):
    			raise Timout

		signal.signal(signal.SIGALRM, timeoutHandler)
		signal.alarm(8*60)  # 8 minutes

		# Executing Recorder App
		try:
			print "Going to start App..."
			sys.stdout.flush()
			outdata = subprocess.check_output(cmd, shell=True)
    			signal.alarm(0)  # reset the alarm
		except Timout:
    			print "#TDK_@error-ERROR : Timeout!! Taking too long"
			print "Details : ", outdata
			sys.stdout.flush()
			sys.exit()
		except:
			print "#TDK_@error-ERROR : Unable to initiate App"
			sys.stdout.flush()
			sys.exit()
		
		os.remove(inputfile)

		return outdata
	
########## End of Function startRecorderApp ##########

LOIPADDR = '127.0.0.1'

def callServerHandler(methodName,gwIp):

        # To invoke and fetch status of REST API in the simulator for a particular box

        # Parameters   : methodName, gwIp
        # methodName   : REST API name. e.g., clearStatus, retrieveStatus, clearDeviceStatus, retrieveDeviceStatus etc.,
        #                clearStatus  : To clear the status message held by the simulator from a particular box
        #                retrieveStatus : To retrieve the status message held by the simulator from a particular box
        #                clearDeviceStatus : To clear device status messages held by the simulator from a particular box
        #                retrieveDeviceStatus : To retrieve Device status messages held by the simulator from a particular box
        # gwIp         : IP address of gateway box
        # Return Value : Console output of the curl command

        try:
                serverIp = LOIPADDR
	
        except:
                print "#TDK_@error-ERROR : Unable to fetch recorder server IP"
		outdata = "ERROR: Unable to fetch recorder server IP"
                sys.stdout.flush()
		return outdata

        # Constructing Query Command
        cmd = 'curl ' + '-g ' + '\'' + 'http://' + serverIp + ':8080/DVRSimulator/' + methodName + '?boxIp=' + gwIp + '\''

        class Timout(Exception):
                pass

        def timeoutHandler(signum, frame):
                raise Timout

        signal.signal(signal.SIGALRM, timeoutHandler)
        signal.alarm(20)

        # Executing request command
        try:
                print "Executing \"",cmd," \""
                sys.stdout.flush()
                byteStr = subprocess.check_output(cmd, shell=True)
                outdata = unicode(byteStr, errors='ignore')
                signal.alarm(0)  # reset the alarm
        except Timout:
                print "#TDK_@error-ERROR : Timeout!! Taking too long"
		outdata = "ERROR: Timeout!! Taking too long"
                sys.stdout.flush()
		return outdata
        except:
                print "#TDK_@error-ERROR : Unable to execute curl command"
		outdata = "ERROR: Unable to execute curl command"
                sys.stdout.flush()
		return outdata

        return outdata

########## End of Function callServerHandler ##########

def callServerHandlerWithMsg(methodName,jsonMsg,gwIp):

        # To invoke and fetch status of user provided JSON message passed as argument to REST API in the simulator for a particular box

        # Parameters   : methodName, jsonMsg, gwIp
        # methodName   : REST API name. e.g., updateMessage, updateInlineMessage.
        #                updateMessage  : To send user provided JSON message to box
        #                updateInlineMessage : To send user provided JSON message to box
        # gwIp         : IP address of gateway box
        # Return Value : Console output of the curl command

        try:
                serverIp = LOIPADDR
        except:
                print "#TDK_@error-ERROR : Unable to fetch recorder server IP"
		outdata = "ERROR: Unable to fetch recorder server IP"
                sys.stdout.flush()
                return outdata

        # Constructing Query Command
        cmd = 'curl '+'-g '+'\''+'http://'+serverIp+':8080/DVRSimulator/'+methodName+'?boxIp='+gwIp+'&jsonMessage='+jsonMsg+'\''

        class Timout(Exception):
                pass

        def timeoutHandler(signum, frame):
                raise Timout

        signal.signal(signal.SIGALRM, timeoutHandler)
        signal.alarm(20)

        # Executing request command
        try:
		print "Executing \"",cmd," \""
                sys.stdout.flush()
                byteStr = subprocess.check_output(cmd, shell=True)
                outdata = unicode(byteStr, errors='ignore')
                signal.alarm(0)  # reset the alarm
        except Timout:
                print "#TDK_@error-ERROR : Timeout!! Taking too long"
		outdata = "ERROR: Timeout!! Taking too long"
                sys.stdout.flush()
		return outdata
        except:
                print "#TDK_@error-ERROR : Unable to execute curl command"
		outdata = "ERROR: Unable to execute query command"
                sys.stdout.flush()
		return outdata

	print "Server response: ",outdata
        return outdata

########## End of Function callServerHandlerWithMsg ##########

def callServerHandlerWithType(methodName,type,gwIp):

        # To enable/disable Longpoll and RWS server in the simulator for a particular box

        # Parameters   : methodName, type, gwIp
        # methodName   : REST API name. e.g., disableServer, enableServer
        #                isEnabledServer  : To check the server status for an STB
        #                enableServer : To enable the server for STB
        #                disableServer : To disable the server for a particular STB (This will not affect the server communication for other STB)
        #                retrieveDisabledStatus : To retrieve the recorder communication with disabled server
        #                clearDisabledStatus : To clear the recorder communication with disabled server
        # type         : RWSServer, RWSStatus, LPServer
        # gwIp         : IP address of gateway box
        # Return Value : Console output of the curl command

        try:
                serverIp = LOIPADDR
        except:
                print "#TDK_@error-ERROR : Unable to fetch recorder server IP"
                outdata = "ERROR: Unable to fetch recorder server IP"
                sys.stdout.flush()
                return outdata

        # Constructing Query Command
        cmd = 'curl '+'-g '+'\''+'http://'+serverIp+':8080/DVRSimulator/'+methodName+'?boxIp='+gwIp+'&serverType='+type+'\''

        class Timout(Exception):
                pass

        def timeoutHandler(signum, frame):
                raise Timout

        signal.signal(signal.SIGALRM, timeoutHandler)
        signal.alarm(20)

        # Executing request command
        try:
		print "Executing \"",cmd," \""
                sys.stdout.flush()
                byteStr = subprocess.check_output(cmd, shell=True)
                outdata = unicode(byteStr, errors='ignore')
                signal.alarm(0)  # reset the alarm
        except Timout:
                print "#TDK_@error-ERROR : Timeout!! Taking too long"
                outdata = "ERROR: Timeout!! Taking too long"
                sys.stdout.flush()
                return outdata
        except:
                print "#TDK_@error-ERROR : Unable to execute curl command"
                outdata = "ERROR: Unable to execute query command"
                sys.stdout.flush()
                return outdata

        return outdata

########## End of Function callServerHandlerWithType ##########


def getGenerationId(jsonData):
        ret = "NOID"
        try:
		jsonList = json.loads(jsonData, strict=False)
        except ValueError, e:
                print e
                return ret
        except:
                print "Unexpected error:", sys.exc_info()[0]
                return ret

        #Check if status is not empty
        if jsonList == []:
                print "ERROR: No status available"
                return ret

        #Get dictionary content inside list status
        for my_item in jsonList:
		if 'generationId' in my_item:
                	return my_item['generationId']

        print "ERROR: generationId not found!"
        return ret

########## End of Function getGenerationId ##########

def readGenerationId(gwIp):

        ret = "NOID"

        #Get recordings list
        callServerHandler('clearStatus',gwIp)
        callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',gwIp)
        print "Wait for 60sec to get the recording list"
        sleep(60)
        recResponse = callServerHandler('retrieveStatus',gwIp)
	print "Rec List: ",recResponse

        try:
                jsonList = json.loads(recResponse, strict=False)
        except ValueError, e:
                print e
                return ret
        except:
                print "Unexpected error:", sys.exc_info()[0]
                return ret

        #Check if response is not empty
        if jsonList == []:
                print "ERROR: No response available"
                return ret

        #Get dictionary content inside list status
        for my_item in jsonList:
                if 'generationId' in my_item:
			print "generationId = ",my_item['generationId']
                        return my_item['generationId']

        print "ERROR: generationId not found in response!"
        return ret

########## End of Function readGenerationId ##########

def getStatusMessage(jsonData):
        ret = "NOSTATUS"
        try:
		jsonList = json.loads(jsonData, strict=False)
        except ValueError, e:
                print e
                return ret
        except:
                print "Unexpected error:", sys.exc_info()[0]
                return ret
	
        #Check if status is not empty
        if jsonList == []:
                print "ERROR: No status available"
                return ret

        #Get statusMessage from status list
        for my_item in jsonList:
                if 'recordingStatus' in my_item['statusMessage']:
                        return my_item['statusMessage']

        print "ERROR: StatusMessage not found!"
        return ret

########## End of Function getStatusMessage ##########

def getTimeFromStatus(jsonData):
        ret = 0
        try:
                jsonList = json.loads(jsonData, strict=False)
        except ValueError, e:
                print e
                return ret
        except:
                print "Unexpected error:", sys.exc_info()[0]
                return ret

        #Check if status is not empty
        if jsonList == []:
                print "ERROR: No status available"
                return ret

        #Get dictionary content inside list status
        for my_item in jsonList:
                try:
			time = my_item['time']
			print "Time = ",time
                        return int(time)
        	except KeyError, e:
                	print "Invalid key %s" % str(e)

        print "ERROR: time info not found!"
        return ret

########## End of Function getTimeFromStatus ##########

def getTimeStampFromStatus(jsonData):
        ret = 0
        try:
                jsonList = json.loads(jsonData, strict=False)
        except ValueError, e:
                print e
                return ret
        except:
                print "Unexpected error:", sys.exc_info()[0]
                return ret

        #Check if status is not empty
        if jsonList == []:
                print "ERROR: No status available"
                return ret

        #Get dictionary content inside list status
        for my_item in jsonList:
                try:
			if 'recordingStatus' in my_item['statusMessage']:
				status = my_item['statusMessage']
                        	timestamp = status ['recordingStatus'] ["timestamp"]
                        	print "TimeStamp = ",timestamp
                        	return int(timestamp)
                except KeyError, e:
                        print "Invalid key %s" % str(e)

        print "ERROR: timestamp info not found!"
        return ret

########## End of Function getTimeStampFromStatus ##########

def getTimeStampListFromStatus(jsonData):
        ret = []
        try:
                jsonList = json.loads(jsonData, strict=False)
        except ValueError, e:
                print e
                return ret
        except:
                print "Unexpected error:", sys.exc_info()[0]
                return ret

        #Check if status is not empty
        if jsonList == []:
                print "ERROR: No status available"
                return ret

        #Get dictionary content inside list status
        for my_item in jsonList:
                try:
                        if 'recordingStatus' in my_item['statusMessage']:
                                status = my_item['statusMessage']
                                timestamp = status ['recordingStatus'] ["timestamp"]
                                print "TimeStamp = ",timestamp
                                ret.append(int(timestamp))
                except KeyError, e:
                        print "Invalid key %s" % str(e)

        return ret

########## End of Function getTimeStampListFromStatus ##########

def getTimeListFromStatus(jsonData):
	ret = []
        try:
                jsonList = json.loads(jsonData, strict=False)
        except ValueError, e:
                print e
                return ret
        except:
                print "Unexpected error:", sys.exc_info()[0]
                return ret

        #Check if status is not empty
        if jsonList == []:
                print "ERROR: No status available"
                return ret

        #Get dictionary content inside list status
        for my_item in jsonList:
                try:
                        time = my_item['time']
			ret.append(int(time))
                except KeyError, e:
                        print "Invalid key %s" % str(e)

        return ret

########## End of Function getTimeListFromStatus ##########

def getRecordingFromRecId(jsonData,recordingId):
        ret = "NOTFOUND"
        try:
		jsonList = json.loads(jsonData, strict=False)
        except ValueError, e:
                print e
                return ret
        except:
                print "Unexpected error:", sys.exc_info()[0]
                return ret

        #Check if status is not empty
        if jsonList == []:
                print "ERROR: No status available"
                return ret

	#Get statusMessage from status list
	for my_item in jsonList:
		recordings = {}
		if 'recordingStatus' in my_item['statusMessage']:
                        recordings = my_item['statusMessage']
                        for i in range(0, len(recordings['recordingStatus']['recordings'])):
                                if (str(recordings['recordingStatus']['recordings'][i]['recordingId'])) == str(recordingId):
                                        #print "Found Recording with recordingId ",recordingId
                                        return (recordings['recordingStatus']['recordings'][i])

        print "RecordingID ", recordingId, " not found in status message!"
        return ret

########## End of Function getRecordingFromRecId ##########

def getValueFromKeyInRecording(recording,key):
        value = "BADVALUE"

        try:
                if "NOTFOUND" == recording:
                        print "No recording data found"
                        return value

                if key in ['volume','start','duration','playbackLocator']:
			#Extract dictionary from content list value
			content = {}
			if 'content' in recording:
				for line in recording['content']:
					content.update(line)
				print "Recording content value: ",content
                        	value = content[key]
			else:
				print "Recording missing content value"
                else:
                        value = recording[key]
        except KeyError, e:
                print "key %s not found in recording" % str(e)

        return value

########## End of Function getValueFromKeyInRecording ##########

def getRecordings(jsonData):
        recordings = []
        try:
                jsonList = json.loads(jsonData, strict=False)
        except ValueError, e:
                print e
                return recordings
        except:
                print "Unexpected error:", sys.exc_info()[0]
                return recordings

        #Check if status is not empty
        if jsonList == []:
                print "ERROR: No status available"
                return recordings

        #Get statusMessage from status list
        for my_item in jsonList:
                if 'recordingStatus' in my_item['statusMessage']:
                        recordings = my_item['statusMessage']['recordingStatus']['recordings']
                else:
                        print "Could not find recordingStatus in json message"

        return recordings

########## End of Function getRecordings ##########

#numOfTuners = no of tuners on STB
#recDuration = recording duration in millisec
#priority = priority of recording to be created
def checkDiskFullWithRecordings(gwIp,tdkTestObj,numOfTuners,recDuration,priority):

	print "Enter Disk Full..."
	print "tuners: ",numOfTuners," recording duration: ",recDuration," priority: ",priority
        diskFull = 0
        inProgress = 0

        #Start hot recording on all the tuners
        for n in range(0,numOfTuners):
                requestID = str(randint(10, 500))
                recordingID = str(randint(10000, 500000))
                startTime = "0"
                duration = str(recDuration)
                streamId = '0'+str(n+1)
                ocapId = tdkTestObj.getStreamDetails(streamId).getOCAPID()
                now = "curTime"

                #Frame json message to schedule recording
                jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"RecordingTitle_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\""+priority+"\"}]}}"

                #Send update msg to simulator server
                callServerHandler('clearStatus',gwIp)
                callServerHandlerWithMsg('updateMessage',jsonMsg,gwIp)
                #Wait to send next request
                sleep(30)
                #Get recordings list and check for error code of scheduled recording
                callServerHandler('clearStatus',gwIp)
                callServerHandlerWithMsg('updateMessage','{\"getRecordings\":{}}',gwIp)
                #Wait to get response from recorder
                sleep(120)
                recResponse = callServerHandler('retrieveStatus',gwIp)
                #Look for recordings field in response
                recordings = getRecordings(recResponse)
                if [] == recordings:
                        print "No recordings found in response: ",recResponse
                else:
			print "recordings found in response: ",recResponse

                        recordingData = getRecordingFromRecId(recResponse,recordingID)
                        print "Recording Details: ",recordingData
                        if "NOTFOUND" == recordingData:
                                print "Recording ",recordingID," not found in recording list: ",recResponse
				#TODO: Remove later
				#RDKTT-404 (only failed recordings shown so may be recording actually started)
				print "Assuming recording ",recordingID," scheduled successfully"
				inProgress = 1
                        else:
                                status = getValueFromKeyInRecording(recordingData,'status')
				error = getValueFromKeyInRecording(recordingData,'error')
				if "BADVALUE" == error:
					print "No error in scheduled recording"
					if "PENDING" == status.upper():
						print "Recording ",recordingID," in pending state"
						print "Not waiting for recording to complete"
					else:
						print "Recording ",recordingID," scheduled successfully"
						inProgress = 1
				else:
					print "Failed to record due to error: ",error,"status: ",status
					if "SPACE_FULL" == error:
						print "DiskFull!! Could not schedule recording ",recordingID
						diskFull = 1
						break
        #hot recording on all the tuners - End

        if 1 == inProgress:
                print "Started ",priority," recordings of duration ",recDuration
                print "Wait for recordings to complete"
		#sleep(150)
		sleep(numOfTuners*150)
                sleep(recDuration/1000)
        else:
                print "No ",priority," recordings started of duration ",recDuration

	print "Exit Disk Full..."

        return diskFull

############  checkDiskFullWithRecordings End ###########################

def getRecordingFromField(jsonData,field,value):
        ret = "NOTFOUND"
        try:
                jsonList = json.loads(jsonData, strict=False)
        except ValueError, e:
                print e
                return ret
        except:
                print "Unexpected error:", sys.exc_info()[0]
                return ret

        #Check if status is not empty
        if jsonList == []:
                print "ERROR: No status available"
                return ret

        #Get statusMessage from status list
        for my_item in jsonList:
                recordings = {}
                if 'recordingStatus' in my_item['statusMessage']:
                        recordings = my_item['statusMessage']
                        for i in range(0, len(recordings['recordingStatus']['recordings'])):
				if field in (str(recordings['recordingStatus']['recordings'][i])):
                                	if (str(recordings['recordingStatus']['recordings'][i][field])) == str(value):
                                        	print "Found Recording with value ",value
                                        	return (recordings['recordingStatus']['recordings'][i])

        print "Expected field not found in status message!"
        return ret

########## End of Function getRecordingFromField ##########

#Input  	reqRecording = ["recordingId","duration","deletePriority"]
#               recording is the output of getRecordingFromRecId containing following fields:
		#recordingId      [String] is a unique recording identifier.
		#status           [String] is the state of the recording.
		#error            [String] (optional) is the error code.
		#deletePriority   [String]
		#expectedStart    [long] is the expected start time of the recording in UTC milliseconds.
		#expectedDuration [long] is the recording length in milliseconds.
		#estimatedSize    [long] is the estimated size of the recording in bytes.
		#size             [long] is the size of the recording in bytes.
		#start            [long] is the recording start time, specified in UTC milliseconds since epoch.
		#duration         [long] is the recording duration, specified in milliseconds.
		#volume           [String] is the unique id of the media volume where the content is stored.
		#playbackLocator  [String]

def verifyCompletedRecording(recording,reqRecording):

        MAX_DEVIATION_THRESHOLD = 30000

        ret = "TRUE"

        try:
                if 'recordingId' not in recording:
                        print "Invalid recording ",recording
                        return "FALSE"
                recordingId = recording['recordingId']
                deletePriority = recording["deletePriority"]
                status = recording['status']
                expectedStart = recording["expectedStart"]
                expectedDuration = recording["expectedDuration"]
                estimatedSize = recording["estimatedSize"]
                size = recording["size"]

                #Check if recordingId,duration and deletePriority is set as expected
                if str(recordingId) != str(reqRecording["recordingId"]):
                        print "recordingId ",recordingId," not matching value set ",reqRecording["recordingId"]
                        ret = "FALSE"
                elif expectedDuration != reqRecording['duration']:
                        print "expectedDuration ",expectedDuration," not matching value set ",reqRecording['duration']
                        ret = "FALSE"
                elif deletePriority != reqRecording["deletePriority"]:
                        print "deletePriority ",deletePriority," not matching value set ",reqRecording["deletePriority"]
                        ret = "FALSE"
                #Check if status is complete
                elif "Complete" != status:
                        print "Recording is not in complete state ",status
                        ret = "FALSE"
                #Check there is no error status
                elif 'error' in recording:
                        print "Error found in recording ",recording['error']
                        ret = "FALSE"
                #Check if size,expectedStart,expectedDuration,estimatedSize is valid
                elif 0 >= size:
                        print "Recording size not valid ",size
                        ret = "FALSE"
                elif 0 >= expectedStart:
                        print "Recording expectedStart not valid ",expectedStart
                        ret = "FALSE"
                elif 0 >= estimatedSize:
                        print "Recording estimatedSize not valid ",estimatedSize
                        ret = "FALSE"
                elif 0 >= expectedDuration:
                        print "Recording expectedDuration not valid ",expectedDuration
                        ret = "FALSE"
                #Check if content field is present and is not empty
                elif 'content' in recording:
                        if [] == recording['content']:
                                print "Recording has empty content field ",recording['content']
                                ret = "FALSE"
                        else:
                                #Multiple segments recordings are not expected
                                #Extract content as dictionary from content as list of dictionaries
                                content = {}
                                for contentDict in recording['content']:
                                        content.update(contentDict)
                                        #print "content: ",content

                                start = content['start']
                                duration = content['duration']
                                volume = content['volume']
                                playbackLocator = content['playbackLocator']

                                #Check if start,duration is valid
                                if 0 >= start:
                                        print "Recording actual start time is not valid ",start
                                        ret = "FALSE"
                                elif 0 >= duration:
                                        print "Recording actual duration is not valid ",duration
                                        ret = "FALSE"
                                #Check if volume,playbackLocator is valid
                                elif "" == volume:
                                        print "Recording media volume location is null"
                                        ret = "FALSE"
                                elif "" == playbackLocator:
                                        print "Recording playbackLocator is null"
                                        ret = "FALSE"
                                #Check value of volume
                                elif "/opt" not in volume:
                                        print "Recording media volume location is not /opt"
                                        ret = "FALSE"
                                #Check playbackLocator value contains recordingId
                                elif str(recordingId) not in playbackLocator:
                                        print "Recording playbackLocator does not contain recordingId ",playbackLocator
                                        ret = "FALSE"
                                #Check actual start and expected start time values
                                elif expectedStart > start:
                                        print "Recording expected start time is greater than actual start time ",expectedStart,start
                                        ret = "FALSE"
                                #Check that actualStart and requestedStart is not more than max deviation threshold (30sec)
                                elif start - expectedStart > MAX_DEVIATION_THRESHOLD:
                                        print "Recording actualStart and requestedStart is more than max deviation threshold"
                                        ret = "FALSE"
                                #Check that difference between actual duration and requested duration is not more than max deviation threshold (30sec)
                                elif abs (expectedDuration - duration) > MAX_DEVIATION_THRESHOLD:
                                        print "Difference between actual duration and requested duration in millisec ",abs (expectedDuration - duration)
                                        ret = "FALSE"
                                else:
                                        print "No issues found in content field"
                else:
                        print "Recording missing content field"
                        ret = "FALSE"
        except KeyError, e:
                print "key %s not found in recording" % str(e)
                ret = "FALSE"

        return ret

########## End of Function verifyCompletedRecording ##########
