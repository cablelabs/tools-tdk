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
import os
import sys
import time
import signal
import subprocess


def startRecorderApp(realpath,arg):

	# To start recorder application

	# Syntax       : OBJ.initiateApp(realpath)
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
		signal.alarm(3*60)  # 3 minutes

		# Executing Recorder App
		try:
			print "Going to start App..."
			sys.stdout.flush()
			outdata = subprocess.check_output(cmd, shell=True)
    			signal.alarm(0)  # reset the alarm
		except Timout:
    			print "#TDK_@error-ERROR : Timeout!! No Response Received by Recorder Server"
			sys.stdout.flush()
#			sys.exit()
		except:
			print "#TDK_@error-ERROR : Unable to initiate Recorder Server"
			sys.stdout.flush()
			sys.exit()
		
		os.remove(inputfile)

		return outdata
	
########## End of Function ##########
