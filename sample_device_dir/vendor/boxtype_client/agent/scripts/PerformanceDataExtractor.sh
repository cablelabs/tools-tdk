#!/bin/sh
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

export PATH=$PATH:/usr/local/bin:/usr/local/lib:/usr/local/lib/sa

cd $TDK_PATH

rm cpu.log memused.log

while read line
do

    sed -e '0,/Average:        CPU/d' -e '/Average:         eth1/,$d' sysStatAvg.log > performance.temp

    cat performance.temp | awk 'BEGIN { RS="" ; FS="\n" } { print $2 }' | awk '{print $8}' >> cpu.log

    cat performance.temp  | awk 'BEGIN { RS="" ; FS="\n" } { print $8 }' | awk '{print$2,$3,$4}' >> memused.log

    sed -e '1,25d' < sysStatAvg.log > temp

    mv temp sysStatAvg.log

done < sysStatAvg.log

echo "Performance data Extracted"
