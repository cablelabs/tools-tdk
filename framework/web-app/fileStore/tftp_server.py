
#============================================================================
#COMCAST CONFIDENTIAL AND PROPRIETARY
#============================================================================
#This file and its contents are the intellectual property of Comcast.  It may
#not be used, copied, distributed or otherwise  disclosed in whole or in part
#without the express written permission of Comcast.
#============================================================================
#Copyright (c) 2014 Comcast. All rights reserved.
#============================================================================

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import tftpy
import socket
import sys

# Check the number of arguments and print the syntax if args not equal to 3
if ( (len(sys.argv)) != 3):
        print "Usage : python " + sys.argv[0] + " port DestinationDirectory"
        print "eg    : python " + sys.argv[0] + " 69 \"/home/anoop/tftpserver/\""
        sys.exit()

# Assigning IP address, port number and destination path
logpath = sys.argv[2]
tmIP = '0.0.0.0'
port = int (sys.argv[1])

# Starting TFTP server
try:
	print "Server listening"
	server = tftpy.TftpServer(logpath)
	server.listen(tmIP, port)

except KeyboardInterrupt:
	print "Stopping server"

# End of file
