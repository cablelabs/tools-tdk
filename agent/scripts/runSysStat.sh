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

sar -r -u 1 1 | awk ' /Average:/ { print $0 }' >> sysStatAvg.log

echo "ITERATION" >> sysStatAvg.log
