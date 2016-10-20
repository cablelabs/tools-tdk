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
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>13</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_PowerModeToggle_Trickplay</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>528</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_LinearTV_Play_URL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Tests if STB is able to tune to linear channel when going from standby to on state.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from iarmbus import change_powermode
from tdkintegration import dvrPlayUrl;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
iarmObj.configureTestCase(ip,port,'E2E_RMF_PowerModeToggle_Trickplay');
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[IARMBUS LIB LOAD STATUS] : %s"%iarmLoadStatus ;
iarmObj.setLoadModuleStatus(iarmLoadStatus);

tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
tdkIntObj.configureTestCase(ip,port,'E2E_RMF_PowerModeToggle_Trickplay');
tdkIntLoadStatus = tdkIntObj.getLoadModuleResult();
print "TDKIntegration LIB LOAD STATUS :  %s" %tdkIntLoadStatus;
tdkIntObj.setLoadModuleStatus(tdkIntLoadStatus);

expectedresult="SUCCESS"
tdkIntLoaddetails = tdkIntObj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in tdkIntLoadStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in tdkIntLoaddetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdkIntObj.initiateReboot();
                iarmObj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdkIntObj.configureTestCase(ip,port,'E2E_RMF_simultaneous_recording_liveplayback');
                #Get the result of connection with test component and STB
                tdkIntLoadStatus =tdkIntObj.getLoadModuleResult();
                iarmLoadStatus = iarmObj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %tdkIntLoadStatus;
if (expectedresult in iarmLoadStatus.upper()) and (expectedresult not in tdkIntLoadStatus.upper()):
        iarmObj.unloadModule("iarmbus");
elif (expectedresult in tdkIntLoadStatus.upper()) and (expectedresult not in iarmLoadStatus.upper()):
        tdkIntObj.unloadModule("tdkintegration");
else:
        # Toggle between state values STANDBY (1) / ON (2)
        for powermode in range(1,3):
            actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Init',expectedresult,verifyList ={});
            print "IARMBUS_Init result: [%s]"%actualresult;
            #Check for return value of IARMBUS_Init
            if expectedresult in actualresult:
                #Calling "IARM_Bus_Connect"
                actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Connect',expectedresult,verifyList ={});
                print "IARMBUS_Connect result: [%s]"%actualresult;
                #Check for return value of IARMBUS_Connect
                if expectedresult in actualresult:
                        #Calling change_powermode
                        result = change_powermode(iarmObj,powermode);
                        print "Set PowerMode to %d: %s"%(powermode,result);

                        #Trickplay channel 2
                        streamId = '02'
                        result = dvrPlayUrl(tdkIntObj, kwargs={'play':'trickplay',"STREAMID":streamId})
                        print "Tuning to stream %s is [%s] with PowerMode=%d"%(streamId,result,powermode)

                        #Calling IARMBus_DisConnect API
                        actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_DisConnect',expectedresult,verifyList ={});
                        print "IARMBUS_DisConnect result: [%s]"%actualresult;
                #calling IARMBUS API "IARM_Bus_Term"
                actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Term',expectedresult,verifyList ={});
                print "IARMBUS_Term result: [%s]"%actualresult;
        #End of loop for powermode toggle
		
		#calling IARMBUS API "IARM_Bus_Init"
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Init', 'SUCCESS',verifyList ={});

        #calling IARMBUS API "IARM_Bus_Connect"
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});

        #Setting Power mode to ON
        change_powermode(iarmObj,2);

        #Calling IARM_Bus_DisConnect API
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});

        #calling IARMBUS API "IARM_Bus_Term"
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Term', 'SUCCESS',verifyList ={});
        #Unload modules
        iarmObj.unloadModule("iarmbus");
        tdkIntObj.unloadModule("tdkintegration");
