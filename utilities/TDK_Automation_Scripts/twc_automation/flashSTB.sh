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
