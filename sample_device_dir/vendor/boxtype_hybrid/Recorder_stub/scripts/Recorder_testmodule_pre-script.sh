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
RMFCONFIG_PATH=/etc/
TARGET_PATH=/opt/
TDK_PATH=/opt/TDK
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

