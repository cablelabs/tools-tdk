#
# ============================================================================
# COMCAST CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of Comcast.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of Comcast.
# ===========================================================================
# Copyright (c) 2014 Comcast. All rights reserved.
# ============================================================================
#
#!/bin/bash
INPUT="recordedlist.txt"
#INPUT=$1
while read line
do
if [[ "$line" =~ ['#'] ]]
    then
    echo -n $line
    else
    echo  $line 
fi
done <$INPUT
