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


# Module imports
import sys
import signal
from getImageName import getImageName

# To enable time out
class NotFoundException(Exception):
    pass
    
def timeout(signum, frame):
    raise NotFoundException
		
# Check the number of arguments and print the syntax if args not equal to 5
if ( (len(sys.argv)) != 3):
        print "Usage : python " + sys.argv[0] + " Device_IP_Address PortNumber"
        print "eg    : python " + sys.argv[0] + " 192.168.160.130 8087"
        exit()

# Assigning Box IP address, port number
boxipaddress = sys.argv[1]
port = int (sys.argv[2])

#SIGALRM is only usable on a unix platform
signal.signal(signal.SIGALRM, timeout)

#change 15 to any other desired value
signal.alarm(5)

try:
    status = getImageName(boxipaddress, port)
    print status
except NotFoundException:
    print "NOT_FOUND"