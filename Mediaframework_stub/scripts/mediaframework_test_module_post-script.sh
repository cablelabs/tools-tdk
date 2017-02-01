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

RMFCONFIG_PATH=/etc
TARGET_PATH=/opt
LOGPATH=$TDK_PATH/logs
LOGFILE=Mediaframework_testmodule_postreq_details.log
#Create if log file not there
mkdir -p $LOGPATH

#removing old configuring status from the opt
rm $LOGPATH/$LOGFILE

#removing the rmfconfig.ini file from /opt/
if rm $TARGET_PATH/rmfconfig.ini; then
   echo "rmfconfig.ini removed from "$TARGET_PATH
else
   echo "Cant able to remove rmfconfig.ini"
   touch $LOGPATH/$LOGFILE
   echo "FAILURE<details>Not able to delete rmfconfig.ini" > $LOGPATH/$LOGFILE
   exit 1
fi

#Restart the rmfstreamer,vodclient,podmanager & snmp
process_name="rmf-streamer vod-service pod-service snmp-manager-service"
for process in $process_name
do
	/etc/init.d/$process restart
	if [ $? -eq 0 ]
	then
		echo $process "restarted"
		touch $LOGPATH/$LOGFILE;
		echo "SUCCESS" > $LOGPATH/$LOGFILE
	else
		echo $process "not able to restart"
		touch $LOGPATH/$LOGFILE;
		echo "FAILURE<details>Not able to restart" > $LOGPATH/$LOGFILE
		
	fi
done
