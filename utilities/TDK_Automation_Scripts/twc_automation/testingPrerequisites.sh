##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
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
