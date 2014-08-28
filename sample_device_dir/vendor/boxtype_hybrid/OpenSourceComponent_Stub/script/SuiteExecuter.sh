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
#Setting default values to Environment variables
EXEC_STRING="NULL"
. $OPENSOURCETEST_PATH/opensrc_comp_test.properties
LOG_NAME=$SUMMARY_LOG_NAME
echo $LOG_NAME
GRAPHICS="qt_gfx"
NON_GRAPHICS="qt_non_gfx"
WEBKIT="webkit"
GSTREAMER="gstreamer"

#fix for network related qt applications
if grep "qt-test-server.qt-test-net" /etc/hosts
then
   echo "QT server already configured"
else
     echo "127.0.0.1 qt-test-server.qt-test-net" >> /etc/hosts
fi

#Listing the usage of Suite Executor script
usage() { 

echo "Usage: `basename $0` [-c Component name] [-h help]"
echo " -c     Specify the name of the component."
echo "Example:Enter qt_non_gfx for qt non gfxs test runs & enter qt_gfx for gfx test runs " 
echo "        Enter webkit for webkit test runs "
echo "        Enter gstreamer for gstreamer, gst_plugin_base for gstreamer-plugins-base or gst_plugin_good for gstreamer-plugins-good test suite execution"
echo "        Enter glib for glib test runs "
echo "        Enter openssl for  openssl test runs "
echo "        Enter libSoup for libsoup test runs "
echo "        Enter Jansson for Jansson test runs "
}
while getopts ":hp:o:c:" opt; do
    case $opt in
        h)
            usage
            exit
            ;;
        c)
            COMPONENT_NAME=$OPTARG
            echo $COMPONENT_NAME 
            ;;
	o)
            OPTIONS=$OPTARG
            echo $OPTIONS
            ;;
        \?)
            usage
            exit
            ;;
        :)
 	   echo "Option -$OPTARG requires an argument." >&2
           echo "   try 'SuiteExecuter.sh -h' for more information"
           exit 1
           ;;	      
    esac
done

if [ -z "$1" ]; then
  usage
  exit 1
fi

if [ -z "$COMPONENT_NAME" ]; then
  echo "-c 'COMPONENT NAME' is a required argument" >&2
  exit 1
fi

if [[ "$COMPONENT_NAME" == "$GRAPHICS" || "$COMPONENT_NAME" == "$WEBKIT" ]]; then
   if [ -z "$OPTIONS" ]; then
      echo "-o 'OPTIONS' is a required argument" >&2
      exit 1
   fi        
fi

#Checking for component name and setting the respective environment variable
case $COMPONENT_NAME in
     qt_non_gfx)
         BIN_PATH=$QT_NON_GFX_BIN_PATH
         SEARCH_KEY="Totals:"
         LOG_PATH=$QT_NONGFX_LOG_PATH
         OPTIONS="null"
         ;;
     qt_gfx)
	 BIN_PATH=$QT_GFX_BIN_PATH
         SEARCH_KEY="Totals:"
         LOG_PATH=$QT_GFX_LOG_PATH
         ;;
     webkit)
         BIN_PATH=$WEBKIT_BIN_PATH
         SEARCH_KEY="Totals:"
         LOG_PATH=$WEBKIT_LOG_PATH
         ;;
     gstreamer)
	 BIN_PATH=$GSTREAMER_BIN_PATH
         SEARCH_KEY="Checks:"
         OPTIONS="NULL"
         LOG_PATH=$GSTREAMER_LOG_PATH
         ;;
     gst_plugin_base)
	 BIN_PATH=$GSTREAMER_BASE_BIN_PATH
         SEARCH_KEY="Checks:"
         OPTIONS="NULL"
         LOG_PATH=$GSTREAMER_BASE_LOG_PATH
         ;;
     gst_plugin_good)
	 BIN_PATH=$GSTREAMER_GOOD_BIN_PATH
         SEARCH_KEY="Checks:"
         OPTIONS="NULL"
         LOG_PATH=$GSTREAMER_GOOD_LOG_PATH
         ;;
     glib)
         BIN_PATH=$GLIB_BIN_PATH
         SEARCH_KEY="OK"
         OPTIONS="NULL"
         LOG_PATH=$GLIB_LOG_PATH
         ;;
     openssl)
         BIN_PATH=$OPENSSL_BIN_PATH
         SEARCH_KEY="NULL"
         OPTIONS="NULL"
         LOG_PATH=$OPENSSL_LOG_PATH
	 ;;
     libsoup)
         BIN_PATH=$LIBSOUP_BIN_PATH
         SEARCH_KEY="OK"
	 OPTIONS="NULL"
         LOG_PATH=$LIBSOUP_LOG_PATH
	 ;;
     jansson)
         BIN_PATH=$JANSSON_BIN_PATH
         SEARCH_KEY="suites"
	 OPTIONS="NULL"
         LOG_PATH=$JANSSON_LOG_PATH
         MASTER_SUITE="run-suites"
	 export VERBOSE=1
	 export top_srcdir=$OPENSOURCETEST_PATH/jansson
	 ;;
     qt5)
         BIN_PATH=$QT_5_BIN_PATH
         SEARCH_KEY="Totals:"
	 OPTIONS="NULL"
         LOG_PATH=$QT_5_LOG_PATH
	 ;;
     qt5webkit)
         BIN_PATH=$WEBKIT_5_BIN_PATH
         SEARCH_KEY="Totals:"
	 OPTIONS="NULL"
         LOG_PATH=$WEBKIT_5_LOG_PATH
	 ;;
      yajl)
         BIN_PATH=$YAJL_BIN_PATH
         SEARCH_KEY="successful"
         OPTIONS="NULL"
         LOG_PATH=$YAJL_LOG_PATH
         MASTER_SUITE="run_tests.sh"
         ;;
       *)
         echo "At this moment qt_non_gfx , qt_gfx, webkit, gstreamer,gstreamer base plugin and gstreamer good plugin tests can run "
         exit
         ;;
esac

GetSuiteStatus()
{
   COMP_NAME=$1
   LOG_PATH=$2
   Log_File=log_$3
   TEST_NAME=$3
   echo "component inside func"$COMP_NAME
   if [[ "$COMP_NAME" == "glib" || "$COMP_NAME" == "libsoup" ]]; then
        if [ "$COMP_NAME" == "glib" ]; then
           StringPattern="/".*"/".*":"
        elif [ "$COMP_NAME" == "libsoup" ]; then
           TEST_NAME=`echo $TEST_NAME | cut -d "-" -f3-`
           StringPattern=$TEST_NAME":"
        fi
        
        echo $StringPattern
        TotalTest=`cat $LOG_PATH/$Log_File|grep -nr $StringPattern|wc -l`
        echo $TotalTest
        success_string="OK"
        Success_count=`cat $LOG_PATH/$Log_File|grep -nr $success_string|wc -l`
        echo $Success_count
        Failure_count=$((TotalTest-Success_count))
        echo $Failure_count
        echo "Totals:"$TotalTest" PASSED:"$Success_count" FAILED:"$Failure_count > $LOG_PATH/TEMPFILE2
   elif [ "$COMP_NAME" == "openssl" ]; then
       echo "Refer the "$Log_File " for the Execution status " > $LOG_PATH/TEMPFILE2 
   fi

}

#Depends on the argument ,Execute the respective test suite. 
Execute(){ 
   BIN_PATH=$1
   NEXT_LINE='
'
   LOG_NAME=$3
   COMP_NAME=$2
   EXEC_OPTION=$4
   KEY_WORD=$5
   LOG_PATH=$6
   echo "EXECUTER_PATH" $$EXECUTER_PATH
   
   #Removing the old logs and Summary log
   rm -f $EXECUTER_PATH/LOGPATH_INFO
   rm -f $LOG_PATH/log_*
   rm -f $LOG_PATH/$LOG_NAME
   rm -f $LOG_PATH/TEMPFILE*
   rm -f $LOG_PATH/TEMP_FILES
   rm -f $EXECUTER_PATH/SUITE_STATUS
                        

   #Navigate in to mentioned path
   cd $BIN_PATH
   if [ $? != 0 ]; then
   	echo $BIN_PATH is not found
   	echo $BIN_PATH is not found >> $EXECUTER_PATH/SUITE_STATUS
   	echo $BIN_PATH "is not found" > $EXECUTER_PATH/LOGPATH_INFO
   	exit 1
   fi
   echo "Binary path:"$BIN_PATH
   echo "Component Name:"$COMPONENT_NAME

   #Creating the summary log and changing the log file permissions
   if [[ "$COMP_NAME" == "jansson" || "$COMP_NAME" == "yajl" ]]; then
	mkdir -p $LOG_PATH
	touch $LOG_PATH/log_$COMP_NAME
	sh $MASTER_SUITE &>$LOG_PATH/log_$COMP_NAME
	touch $EXECUTER_PATH/LOGPATH_INFO   
	echo "Generating Log Path Info......"
	echo "$COMP_NAME log path name:" $LOG_PATH
	echo $LOG_PATH"/"log_$COMP_NAME >> $EXECUTER_PATH/LOGPATH_INFO
	cat  $LOG_PATH/log_$COMP_NAME
	cat  $LOG_PATH/log_$COMP_NAME|grep "$KEY_WORD" > $EXECUTER_PATH/SUITE_STATUS

   else

        #Creating the summary log and changing the log file permissions
        mkdir -p $LOG_PATH
        touch $LOG_PATH/$LOG_NAME
        chmod 777 $LOG_PATH/$LOG_NAME 
   	IGNORE_LIST=`echo $FILES_TO_IGNORE | tr "," " "`
   	echo "Ignore File List :"$IGNORE_LIST 
   	#Finding the total executables counts
   	FILE_LIST=$(ls)
   	echo "FILE_LIST:"$FILE_LIST
         
   	#Ignoring the list of files from the execution list
   	for FILE in $FILE_LIST
   	do
      		echo $FILE$NEXT_LINE >> $LOG_PATH/TEMP_FILES
   	done
   	for IGNORE_FILE in $IGNORE_LIST
   	do
      		echo "IGNOREFILE:"$IGNORE_FILE
      		sed -i "/$IGNORE_FILE/d" $LOG_PATH/TEMP_FILES
   	done
   	FILE_LIST=`cat $LOG_PATH/TEMP_FILES`
   	echo "FILE_LIST:"$FILE_LIST
   
        TOTAL_FILE_COUNT=`cat $LOG_PATH/TEMP_FILES |wc -l`
   	echo "Total file count :"$TOTAL_FILE_COUNT
   	echo "Total Test suite available :"$TOTAL_FILE_COUNT >> $LOG_PATH/$LOG_NAME
   	if [ $TOTAL_FILE_COUNT == 0 ]; then
   		echo "No binaries are availble to execute"
   		echo "No binaries are availble to execute" > $EXECUTER_PATH/SUITE_STATUS
   		echo "No binaries are availble to execute" > $EXECUTER_PATH/LOGPATH_INFO
   		exit 1
   	fi	
   	EXECUTE_SUCCESS_COUNTER=0
   	EXECUTE_FAILURE_COUNTER=0

  	#Test Execution
   	echo "FILE_LIST:"$FILE_LIST
   	for ELEMENT in $FILE_LIST
	do
       
      		echo "Test Suite Name :"$ELEMENT
      		echo "Test Suite Name :"$ELEMENT";" > $LOG_PATH/TEMPFILE1
      		if [[ "$COMP_NAME" == "$GRAPHICS" || "$COMP_NAME" == "$WEBKIT" ]]; then	
        		./$ELEMENT -qws -display $EXEC_OPTION &> $LOG_PATH/log_$ELEMENT
      		else
        		./$ELEMENT &> $LOG_PATH/log_$ELEMENT
      		fi
    
	      #Collecting the log details and store in to Summary_Log
	      if [[ "$COMP_NAME" == "glib" || "$COMP_NAME" == "openssl" || "$COMP_NAME" == "libsoup" ]]; then
		   echo $COMP_NAME
		   GetSuiteStatus $COMP_NAME $LOG_PATH $ELEMENT
	      else
	   	   echo "Finding the execution status from log with the keyword : "$KEY_WORD
	   	   cat  $LOG_PATH/log_$ELEMENT
	   	   cat  $LOG_PATH/log_$ELEMENT|grep $KEY_WORD > $LOG_PATH/TEMPFILE2
	      fi
	      if [ "$COMP_NAME" != "openssl" ]; then
	   	#Checking the results of each suite execution 
	   	EXECUTION_CHECK=`cat  $LOG_PATH/log_$ELEMENT|grep -c $KEY_WORD`
	   	if [ $EXECUTION_CHECK -gt 0 ]; then
                   EXECUTE_SUCCESS_COUNTER=$((EXECUTE_SUCCESS_COUNTER+1))
	           echo "Number of TestSuite Executed :"$EXECUTE_SUCCESS_COUNTER
	        else
                   EXECUTE_FAILURE_COUNTER=$((EXECUTE_FAILURE_COUNTER+1))
	           echo "Number of TestSuite Not Executed :"$EXECUTE_FAILURE_COUNTER
	        fi
	        touch $EXECUTER_PATH/SUITE_STATUS
	        echo "TotalSuite:"$TOTAL_FILE_COUNT" TestSuiteExecuted:"$EXECUTE_SUCCESS_COUNTER" SuiteNotExecuted:"$EXECUTE_FAILURE_COUNTER > $EXECUTER_PATH/SUITE_STATUS
	     fi 
             #Exporting log path in to temp file
             echo ";"$LOG_PATH"/log_"$ELEMENT >$LOG_PATH/TEMPFILE3
  
	    #Exporting the Summary details in to TestSummary.log        
	    cat $LOG_PATH/TEMPFILE1 $LOG_PATH/TEMPFILE2 $LOG_PATH/TEMPFILE3|tr '\n' " " >> $LOG_PATH/$LOG_NAME
	    echo $NEXT_LINE >> $LOG_PATH/$LOG_NAME

	   #Removing the Temp Files
	   rm -f $LOG_PATH/TEMPFILE*

	   done

	   #Exporting Summary log path and file name to stub
	   touch $EXECUTER_PATH/LOGPATH_INFO   
	   echo "Generating Log Path Info......"
	   echo $LOG_PATH"/"$LOG_NAME >> $EXECUTER_PATH/LOGPATH_INFO
  fi

}

#Executing the testsuite
Execute $BIN_PATH $COMPONENT_NAME $LOG_NAME $OPTIONS $SEARCH_KEY $LOG_PATH

