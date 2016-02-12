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

