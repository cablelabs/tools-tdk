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
  <id>1590</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check the Resolution value sets by device settings component after and before reboots the STB while playing the video.	E2E_LinearTV_13</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
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
import devicesettings;

#Test component to be tested
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
dev_obj = tdklib.TDKScriptingLibrary("devicesettings","2.0");    

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback');
dev_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = dev_obj.getLoadModuleResult();

print "[tdkintegration LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
print "[devicesettings LIB LOAD STATUS]  :  %s" %loadmodulestatus1 ;
loadmoduledetails = tdk_obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdk_obj.initiateReboot();
                dev_obj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback');
                #Get the result of connection with test component and STB
                loadmodulestatus =tdk_obj.getLoadModuleResult();
                loadmodulestatus1 = dev_obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    dev_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");    

    displayStatus = "FALSE"
    #calling DS_ManagerInitialize to check Intialize API.
    actualresult = devicesettings.dsManagerInitialize(dev_obj)

    #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
    if "SUCCESS" in actualresult:
        #Calling DS_IsDisplayConnectedStatus function to check for display connection status
        displayStatus = devicesettings.dsIsDisplayConnected(dev_obj)
        if "TRUE" in displayStatus:

		actualresult,dsTdkObj,supportedResolutions = tdklib.Create_ExecuteTestcase(dev_obj,'DS_Resolution', 'SUCCESS',verifyList ={}, port_name = "HDMI0");

		print "Get current resolution"
		copyResolution = devicesettings.dsGetResolution(dev_obj,"SUCCESS",kwargs={'portName':"HDMI0"});
        	#Set resolution value to 720p
        	setresolution="720p";
        	#Check if current value is already 720p
		if setresolution not in supportedResolutions:
			print setresolution, " Resolution not supported"
		elif setresolution in copyResolution:
			print "Resolution value already at ",copyResolution
			#Calling the getURL_PlayURL to get the URL and playback
                	result = getURL_PlayURL(tdk_obj,'01');
                	if "SUCCESS" in result:
                    		print "Sucessfully executed the getURL_PlayURL function"
                	else:
                    		print "Failure: getURL_PlayURL function"
        	else:
			devicesettings.dsSetResolution(dev_obj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':setresolution});
                        #Calling the getURL_PlayURL to get the URL and playback
                        result = getURL_PlayURL(tdk_obj,'01');
                        if "SUCCESS" in result:
                                print "Sucessfully executed the getURL_PlayURL function"
                        else:
                                print "Failure: getURL_PlayURL function"
        #calling DS_ManagerDeInitialize to DeInitialize API
	result = devicesettings.dsManagerDeInitialize(dev_obj)

    #unloading the module
    tdk_obj.unloadModule("tdkintegration");

    if "TRUE" in displayStatus:
    	dev_obj.initiateReboot();
    	dev_obj.resetConnectionAfterReboot();

    	print "#--------------------------------------After Reboot--------------------------------------#";

	setresolution="720p";	

    	#calling DS_ManagerInitialize to check Intialize API.
    	actualresult = devicesettings.dsManagerInitialize(dev_obj)
    	if "SUCCESS" in actualresult:
		actualresult,tdkObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_SetResolution', 'SUCCESS', verifyList = {'resolution':setresolution},resolution = setresolution, port_name = "HDMI0",get_only = 1);
        	#calling DS_ManagerDeInitialize to DeInitialize API
		result = devicesettings.dsManagerDeInitialize(dev_obj)

    #Unload the modules
    dev_obj.unloadModule("devicesettings");
else:
    print"Load module failed";
    #Set the module loading status
    dev_obj.setLoadModuleStatus("FAILURE");
    tdk_obj.setLoadModuleStatus("FAILURE");
