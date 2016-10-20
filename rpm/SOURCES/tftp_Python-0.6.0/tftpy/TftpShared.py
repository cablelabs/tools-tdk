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
"""This module holds all objects shared by all other modules in tftpy."""

import logging

LOG_LEVEL = logging.NOTSET
MIN_BLKSIZE = 8
DEF_BLKSIZE = 512
MAX_BLKSIZE = 65536
SOCK_TIMEOUT = 5
MAX_DUPS = 20
TIMEOUT_RETRIES = 5
DEF_TFTP_PORT = 69

# A hook for deliberately introducing delay in testing.
DELAY_BLOCK = 0

# Initialize the logger.
logging.basicConfig()
# The logger used by this library. Feel free to clobber it with your own, if you like, as
# long as it conforms to Python's logging.
log = logging.getLogger('tftpy')

def tftpassert(condition, msg):
    """This function is a simple utility that will check the condition
    passed for a false state. If it finds one, it throws a TftpException
    with the message passed. This just makes the code throughout cleaner
    by refactoring."""
    if not condition:
        raise TftpException, msg

def setLogLevel(level):
    """This function is a utility function for setting the internal log level.
    The log level defaults to logging.NOTSET, so unwanted output to stdout is
    not created."""
    global log
    log.setLevel(level)

class TftpErrors(object):
    """This class is a convenience for defining the common tftp error codes,
    and making them more readable in the code."""
    NotDefined = 0
    FileNotFound = 1
    AccessViolation = 2
    DiskFull = 3
    IllegalTftpOp = 4
    UnknownTID = 5
    FileAlreadyExists = 6
    NoSuchUser = 7
    FailedNegotiation = 8

class TftpException(Exception):
    """This class is the parent class of all exceptions regarding the handling
    of the TFTP protocol."""
    pass

class TftpTimeout(TftpException):
    """This class represents a timeout error waiting for a response from the
    other end."""
    pass
