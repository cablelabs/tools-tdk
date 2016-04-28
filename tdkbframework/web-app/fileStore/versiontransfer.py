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
import tftpy
import sys

IP = <ipaddress>
PORT = <port> 
RemoteFile = "/version.txt"
LocalFile = <localfile>

try:
	client = tftpy.TftpClient( IP, PORT )
	client.download( RemoteFile, LocalFile )
       
except TypeError:
       	print "Connection Error!!! Transfer of " + RemoteFile + " Failed: Make sure Agent is running"

except:
       	print "Error!!! Transfer of " + RemoteFile + " Failed.."
 

