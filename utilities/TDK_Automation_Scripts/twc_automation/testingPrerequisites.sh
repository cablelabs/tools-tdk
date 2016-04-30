#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
TDK_AUTOMATION_PATH="/tdk/TDK_Automation_Scripts/twc_automation"
SCRIPT_PATH=`pwd`
export STB_IP_ADDRESS=$1
export STB_TELNET_PORT="23"

#####################################
#KIlling all Zombie/pending processes
#####################################

echo " Checking for prerequisites before starting the execution of test cases"
echo "Prerequisite1:Cleaning All the Zombie/pending processess (TdkTestExecuter.py and commonTestScript) "
python CleanHostMachineProcess.py

echo " Host machine is cleaned"

#####################################
#Rebooting STB
#####################################

if nc -vz $STB_IP_ADDRESS $STB_TELNET_PORT
then
	sleep 10 
	echo "./rebootSTB.sh $STB_IP_ADDRESS"	
	./rebootSTB.sh $STB_IP_ADDRESS
	sleep 20
fi


counter=0
while ! ping -c1 $STB_IP_ADDRESS &>/dev/null; do sleep 20; let counter++; if [[ "$counter" -gt 50 ]]; then break; fi; echo "Testing STB Bootup ...\n"; done
#####################################
#Starting Agent in STB
#####################################

echo "\r\r******* Starting Agent... ********\r\r"
if nc -vz $STB_IP_ADDRESS $STB_TELNET_PORT
then
	echo $SCRIPT_PATH
	cd $SCRIPT_PATH
	echo "./runAgent.sh $STB_IP_ADDRESS"
	./runAgent.sh $STB_IP_ADDRESS
	echo "\r\r******* Agent Started... *******\r\r"	
	sleep 30
else
	sleep 240
fi
echo "\r\r******* Agent Started Successfully... ********\r\r"

########################################
#Starting Test Case Execution Using Command Line Automation
########################################
echo "\r\r************Executing Test Cases....************\n\n"
pwd
cd $SCRIPT_PATH
pwd
chmod +x *.py
echo "python TdkTestExecuter.py TdkConfig.xml $STB_IP_ADDRESS"
python TdkTestExecuter.py TdkConfig.xml $STB_IP_ADDRESS
