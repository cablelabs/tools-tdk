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
  <id>1581</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check the DS set Mute while live playback and sets the power state of STB using DS.	E2E_LinearTV_16</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
from tdkintegration import getURL_PlayURL;
from iarmbus import change_powermode

#Test component to be tested
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
dev_obj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
iarm_obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback');
dev_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback');
iarm_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = dev_obj.getLoadModuleResult();
loadmodulestatus2 = iarm_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1 ;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus2 ;
loadmoduledetails = tdk_obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdk_obj.initiateReboot();
                dev_obj.resetConnectionAfterReboot();
                iarm_obj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback');
                #Get the result of connection with test component and STB
                loadmodulestatus =tdk_obj.getLoadModuleResult();
                loadmodulestatus1 = dev_obj.getLoadModuleResult();
                loadmodulestatus2 = iarm_obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()) and ("SUCCESS" in loadmodulestatus2.upper()):
    #Set the module loading status
    dev_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");
    iarm_obj.setLoadModuleStatus("SUCCESS");

    #calling getURL_PlayURL to get and play the URL
    result = getURL_PlayURL(tdk_obj,'01');                
    
    if "SUCCESS" in result:     
                
        #calling DS_ManagerInitialize to check Intialize API.
        actualresult,tdkTestObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_ManagerInitialize', 'SUCCESS',verifyList ={});
                
        mutestatus=0;
        print "Port name value set to:%s" %mutestatus;                               
                
        portname = "HDMI0";                
        print "Port name value set to:%s" %portname;

        powermode=0;
        print "Power Mode value set to %s" %powermode;
                
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in actualresult:
            
            #calling DS_MuteStatus to check audio mute for a port.
            actualresult,tdkTestObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_MuteStatus', 'SUCCESS',verifyList = {'mute_status':str(mutestatus)},port_name = portname, mute_status = mutestatus);                    
            if "SUCCESS" in actualresult:
                
                #calling DS_SetPowerMode to set the power mode of STB
                change_powermode(iarm_obj,2);                        

            #calling DS_ManagerDeInitialize to DeInitialize API
            actualresult,tdkTestObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_ManagerDeInitialize', 'SUCCESS',verifyList ={});                                    
                            

        else:
            print "FAILURE :DS Manager Intialize";    
              
    else:                
        print "FAILURE: getURL_PlayURL function";               
        
        
    #Unload the deviceSettings module
    dev_obj.unloadModule("devicesettings");
    tdk_obj.unloadModule("tdkintegration");
    iarm_obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        dev_obj.setLoadModuleStatus("FAILURE");
        iarm_obj.setLoadModuleStatus("FAILURE");
        tdk_obj.setLoadModuleStatus("FAILURE");

