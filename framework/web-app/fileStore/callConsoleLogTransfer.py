
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
from consoleLogTransfer import consoleLogTransfer

if((len(sys.argv))!=6):
	print "Usage : python " + sys.argv[0] + " DeviceIP AgentMonitorPortNumber LogTransferPortNumber FileName LocalFilePath"
	print "eg    : python " + sys.argv[0] + " 192.168.160.130 8090 69 \"2885410322886_AgentConsole.log\" \"/filestore/logs/\""

else:
	deviceIP = sys.argv[1]
	agentPort = (int)(sys.argv[2])
	logTransferPort = (int)(sys.argv[3])
	fileName = sys.argv[4]
	localFilePath = sys.argv[5]
	consoleLogTransfer(deviceIP,agentPort,logTransferPort,fileName,localFilePath)
	
	
