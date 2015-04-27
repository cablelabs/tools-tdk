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
