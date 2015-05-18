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
	#	         disableLPServer : To disable the LP server for a particular STB (This will not affect the LP server communication for other STB)
	#                enableLPServer : To enable the LP server for STB
	#                isEnabledLPServer : To check the LP server status of an STB
	#                retrieveLPRedirectStatus : To retrieve the LP redirect status
	#                clearLPRedirectStatus : To clear the LP redirect status	 
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
        #Extract dictionary from list content value
        content = {}
        for line in recording['content']:
                content.update(line)
        try:
                if key in ['volume','start','duration','playbackLocator']:
                        value = content[key]
                else:
                        value = recording[key]
        except KeyError, e:
                print "Invalid key %s" % str(e)

        return value

########## End of Function getValueFromKeyInRecording ##########
