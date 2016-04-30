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
set prompt "#"
set CNTRLZ "\x1a"
set CNTRLSQUAREBRACKET "\x1d"
spawn telnet [lindex $argv 0]
expect "'^]'.\r"
send "cd /appfs/tdk_br1.3/bin/\r"
send "\r"
send "./StartTDK.sh\r"
sleep 10
send $CNTRLZ
send "\r"
send $CNTRLSQUAREBRACKET
send "\r"
expect "telnet>"
sleep 3
send "quit\r"
expect eof

