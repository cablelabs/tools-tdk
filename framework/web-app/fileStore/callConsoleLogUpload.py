
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
from consoleLogUpload import consoleLogUpload

if((len(sys.argv))!=6):
	print "Usage : python " + sys.argv[0] + " DeviceIP AgentMonitorPortNumber BoxFileName TMFileName logUploadURL"
	print "eg    : python " + sys.argv[0] + " 192.168.160.189 8090 \"AgentConsole.log\" \"111_222_333_AgentConsole.log\" http://192.168.160.101:8080/rdk-test-tool/"

else:
	deviceIP = sys.argv[1]
	agentMonitorPort = (int)(sys.argv[2])
	boxFileName = sys.argv[3]
	tmFileName = sys.argv[4]
	logUploadURL = sys.argv[5]
	consoleLogUpload(deviceIP,agentMonitorPort,boxFileName,tmFileName,logUploadURL)
