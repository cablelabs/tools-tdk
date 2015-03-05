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


echo "Stopping TDK Agent.."

sleep 1

#Killing inactive TDK processes
#Make sure "ps" will list all process. In some platform it is "ps -ef". Make changes accordingly in below commands.
ps | grep "agent" | grep -v "grep" | grep -v "syssnmpagent" | awk '{print $1}' | xargs kill -9 >& /dev/null
ps | grep "tftp" | grep -v "grep" | awk '{print $1}' | xargs kill -9 >& /dev/null
ps | grep "/opt/TDK/" | grep -v "grep" | awk '{print $1}' | xargs kill -9 >& /dev/null
sleep 2

echo "Done"
