#!/bin/bash
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
#This file will align the list of urls as one entry per line

grep . "${1}" | while read line
do
if [ "${line#*"#"}" != "$line" ]
    then
    echo -n $line
    else
    echo  $line
fi
done
