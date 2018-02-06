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
  <name>SM_FP_setbrightness_neg_2424</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_FP_SetBrightness</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>SM_FP_setbrightness_negative value
RDK-2424</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# This will not test the actual functionality of setbrightnessSettings API.Because this API is
# not yet implemented in servicemanager components itself.

#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import devicesettings;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");
dsobj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'SM_FP_setbrightness_neg_2424');
dsobj.configureTestCase(ip,port,'SM_FP_setbrightness_neg_2424');
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =dsobj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        dsobj.setLoadModuleStatus("SUCCESS");
        result = devicesettings.dsManagerInitialize(dsobj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result.upper():
                    #calling ServiceManger - registerService API
                    tdkTestObj = obj.createTestStep('SM_RegisterService');
                    expectedresult="SUCCESS"
                    serviceName="FrontPanelService";
                    tdkTestObj.addParameter("service_name",serviceName);
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    #Check for SUCCESS/FAILURE return value of SM_RegisterService
                    if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "SUCCESS :Application successfully registered a service with serviceManger";
                            tdkTestObj = obj.createTestStep('SM_FP_SetAPIVersion');
                            expectedresult="SUCCESS"
                            apiVersion=5;
                            tdkTestObj.addParameter("apiVersion",apiVersion);
                            
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            apiversiondetail =tdkTestObj.getResultDetails();
                            print "[EXECUTION DETAILS] APi Version : %s"%apiversiondetail;
                            print "Registered Service:%s" %serviceName;
                            tdkTestObj = obj.createTestStep('SM_FP_SetBrightness');
                            expectedresult="FAILURE"
                            setbrightness = -20;
                            tdkTestObj.addParameter("LEDBrightness",setbrightness);
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult= tdkTestObj.getResult();
                            brightnessdetails= tdkTestObj.getResultDetails();
                            #Check for SUCCESS/FAILURE return value of SM_DisplaySetting_SetbrightnessSettings
                            if expectedresult in actualresult:
                                    print "SUCCESS: Application failed to set negative value for SM_FP_SetBrightness API";
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print brightnessdetails;
                            else:
                                    tdkTestObj = obj.createTestStep('SM_FP_GetBrightness');
                                    expectedresult="SUCCESS"
                                    
                                    tdkTestObj.executeTestCase(expectedresult);
                                    actualresult= tdkTestObj.getResult();
                                    brightnessdetails= tdkTestObj.getResultDetails();
                                    #Check for SUCCESS/FAILURE return value of SM_DisplaySetting_SetbrightnessSettings
                                    if expectedresult in actualresult and str(setbrightness) in brightnessdetails:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "FAILURE: Application succesfully executes SM_FP_GetBrightness API";
                                            print brightnessdetails;
                                    else:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "SUCCESS: Application Failed to execute SM_FP_GetBrightness API";
                                    print "FAILURE: Application successfully  executed SM_FP_SetBrightness API for negative value";
                            # calling SM_UnRegisterService to unregister service
                            tdkTestObj = obj.createTestStep('SM_UnRegisterService');
                            expectedresult="SUCCESS"
                            tdkTestObj.addParameter("service_name",serviceName);
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            #Check for SUCCESS/FAILURE return value of SM_UnRegisterService
                            if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "SUCCESS :Application successfully unRegisteres a service";
                            else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "FAILURE: Failed to unRegister the service" ;
                    else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "FAILURE: Application failed to register a service";
          

                    result = devicesettings.dsManagerDeInitialize(dsobj)
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the servicemanager module
        obj.unloadModule("servicemanager");
        dsobj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
        dsobj.setLoadModuleStatus("FAILURE");
				
