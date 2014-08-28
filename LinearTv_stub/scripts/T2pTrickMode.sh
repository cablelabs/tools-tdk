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
trickPlayRate="$1"
echo "Trick Play rate: $trickPlayRate"
telnet localhost 3773 << EOF
t2p:msg trickModeRequest
{ "trickModeRequest" : { "rate" : $trickPlayRate } }
t2p:msg
echo "Done"
