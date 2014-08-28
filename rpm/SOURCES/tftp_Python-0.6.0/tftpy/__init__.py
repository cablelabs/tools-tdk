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
"""
This library implements the tftp protocol, based on rfc 1350.
http://www.faqs.org/rfcs/rfc1350.html
At the moment it implements only a client class, but will include a server,
with support for variable block sizes.

As a client of tftpy, this is the only module that you should need to import
directly. The TftpClient and TftpServer classes can be reached through it.
"""

import sys

# Make sure that this is at least Python 2.3
verlist = sys.version_info
if not verlist[0] >= 2 or not verlist[1] >= 3:
    raise AssertionError, "Requires at least Python 2.3"

from TftpShared import *
from TftpPacketTypes import *
from TftpPacketFactory import *
from TftpClient import *
from TftpServer import *
from TftpContexts import *
from TftpStates import *
