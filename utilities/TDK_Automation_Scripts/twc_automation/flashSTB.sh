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
spawn telnet [lindex $argv 0]
expect "'^]'."
send "rm -f /mnt/data/*.bin\r"
send "cd /mnt/data\r"
send "tftp -g -r [lindex $argv 1]/[lindex $argv 2] [lindex $argv 3]\r"
sleep 10
expect $PROMPT
send "exit\r"
expect eof
