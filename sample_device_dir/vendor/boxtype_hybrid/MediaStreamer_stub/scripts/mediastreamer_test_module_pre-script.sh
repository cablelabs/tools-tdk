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
MPEENV_PATH=/mnt/nfs/env
TARGET_PATH=/opt
SCRIPT_PATH=$TDK_PATH
LOG_PATH=$TDK_PATH/logs
LOGFILE=Mediastreamer_testmodule_prereq_details.log

mkdir -p $LOG_PATH
#removing old configuring status from the opt
rm $LOG_PATH/$LOGFILE

#Editing the mpeenv.ini to disbale the dtcp flag
dtcp_flags="FEATURE.DTCP.SUPPORT"
for flag in $dtcp_flags
do
	FLAG_SEARCH_STATUS=`grep $flag $TARGET_PATH/mpeenv.ini|wc -l`
	if [ $FLAG_SEARCH_STATUS -ne 0 ]
	then
	     echo $flag is found in mpeenv.ini
	     #Editing the flag to false
	     sed -i -e 's/'$flag'=TRUE/'$flag'=FALSE/g' $TARGET_PATH/mpeenv.ini
	     if [ $? -eq 0 ]
	     then
	     	echo "mpeenv.ini file edited"
	     	touch $LOG_PATH/$LOGFILE
	     	echo  "SUCCESS" > $LOG_PATH/$LOGFILE
	     else
	        echo "sed utillity is not found"
	        touch $LOG_PATH/$LOGFILE
	        echo  "Failure<details>sed utillity is not found" > $LOG_PATH/$LOGFILE
	        exit 1
	     fi
	else
	     echo $flag "is not found in mpeenv.ini"
	     touch $LOG_PATH/$LOGFILE
	     echo  "FAILURE<DETAILS>"$flag "is not found in mpeenv.ini" > $LOG_PATH/$LOGFILE
	     exit 1
	fi
done

#Kill the Guide Application		
