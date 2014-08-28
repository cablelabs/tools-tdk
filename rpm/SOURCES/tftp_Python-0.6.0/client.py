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
# Python TFTP Client using tftpy module 

import tftpy
IPAddr='127.0.0.1'
port=69
remoteFileName='test.txt'
localFileName='TestReceived.txt'
client = tftpy.TftpClient(IPAddr, port)
client.download(remoteFileName,localFileName)
