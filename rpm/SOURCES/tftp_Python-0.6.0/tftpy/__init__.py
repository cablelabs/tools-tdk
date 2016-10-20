##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
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
