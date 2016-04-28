
#!/usr/bin/python

#============================================================================
#COMCAST CONFIDENTIAL AND PROPRIETARY
#============================================================================
#This file and its contents are the intellectual property of Comcast.  It may
#not be used, copied, distributed or otherwise  disclosed in whole or in part
#without the express written permission of Comcast.
#============================================================================
#Copyright (c) 2013 Comcast. All rights reserved.
#============================================================================

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import sys
from setTDKAvailablity import setTDKAvailablity

if((len(sys.argv))!=4):
	print "Invalid Arguments !!!"
	print "Usage : python " + sys.argv[0] + " DeviceIP PortNumber option(enable/disable)"
	print "eg    : python " + sys.argv[0] + " 192.168.161.40 8088 enable"

else:
	deviceIP = sys.argv[1]
	devicePort = (int)(sys.argv[2])
	option = sys.argv[3]
	retVal = setTDKAvailablity(deviceIP,devicePort,option)

