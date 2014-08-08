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
# this script sets the runtime environment variables, play the url and copy the ocapri log to mediastreamer log file

export LD_LIBRARY_PATH=/mnt/nfs/bin/gstreamer_plugins/:/mnt/nfs/bin/rstreamer/lib:/lib:$LD_LIBRARY_PATH
export GST_PLUGIN_PATH=/lib/gstreamer-0.10:/usr/local/lib/gstreamer-0.10:/mnt/nfs/bin/gstreamer_plugins/

#To delete the content in ocapri_log.txt file
>$4

echo "Inside player script"
chmod 777 player
./player $1 $2

#To copy the ocapri_log to Mediastreamer log file
cp $4 $3

