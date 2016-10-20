#!/usr/bin/env python
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

import sys, logging, os
from optparse import OptionParser
import tftpy

def main():
    usage=""
    parser = OptionParser(usage=usage)
    parser.add_option('-H',
                      '--host',
                      action='store',
                      dest='host',
                      help='remote host or ip address')
    parser.add_option('-p',
                      '--port',
                      action='store',
                      dest='port',
                      help='remote port to use (default: 69)',
                      default=69)
    parser.add_option('-f',
                      '--filename',
                      action='store',
                      dest='filename',
                      help='filename to fetch')
    parser.add_option('-b',
                      '--blocksize',
                      action='store',
                      dest='blocksize',
                      help='udp packet size to use (default: 512)',
                      default=512)
    parser.add_option('-o',
                      '--output',
                      action='store',
                      dest='output',
                      help='output file (default: same as requested filename)')
    parser.add_option('-d',
                      '--debug',
                      action='store_true',
                      dest='debug',
                      default=False,
                      help='upgrade logging from info to debug')
    parser.add_option('-q',
                      '--quiet',
                      action='store_true',
                      dest='quiet',
                      default=False,
                      help="downgrade logging from info to warning")
    options, args = parser.parse_args()
    if not options.host or not options.filename:
        sys.stderr.write("Both the --host and --filename options "
                         "are required.\n")
        parser.print_help()
        sys.exit(1)

    if options.debug and options.quiet:
        sys.stderr.write("The --debug and --quiet options are "
                         "mutually exclusive.\n")
        parser.print_help()
        sys.exit(1)

    if not options.output:
        options.output = os.path.basename(options.filename)

    class Progress(object):
        def __init__(self, out):
            self.progress = 0
            self.out = out
        def progresshook(self, pkt):
            self.progress += len(pkt.data)
            self.out("Downloaded %d bytes" % self.progress)

    if options.debug:
        tftpy.setLogLevel(logging.DEBUG)
    elif options.quiet:
        tftpy.setLogLevel(logging.WARNING)
    else:
        tftpy.setLogLevel(logging.INFO)

    progresshook = Progress(tftpy.logger.info).progresshook

    tftp_options = {}
    if options.blocksize:
        tftp_options['blksize'] = int(options.blocksize)

    tclient = tftpy.TftpClient(options.host,
                               int(options.port),
                               tftp_options)

    tclient.download(options.filename,
                     options.output,
                     progresshook)

if __name__ == '__main__':
    main()
