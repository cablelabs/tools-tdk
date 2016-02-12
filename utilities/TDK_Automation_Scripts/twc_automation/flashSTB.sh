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
