# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================
RMFCONFIG_PATH=/etc
TDK_PATH=/opt/TDK
TARGET_PATH=/opt
SCRIPT_PATH=$TDK_PATH
LOG_PATH=$TDK_PATH/logs
PID_FILE=$TDK_PATH/Pid.txt
LOGFILE=Mediaframework_testmodule_prereq_details.log

mkdir -p $LOG_PATH
#removing old configuring status from the opt
rm $LOG_PATH/$LOGFILE
rm $PID_FILE

#Editing the rmf_config.ini to disbale the dtcp flag
rmf_flags="FEATURE.DTCP.SUPPORT FEATURE.MRDVR.MEDIASTREAMER.DLNA.DTCP.SUPPORT DTCP_IP_FORCE_ENCRYPTION"
for flag in $rmf_flags
do
        FLAG_SEARCH_STATUS=`grep $flag $TARGET_PATH/rmfconfig.ini|wc -l`
        if [ $FLAG_SEARCH_STATUS -ne 0 ]
        then
             echo $flag is found in rmfconfig.ini
             #Editing the flag to false
             sed -i -e 's/'$flag'=TRUE/'$flag'=FALSE/g' $TARGET_PATH/rmfconfig.ini
             if [ $? -eq 0 ]
             then
                echo "rmfconfig.ini file edited"
                touch $LOG_PATH/$LOGFILE
                echo  "SUCCESS" > $LOG_PATH/$LOGFILE
             else
                echo "sed utillity is not found"
                touch $LOG_PATH/$LOGFILE
                echo  "Failure<details>sed utillity is not found" > $LOG_PATH/$LOGFILE
                exit 1
             fi
        else
             echo $flag "is not found in rmfconfig.ini"
             touch $LOG_PATH/$LOGFILE
             echo  "FAILURE<DETAILS>"$flag "is not found in rmfconfig.ini" > $LOG_PATH/$LOGFILE
             exit 1
        fi
done

#Validating  RMF Streamer is running or not
echo "Going to check rmfStreamer"
sh /lib/rdk/processPID.sh rmfStreamer > $PID_FILE
if [ -s "$PID_FILE" ]; then
        echo "rmfStreamer  running"
else
        echo "rmfStreamer not running"
        touch $LOG_PATH/$LOGFILE
        echo "FAILURE<details>RMF_STREAMER_NOT_RUNNING" > $LOG_PATH/$LOGFILE
        exit 1
fi
