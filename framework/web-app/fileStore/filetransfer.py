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

# Module Imports
import tftpy
import sys

# Check the number of arguments and print the syntax if args not equal to 5
if ( (len(sys.argv)) != 5):
        print "Usage : python " + sys.argv[0] + " Device_IP_Address PortNumber Remote_File_Path Local_file_path"
	print "eg    : python " + sys.argv[0] + " 192.168.160.130 8088 \"/version.txt\" \"/filestore/version/version.txt\""
	exit()

# Assigning IP address, port number and path of source and destination files
ipaddrs = sys.argv[1]
port = int (sys.argv[2])
remotefile = sys.argv[3]
localfile = sys.argv[4]

# Connect to TFTP server and download the file
try:
	client = tftpy.TftpClient (ipaddrs, port)
	client.download (remotefile, localfile)
       
except TypeError:
      	print "Connection Error!!! Transfer of " + remotefile + " Failed: Make sure Agent is running"

except:
      	print "Error!!! Transfer of " + remotefile + " Failed.."

# End of File
