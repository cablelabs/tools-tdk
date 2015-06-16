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

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

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
                serverIp = get_ip_address('eth0')
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
                print "Query cmd: ",cmd
                sys.stdout.flush()
                byteStr = subprocess.check_output(cmd, shell=True)
                outdata = unicode(byteStr, errors='ignore')
                #outdata = subprocess.check_output(cmd, shell=True)
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
                serverIp = get_ip_address('eth0')
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
                print "Query cmd: ",cmd
                sys.stdout.flush()
                byteStr = subprocess.check_output(cmd, shell=True)
                outdata = unicode(byteStr, errors='ignore')
                #outdata = subprocess.check_output(cmd, shell=True)
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
                serverIp = get_ip_address('eth0')
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
                print "Executing cmd: ",cmd
                sys.stdout.flush()
                byteStr = subprocess.check_output(cmd, shell=True)
                outdata = unicode(byteStr, errors='ignore')
                #outdata = subprocess.check_output(cmd, shell=True)
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


def callScheduleHandler(methodName,params,gwIp):

        # To invoke and fetch status of updateSchedule REST API in the simulator for a particular box

        # Parameters   : methodName, params, gwIp
        # methodName   : REST API name. e.g., updateSchedule, updateInlineSchedule.
        #                updateSchedule : To send updateSchedule query to box
        #                updateInlineSchedule : To send updateSchedule as inline message to box
        # gwIp         : IP address of gateway box
        # Return Value : Console output of the curl command

        try:
                serverIp = get_ip_address('eth0')
        except:
                print "#TDK_@error-ERROR : Unable to fetch recorder server IP"
		outdata = "ERROR : Unable to fetch recorder server IP"
                sys.stdout.flush()
		return outdata

        # Constructing Query Command
        cmd = 'curl '+'-g '+'\''+'http://'+serverIp+':8080/DVRSimulator/'+methodName+'?boxIp='+gwIp+'&'+params+'\''

        class Timout(Exception):
                pass

        def timeoutHandler(signum, frame):
                raise Timout

        signal.signal(signal.SIGALRM, timeoutHandler)
        signal.alarm(20)

        # Executing request command
        try:
                print "Query cmd: ",cmd
                sys.stdout.flush()
                byteStr = subprocess.check_output(cmd, shell=True)
                outdata = unicode(byteStr, errors='ignore')
                #outdata = subprocess.check_output(cmd, shell=True)
                signal.alarm(0)  # reset the alarm
        except Timout:
                print "#TDK_@error-ERROR : Timeout!! Taking too long"
		outdata = "ERROR : Timeout!! Taking too long"
                sys.stdout.flush()
		return outdata
        except:
                print "#TDK_@error-ERROR : Unable to execute curl command"
		outdata = "ERROR: Unable to execute query command"
                sys.stdout.flush()
		return outdata

        return outdata

########## End of Function callScheduleHandler ##########

def getGenerationId(jsonData):
        ret = "NOID"
        try:
                #jsonList = json.loads(unicode(jsonData, errors='ignore'), strict=False)
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
                return my_item['generationId']

        print "ERROR: StatusMessage not found!"
        return ret

########## End of Function getGenerationId ##########

def getStatusMessage(jsonData):
        ret = "NOSTATUS"
        try:
		#jsonList = json.loads(unicode(jsonData, errors='ignore'), strict=False)
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
                return my_item['statusMessage']

        print "ERROR: StatusMessage not found!"
        return ret

########## End of Function getStatusMessage ##########

def getTimeFromStatus(jsonData):
        ret = 0
        try:
                #jsonList = json.loads(unicode(jsonData, errors='ignore'), strict=False)
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
                #jsonList = json.loads(unicode(jsonData, errors='ignore'), strict=False)
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
                #jsonList = json.loads(unicode(jsonData, errors='ignore'), strict=False)
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
		#jsonList = json.loads(unicode(jsonData, errors='ignore'), strict=False)
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
                                        print "Found Recording with recordingId %s: "%recordingId
                                        return (recordings['recordingStatus']['recordings'][i])

        print "ERROR: Recording not found!"
        return ret

########## End of Function getRecordingFromRecId ##########

def getValueFromKeyInRecording(recording,key):
        value = "BADVALUE"
        try:
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
