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
#!/usr/bin/
ocapId="$1"
echo "OCAP ID: $ocapId"
telnet localhost 3773 << EOF
t2p:msg selectService
{ "selectService" : { "locator" : "$ocapId" } }
t2p:msg
echo "Done"
