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
RMFCONFIG_PATH=/etc/
TARGET_PATH=/opt/
#removing old configuring status from the opt
rm $TDK_PATH/logs/Recorder_testmodule_prereq_details.log

touch /tmp/stage4
touch /tmp/stt_received

#Copying the rmfconfig.ini file in to /opt/
ls $TARGET_PATH/rmfconfig.ini
if [ $? == 0 ]; then
        echo "file present"
else
	if cp $RMFCONFIG_PATH/rmfconfig.ini $TARGET_PATH; then
	   echo "rmfconfig.ini is copied from " $RMFCONFIG_PATH
	else
	   echo "rmfconfig.ini is not copied from " $RMFCONFIG_PATH 1>&2
	   touch $TDK_PATH/logs/Recorder_testmodule_prereq_details.log;
	   echo "FAILURE<DETAILS>Unable to copy rmfconfig.ini" >> $TDK_PATH/logs/Recorder_testmodule_prereq_details.log
	   exit 1
	fi
fi

#Editing the rmf_config.ini to disbale the dtcp flag
rmf_flags="FEATURE.LONGPOLL.URL"
FLAG_SEARCH_STATUS=`grep $rmf_flags $TARGET_PATH/rmfconfig.ini|wc -l`
if [ $FLAG_SEARCH_STATUS -ne 0 ]
then
     echo $rmf_flags is found in rmfconfig.ini
     #Editing the flag to false
     IP=$(awk -F"@" '/Manager IP/{ip=$2}END{print ip}' $TDK_PATH/tdkconfig.ini )
     echo $IP
     sed -i -e "s#$rmf_flags=.*#$rmf_flags=http://$IP:8000/longpollServer#g" $TARGET_PATH/rmfconfig.ini
     if [ $? -eq 0 ]
     then
        echo "rmfconfig.ini file edited"
	touch $TDK_PATH/logs/Recorder_testmodule_prereq_details.log;
        echo  "SUCCESS" >> $TDK_PATH/logs/Recorder_testmodule_prereq_details.log
     else
        echo "sed utillity is not found"
        touch $TDK_PATH/logs/Recorder_testmodule_prereq_details.log;
        echo  "FAILURE<DETAILS>sed utillity is not found" >> $TDK_PATH/logs/Recorder_testmodule_prereq_details.log
        exit 1
     fi
else
     echo $rmf_flags "is not found in rmfconfig.ini"
     touch $TDK_PATH/logs/Recorder_testmodule_prereq_details.log;
     echo  "FAILURE<DETAILS>" $rmf_flags "is not found in rmfconfig.ini" >> $TDK_PATH/logs/Recorder_testmodule_prereq_details.log

fi

