#
# ============================================================================
# COMCAST C O N F I D E N T I A L AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of Comcast.  It may
# not be used, copied, distributed or otherwise  disclosed in whole or in part
# without the express written permission of Comcast.
# ============================================================================
# Copyright (c) 2013 Comcast. All rights reserved.
# ============================================================================
#
from getDevices import getConnectedDevices
import sys

if((len(sys.argv))!=3):
        print "Usage : python " + sys.argv[0] + " Device IP PortNumber"
	print "eg    : python " + sys.argv[0] + " 192.168.160.130 8088"

else:
       deviceIP = sys.argv[1]
       devicePort = (int)(sys.argv[2])

       getConnectedDevices(deviceIP,devicePort)
#print "eg    : python " + sys.argv[0] + " 192.168.160.130 8088"
