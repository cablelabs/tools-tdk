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


#export LOG_PATH=/opt/logs/
cd /opt/logs
if [ -d "$1" ]
 then
    echo "file $1 found"
    rm -rf $1
  else
    echo "folder  not found"
fi
if [ -f "$1.tgz" ]
  then
    echo "file $1.tgz found"
    rm $1.tgz
  else
    echo "file $1.tgz not found"
fi

#rm -rf $LOG_PATH/$1
