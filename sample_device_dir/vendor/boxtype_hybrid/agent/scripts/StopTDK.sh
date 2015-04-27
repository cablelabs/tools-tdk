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
export TDK_PATH=/opt/TDK #Path where TDK libs and bins are installed

sleep 1

#Killing inactive TDK processes
#Make sure "ps" will list all process. In some platform it is "ps -ef". Make changes accordingly in below commands.
ps | grep "tdk_agent" | grep -v "grep" | grep -v "syssnmpagent" | awk '{print $1}' | xargs kill -9 >& /dev/null
ps | grep "tftp" | grep -v "grep" | awk '{print $1}' | xargs kill -9 >& /dev/null
ps | grep $TDK_PATH | grep -v "grep" | awk '{print $1}' | xargs kill -9 >& /dev/null
sleep 2

echo "Done"
