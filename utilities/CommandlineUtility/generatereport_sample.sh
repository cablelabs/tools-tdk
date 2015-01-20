#!/bin/bash
echo ">>>>>>>>>>>>>>>>>"
echo $1
#if [ $3 == "GSTREAMER" ];then
#    EXEC_ID=$4
#elif [ $3 == "WEBKIT" ];then   
#    EXEC_ID=$4
#elif [ $3 == "RDKWEBKIT" ];then   
#    EXEC_ID=$4
#fi

EXEC_ID=$4
echo $EXEC_ID

EXEC_NAME=$5
echo $EXEC_NAME

EXEC_DEVID=$6
echo $EXEC_DEVID

SCRIPT_PATH=$PWD/

#LOG_PATH=$2/$EXEC_ID/
LOG_PATH=$2/$EXEC_ID/$EXEC_DEVID
echo $LOG_PATH
echo "1234567:: "

if [ -d "TEMP" ]; then 
    echo "TEMP folder found"    
    rm -r TEMP
fi

mkdir TEMP

find $LOG_PATH -type f ! -name "*TestSummary*" -exec cp {} TEMP/ \;
LOG_ELEMENT=$(ls TEMP/)
echo "LOG_ELEMENT"
echo $LOG_ELEMENT
if [ $3 == "WEBKIT" ];then
for LOG_NAME in $LOG_ELEMENT
do
    sed -i "/egmentation fault/c\<Incident type=\"error\" file=\"\" line=\"0\"/>\n</TestFunction>\n<\/TestCase>" TEMP/$LOG_NAME   
    sed -i "/Unexpected Critical\/Warnings*/c\<Incident type=\"error\" file=\"\" line=\"0\"/>\n</TestFunction>\n<\/TestCase>" TEMP/$LOG_NAME   
    awk '$1 ~ /^</ || $NF ~ />$/' TEMP/$LOG_NAME>>temp.xml
    cat 'temp.xml' >>  TEMP/"$LOG_NAME.xml"
    rm 'temp.xml'
    rm TEMP/$LOG_NAME
    	
done

elif [ $3 == "RDKWEBKIT" ];then
for LOG_NAME in $LOG_ELEMENT
do
    sed -i "/egmentation fault/c\<Incident type=\"error\" file=\"\" line=\"0\"/>\n</TestFunction>\n<\/TestCase>" TEMP/$LOG_NAME   
    sed -i "/Unexpected Critical\/Warnings*/c\<Incident type=\"error\" file=\"\" line=\"0\"/>\n</TestFunction>\n<\/TestCase>" TEMP/$LOG_NAME   
    awk '$1 ~ /^</ || $NF ~ />$/' TEMP/$LOG_NAME>>temp.xml
    cat 'temp.xml' >>  TEMP/"$LOG_NAME.xml"
    rm 'temp.xml'
    rm TEMP/$LOG_NAME
    	
done

elif [[ $3 == "GSTREAMER" || $3 == "DLNA" ]];then
echo "LOGNAME"
echo $LOG_NAME
for LOG_NAME in $LOG_ELEMENT
do
    #sed -i "/egmentation fault/c\<Incident type=\"error\" file=\"\" line=\"0\"/>\n</TestFunction>\n<\/TestCase>" TEMP/$LOG_NAME   
    #sed -i "/Unexpected Critical\/Warnings*/c\<Incident type=\"error\" file=\"\" line=\"0\"/>\n</TestFunction>\n<\/TestCase>" TEMP/$LOG_NAME   
    echo $1
    echo $NF 
    awk '$1 ~ /^</ || $NF ~ />$/' TEMP/$LOG_NAME>>temp.xml
    cat temp.xml
    cat 'temp.xml' >>  TEMP/"$LOG_NAME.xml"
    rm 'temp.xml'
    #rm TEMP/$LOG_NAME
    sh xml_check.sh TEMP/"$LOG_NAME.xml"    	
done

else 
    echo "Enter the 3rd argument properly::GSTREAMER/WEBKIT"
fi
python $SCRIPT_PATH/ReportGenerator.py $1 $3
python $SCRIPT_PATH/PerformanceReportGenerator.py $1 $3 $5 
#rm -r TEMP
echo "end of script"
