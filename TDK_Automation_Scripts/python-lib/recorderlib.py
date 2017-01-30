#
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
    			print "#TDK_@error-ERROR : Timeout!! Taking too long"
			sys.stdout.flush()
#			sys.exit()
		except:
			print "#TDK_@error-ERROR : Unable to initiate App"
			sys.stdout.flush()
			sys.exit()
		
		os.remove(inputfile)

		return outdata
	
########## End of Function ##########
