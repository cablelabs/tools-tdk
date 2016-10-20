#!/bin/sh
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

