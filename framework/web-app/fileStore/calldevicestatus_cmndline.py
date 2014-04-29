#============================================================================
#COMCAST CONFIDENTIAL AND PROPRIETARY
#============================================================================
#This file and its contents are the intellectual property of Comcast.  It may
#not be used, copied, distributed or otherwise  disclosed in whole or in part
#without the express written permission of Comcast.
#============================================================================
#Copyright (c) 2013 Comcast. All rights reserved.
#============================================================================


# Module imports
import sys
import signal
from devicestatus import getStatus

# To enable time out
class NotFoundException(Exception):
    pass
    
def timeout(signum, frame):
    raise NotFoundException
		
# Check the number of arguments and print the syntax if args not equal to 5
if ( (len(sys.argv)) != 5):
        print "Usage : python " + sys.argv[0] + " Device_IP_Address PortNumber Test_Manager_IP_Address Box_Name"
        print "eg    : python " + sys.argv[0] + " 192.168.160.130 8088 192.168.160.248 \"TVM_XG1\""
        exit()

# Assigning Box IP address, port number, Test manager IP address and Box Name
boxipaddress = sys.argv[1]
port = int (sys.argv[2])
testmanageripaddress = sys.argv[3]
boxname = sys.argv[4]
	
	
#SIGALRM is only usable on a unix platform
signal.signal(signal.SIGALRM, timeout)

#change 4 to however many seconds you need
signal.alarm(4)

try:
    status = getStatus(boxipaddress,testmanageripaddress,boxname,port)  # Calling getStatus to get box status
    print status
except NotFoundException:
    print "NOT_FOUND"
