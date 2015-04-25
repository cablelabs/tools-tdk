SCRIPT_PATH=$TDK_PATH/script/
LOG_PATH=$TDK_PATH/
LOGFILE=output_json_parser_details.log
STREAMING_IP=$1
BASE_URL=$2
echo "Base Url : " $BASE_URL
echo "Streaming IP :" $STREAMING_IP

#check for xdiscovery.conf file
cmd=`cat $XDISCOVERY_PATH/xdiscovery.conf|grep outputJsonFile=|grep -v "#"|awk -F "=" '{print $2}'`
if [ $? == 0 ] && [ "$cmd" != "" ]; then
        echo $cmd
        echo "output.json location has parsed successfully"
        echo SUCCESS > $LOG_PATH/$LOGFILE
else
	echo $cmd
        echo "Not able to parse xdiscovery.conf "
        echo FAILURE > $LOG_PATH/$LOGFILE
        exit 1
fi

if [ "$STREAMING_IP" == "mdvr" ]; then
	Parse_out=`cat $cmd |grep playbackUrl|cut -f2- -d":"|cut -f1 -d "&"|cut -f2 -d "\""|head -1`
        if [ $? == 0 ] && [ "$Parse_out" != "" ]; then
        	echo $Parse_out
                echo "Got proper play url from output.json"
                echo SUCCESS > $LOG_PATH/$LOGFILE
        else
        	echo $Parse_out
                echo "Not able to parse output.json "
                echo FAILURE > $LOG_PATH/$LOGFILE
                exit 1
        fi
else 
                                                                                                                                        
#Parse the play url from output.json
Parse_out=`cat $cmd |grep playbackUrl|cut -f2- -d":"|cut -f1 -d "&"|grep $STREAMING_IP|cut -f2 -d "\""`
if [ $? == 0 ] && [ "$Parse_out" != "" ]; then
	echo $Parse_out
        echo "Got proper play url from output.json"
        echo SUCCESS > $LOG_PATH/$LOGFILE
else
	Parse_out=`cat $cmd |grep playbackUrl|cut -f2- -d":"|cut -f1 -d "&"|grep 127.0.0.1|cut -f2 -d "\""`
        if [ $? == 0 ] && [ "$Parse_out" != "" ]; then
        	echo $Parse_out
                echo "Got proper play url from output.json"
                echo SUCCESS > $LOG_PATH/$LOGFILE
        else
        	echo $Parse_out
                echo "Not able to parse output.json "
                echo FAILURE > $LOG_PATH/$LOGFILE
                exit 1
        fi
 fi
fi                                                                                                                                             
#parse the base URL
Parse_base=`echo $BASE_URL |cut -f2 -d "?"`
if [ $? == 0 ] && [ "$Parse_base" != "" ]; then
	echo $Parse_base
	echo "Parsed the base url properly"
        echo SUCCESS > $LOG_PATH/$LOGFILE
else
        echo $Parse_base
        echo "Not able to parse base url "
        echo FAILURE > $LOG_PATH/$LOGFILE
        exit 1
fi
                                                                                                                                                                                                                                                                                                                        
#Concat the final url
final_url=$Parse_out"&"$Parse_base
echo $final_url > $LOG_PATH/$LOGFILE



                                                                                                                                                                                                        
