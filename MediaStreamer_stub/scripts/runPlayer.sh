#!/bin/bash
# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================

export LD_LIBRARY_PATH=/mnt/nfs/bin/gstreamer_plugins/:/mnt/nfs/bin/rstreamer/lib:/lib:$LD_LIBRARY_PATH
export GST_PLUGIN_PATH=/lib/gstreamer-0.10:/usr/local/lib/gstreamer-0.10:/mnt/nfs/bin/gstreamer_plugins/

#To delete the content in ocapri_log.txt file
>$4

echo "Inside player script"
chmod 777 player
./player $1 $2

#To copy the ocapri_log to Mediastreamer log file
cp $4 $3

