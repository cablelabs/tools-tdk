# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================
TDK_PATH=/opt/TDK/
LOGPATH=$TDK_PATH
LOGFILE=logs/Mediaframework_qamsrc_testmodule_postreq_details.log
rm $LOGPATH/$LOGFILE
touch $LOGPATH/$LOGFILE
## Script for stoping rmfstremer and its dependent services in yocto and non-yocto images
if [ -f /etc/os-release ]; then
    systemctl stop dump-log.timer
    systemctl stop dump-log.service
    systemctl stop htmldiag-pre.service
    systemctl stop logrotate.timer 
    systemctl stop logrotate.service 
    systemctl stop rmfstreamer.service	
else
	sh /lib/rdk/processPID.sh monitorRMF.sh|xargs kill -9
	if [ $? == 0 ]; then
		echo "monitorRMF is killed"
		echo "SUCCESS" > $LOGPATH/$LOGFILE
	else
		echo "monitorRMF is not running"
		echo "SUCCESS" > $LOGPATH/$LOGFILE
	fi
fi
sh /lib/rdk/processPID.sh rmfStreamer |xargs kill -9
if [ $? == 0 ]; then
        echo "rmfstreamer is killed"
        echo "SUCCESS" > $LOGPATH/$LOGFILE
else
	echo "rmfstreamer is not running"
	echo "SUCCESS" > $LOGPATH/$LOGFILE
fi
cp /etc/rmfconfig.ini $LOGPATH/
cp /etc/debug.ini $LOGPATH/
