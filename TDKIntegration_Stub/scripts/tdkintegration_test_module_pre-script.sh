#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast. It may
#  not be used, copied, distributed or otherwise disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2014 Comcast. All rights reserved.
#  ============================================================================

#RMFCONFIG_PATH=/etc
TARGET_PATH=/opt
SCRIPT_PATH=$TDK_PATH
LOG_PATH=$TDK_PATH/logs
#LOGFILE=tdkintegration_testmodule_prereq_details.log

mkdir -p $LOG_PATH
#removing old configuring status from the opt
#rm $LOG_PATH/$LOGFILE

#Editing the rmf_config.ini to disbale the dtcp flag
#rmf_flags="FEATURE.DTCP.SUPPORT FEATURE.MRDVR.MEDIASTREAMER.DLNA.DTCP.SUPPORT DTCP_IP_FORCE_ENCRYPTION"
#for flag in $rmf_flags 
#do
#	FLAG_SEARCH_STATUS=`grep $flag $TARGET_PATH/rmfconfig.ini|wc -l`
#	if [ $FLAG_SEARCH_STATUS -ne 0 ]
#	then
#	     echo $flag is found in rmfconfig.ini
#	     #Editing the flag to false
#	     sed -i -e 's/'$flag'=TRUE/'$flag'=FALSE/g' $TARGET_PATH/rmfconfig.ini
#	     if [ $? -eq 0 ]
#	     then
#	     	echo "rmfconfig.ini file edited"
#	     	touch $LOG_PATH/$LOGFILE
#	     	echo  "SUCCESS" > $LOG_PATH/$LOGFILE
#	     else
#	        echo "sed utillity is not found"
#	        touch $LOG_PATH/$LOGFILE
#	        echo  "Failure<details>sed utillity is not found" > $LOG_PATH/$LOGFILE
#	        exit 1
#	     fi
#	else
#	     echo $flag "is not found in rmfconfig.ini"
#	     touch $LOG_PATH/$LOGFILE
#	     echo  "FAILURE<DETAILS>"$flag "is not found in rmfconfig.ini" > $LOG_PATH/$LOGFILE
#	     exit 1
#	fi
#done

jsonlocationvalue=`cat /$XDISCOVERY_PATH/xdiscovery.conf |grep outputJsonFile|awk -F '=' '{print $2};'`
echo $jsonlocationvalue
echo "Waiting for output.json "
while [ ! -f $jsonlocationvalue ];
do
        sleep 1
	count=$((count+1))
        if [ $count -eq "60" ]; then
                exit 1
        fi
done
echo "Found : $jsonlocationvalue"

#Kill the Guide Application
#/etc/init.d/xre-service stop
#if [ $? -eq 0 ]
#then
#	echo  "xre stopped"
#else
#	echo "xre not stopped"
#fi
                                                                                                                                
