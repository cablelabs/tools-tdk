
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
from getRDKVersion import getRDKVersion


if((len(sys.argv))!=3):
	print "Usage : python " + sys.argv[0] + " DeviceIP PortNumber"
	print "eg    : python " + sys.argv[0] + " 192.168.161.40 8090"

else:
	deviceIP = sys.argv[1]
	devicePort = (int)(sys.argv[2])
	getRDKVersion(deviceIP,devicePort)

