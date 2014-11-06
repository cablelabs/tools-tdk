
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
from resetAgent import resetAgent



if((len(sys.argv))!=4):
	print "Usage : python " + sys.argv[0] + " DeviceIP PortNumber ResetFlag"
	print "eg    : python " + sys.argv[0] + " 192.168.160.130 8090 true"

else:
	deviceIP = sys.argv[1]
	devicePort = (int)(sys.argv[2])
	resetFlag = sys.argv[3]
	resetAgent(deviceIP,devicePort,resetFlag)

