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
#



#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import os
import sys
import time
import signal
import subprocess
import tdklib
import pipes
import urllib
import json

def getDeviceBoxType(self):

        # Create an object for getDeviceBoxType

        # Syntax      : OBJ.getDeviceBoxType()
        # Description : Create an object of Device Box Type
        # Parameters  : None
        # Return Value: Return the box type

                 url = self.url + '/deviceGroup/getDeviceBoxType?deviceIp='+self.ip
                 response = urllib.urlopen(url).read()
                 if 'SUCCESS' in response:
                        boxType = json.loads(response)
                 else:
                        print "#TDK_@error-ERROR : Unable to get Device Box Type from REST !!!"
                        exit()

                 sys.stdout.flush()
                 return boxType['boxtype']

        ########## End of Function ##########

def SnmpExecuteCmd(Obj,SnmpMethod,SnmpVersion,OID,IP_Address):

        # To invoke and fetch status of SNMP command for a particular box

        # Parameters   : SnmpMethod, SnmpVersion, OID, IP_Address
        # SnmpMethod   : Method name. e.g., snmpget, snmpset, snmpwalk etc.,
        # SnmpVersion  : Version of snmp 
	# OID          : Object ID
	# IP_Address   : IP address of the device
        # Return Value : Console output of the snmp command

	expectedResult="SUCCESS";
        Obj.executeTestCase(expectedResult);	
        actualresult = Obj.getResult();
        details = Obj.getResultDetails().strip();
	BoxType = getDeviceBoxType(Obj);
        print "result", actualresult, details;

	if expectedResult not in actualresult:
		return details;

	if "." in IP_Address:
		
		# Constructing Query Command
		if "Emulator" in BoxType and SnmpMethod == "snmpset":
			details = "private";

		cmd=SnmpMethod + ' -OQ -Ir ' + SnmpVersion + ' -c ' + details + ' ' + IP_Address + ' ' +  OID
	else:
		cmd=SnmpMethod + ' -c ' + details + ' ' + SnmpVersion + ' udp6:['+ IP_Address + '] ' + OID

	class Timout(Exception):
       	        pass
        def timeoutHandler(signum, frame):
       	        raise Timout	
        signal.signal(signal.SIGALRM, timeoutHandler)
       	signal.alarm(20)

        # Executing request command
        try:
                print "Executing cmd\"",cmd," \""
                sys.stdout.flush()
                output = subprocess.check_output(cmd, shell=True)
		print "byteStr ",output;
                output = output.replace("<<", "")
                output = output.replace(">>", "")
                outdata = unicode(output, errors='ignore')
                signal.alarm(0)  # reset the alarm
        except Timout:
                print "Timeout!! Taking too long"
                outdata = "ERROR: Timeout!! Taking too long"
                sys.stdout.flush()
		signal.alarm(0)  # reset the alarm
                return outdata
        except:
                print "Unable to execute snmp command"
                outdata = "ERROR: Unable to execute snmp command"
                sys.stdout.flush()
		signal.alarm(0)  # reset the alarm
                return outdata

        return outdata


