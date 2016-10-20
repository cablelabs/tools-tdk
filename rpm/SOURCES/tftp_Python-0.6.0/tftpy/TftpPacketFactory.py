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
"""This module implements the TftpPacketFactory class, which can take a binary
buffer, and return the appropriate TftpPacket object to represent it, via the
parse() method."""

from TftpShared import *
from TftpPacketTypes import *

class TftpPacketFactory(object):
    """This class generates TftpPacket objects. It is responsible for parsing
    raw buffers off of the wire and returning objects representing them, via
    the parse() method."""
    def __init__(self):
        self.classes = {
            1: TftpPacketRRQ,
            2: TftpPacketWRQ,
            3: TftpPacketDAT,
            4: TftpPacketACK,
            5: TftpPacketERR,
            6: TftpPacketOACK
            }

    def parse(self, buffer):
        """This method is used to parse an existing datagram into its
        corresponding TftpPacket object. The buffer is the raw bytes off of
        the network."""
        log.debug("parsing a %d byte packet" % len(buffer))
        (opcode,) = struct.unpack("!H", buffer[:2])
        log.debug("opcode is %d" % opcode)
        packet = self.__create(opcode)
        packet.buffer = buffer
        return packet.decode()

    def __create(self, opcode):
        """This method returns the appropriate class object corresponding to
        the passed opcode."""
        tftpassert(self.classes.has_key(opcode),
                   "Unsupported opcode: %d" % opcode)

        packet = self.classes[opcode]()

        return packet
