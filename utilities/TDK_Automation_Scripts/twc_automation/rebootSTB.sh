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
