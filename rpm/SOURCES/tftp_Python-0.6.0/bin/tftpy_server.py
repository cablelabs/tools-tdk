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

import sys, logging
from optparse import OptionParser
import tftpy

def main():
    usage=""
    parser = OptionParser(usage=usage)
    parser.add_option('-i',
                      '--ip',
                      type='string',
                      help='ip address to bind to (default: INADDR_ANY)',
                      default="")
    parser.add_option('-p',
                      '--port',
                      type='int',
                      help='local port to use (default: 69)',
                      default=69)
    parser.add_option('-r',
                      '--root',
                      type='string',
                      help='path to serve from',
                      default=None)
    parser.add_option('-d',
                      '--debug',
                      action='store_true',
                      default=False,
                      help='upgrade logging from info to debug')
    options, args = parser.parse_args()

    if options.debug:
        tftpy.setLogLevel(logging.DEBUG)
    else:
        tftpy.setLogLevel(logging.INFO)

    if not options.root:
        parser.print_help()
        sys.exit(1)

    server = tftpy.TftpServer(options.root)
    try:
        server.listen(options.ip, options.port)
    except tftpy.TftpException, err:
        sys.stderr.write("%s\n" % str(err))
        sys.exit(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
