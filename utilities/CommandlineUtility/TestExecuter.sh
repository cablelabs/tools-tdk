#!/bin/sh
 
TARGET_IP=192.168.160.170 
PORT_ID=8087

LOG_PATH=/opt/apache-tomcat-6.0.41/webapps/rdk-test-tool/logs/
echo $LOG_PATH

#BUILD_VER=Release-1.0
#BUILD_VER=Release-1.0.2
#BUILD_VER=Release-1.0.3
BUILD_VER=Release-1.0.4

TEST_MANAGER_URL="http://192.168.161.32:8080/rdk-test-tool"

DEV_NAME="170_box_TVM"

datestring=`date +"%d%m%Y%H%M%S"`
EXEC_NAME="$DEV_NAME-$datestring"
echo "Execution Name is: "$EXEC_NAME

TESTS_TO_RUN="GSTREAMER"
if [ "$TESTS_TO_RUN" == "GSTREAMER" ]; then
    python GstreamerBasePluginTest.py $TARGET_IP $PORT_ID $LOG_PATH $TEST_MANAGER_URL $EXEC_NAME > GstreamerBasePluginTest.log
    file=$PWD/GstreamerBasePluginTest.log
    if [ -f $file ]; then
	EXEC_ID=`grep EXEC_ID $file | tail -1 | cut -d = -f3 | cut -d : -f2` 
	EXEC_DEVID=`grep EXEC_DEVID $file | tail -1 | cut -d = -f3 | cut -d : -f2`
    fi
    sh generatereport_sample.sh $BUILD_VER $LOG_PATH $TESTS_TO_RUN $EXEC_ID $EXEC_NAME $EXEC_DEVID
fi

#datestring=`date +"%d%m%Y%H%M%S"`
#EXEC_NAME="$DEV_NAME-$datestring"
#echo "Execution Name is: "$EXEC_NAME

#TESTS_TO_RUN="DLNA"
#if [ "$TESTS_TO_RUN" == "DLNA" ]; then
    #python DlnaTest.py $TARGET_IP $PORT_ID $LOG_PATH $TEST_MANAGER_URL $EXEC_NAME > DlnaTest.log
    #file=$PWD/DlnaTest.log
    #if [ -f $file ]; then
#	EXEC_ID=`grep EXEC_ID $file | tail -1 | cut -d = -f3 | cut -d : -f2` 
#	EXEC_DEVID=`grep EXEC_DEVID $file | tail -1 | cut -d = -f3 | cut -d : -f2`
  #  fi
 #   sh generatereport_sample.sh $BUILD_VER $LOG_PATH $TESTS_TO_RUN $EXEC_ID $EXEC_NAME $EXEC_DEVID
#fi
