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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_DisplaySettings_HDMI_HotplugEventDisconnected_BackToBack_16024_4</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_RunSMEvent_QtApp</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Invokes HotplugEventDisconnected event multiple times
  TestCase ID : CT_16024_4</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import servicemanager;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'SM_DisplaySettings_HDMI_HotplugEventDisconnected_BackToBack_16024_4');

#Get the result of connection with test component and STB
smLoadStatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %smLoadStatus;

#Set the module loading status
obj.setLoadModuleStatus(smLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper():
        tdkTestObj = obj.createTestStep('SM_RunSMEvent_QtApp');
	service_name = "org.openrdk.DisplaySettings"
	event_name = "connectedVideoDisplaysUpdated"
	event_param = 1;
        expectedresult = "SUCCESS";
	ret = servicemanager.RunSMEvent(obj, service_name, event_name, event_param);
        if expectedresult in ret:
                print "Successfully received HotplugEvent event"
                ret = servicemanager.RunSMEvent(obj, service_name, event_name, event_param);
                if expectedresult in ret:
                        print "SUCCESS: Application succesfully executed to verify event"
                else:
                        print "FAILURE: HotplugEvent event not recieved"
        else:
                print "QApp execution failed, HotplugEvent event not received";

        #Unload the modules
        obj.unloadModule("servicemanager");
else:
        print"Load module failed";
