#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
#!/usr/bin/expect
set timeout -1
set PROMPT "#"
set REBOOT "reboot\r"
spawn telnet [lindex $argv 0]
expect "'^]'."
send "\r"
expect $PROMPT
send -- $REBOOT
sleep 10
send -- "^C"
