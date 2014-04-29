
#============================================================================
#COMCAST CONFIDENTIAL AND PROPRIETARY
#============================================================================
#This file and its contents are the intellectual property of Comcast.  It may
#not be used, copied, distributed or otherwise  disclosed in whole or in part
#without the express written permission of Comcast.
#============================================================================
#Copyright (c) 2013 Comcast. All rights reserved.
#============================================================================


from setRoute import setRoute
import sys

if((len(sys.argv))!=8):
        print "Usage : python " + sys.argv[0] + " DeviceIP PortNumber ClientMACaddress ClientExecutionPort ClientStatusPort clientLogTransferPort clientAgentMonitorPort"
        print "eg    : python " + sys.argv[0] + " 192.168.160.130 8088 b4:f2:e8:de:1b:0e 9000 9001 9002 9003"

else:
	deviceIP = sys.argv[1]
	devicePort = (int)(sys.argv[2])
	clientMAC = sys.argv[3]
	clientAgentPort = (sys.argv[4])
	clientStatusPort = (sys.argv[5])
	clientLogTransferPort = (sys.argv[6])
	clientAgentMonitorPort = (sys.argv[7])

	setRoute(deviceIP,devicePort,clientMAC,clientAgentPort,clientStatusPort,clientLogTransferPort,clientAgentMonitorPort)

