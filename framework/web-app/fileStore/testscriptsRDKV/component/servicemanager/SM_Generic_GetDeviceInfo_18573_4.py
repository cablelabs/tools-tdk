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
  <name>SM_Generic_GetDeviceInfo_18573_4</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis></synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
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
    <box_type>Hybrid-5</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id></test_case_id>
    <test_objective></test_objective>
    <test_type></test_type>
    <test_setup></test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch></automation_approch>
    <except_output></except_output>
    <priority></priority>
    <test_stub_interface></test_stub_interface>
    <test_script></test_script>
    <skipped></skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import devicesettings;
import servicemanager;
#import getImageName;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

dsobj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
dsobj.configureTestCase(ip,port,'SM_WH_GetDeviceInfo_18573_4');

result = dsobj.getLoadModuleResult();
print "[Iarmbus module loading status]  :  %s" %result;
dsobj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
	#isDisplayConnected = "FALSE"
        #result = devicesettings.dsManagerInitialize(dsObj);
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        #if "SUCCESS" in result:
                #Check for display connection status
	#	isDisplayConnected = devicesettings.dsIsDisplayConnected(dsObj)
        #if "FALSE" == isDisplayConnected:
         #       result = devicesettings.dsManagerDeInitialize(dsObj)
          #      dsObj.unloadModule("devicesettings");
           #     print "\nPlease test with HDMI device connected. Exiting....!!!"
           #     exit()
           dsobj.setLoadModuleStatus("SUCCESS");
           #calling IARMBUS API "IARM_Bus_Init"
           tdkTestObj = dsobj.createTestStep('IARMBUS_Init');
           expectedresult="SUCCESS"
           tdkTestObj.executeTestCase(expectedresult);
           actualresult = tdkTestObj.getResult();
           details=tdkTestObj.getResultDetails();
           #Check for SUCCESS return value of IARMBUS_Init
           if ("SUCCESS" in actualresult):
               tdkTestObj.setResultStatus("SUCCESS");
               print "SUCCESS: Application successfully initialized with IARMBUS library";
               #calling IARMBUS API "IARM_Bus_Connect"
               tdkTestObj = dsobj.createTestStep('IARMBUS_Connect');
               expectedresult="SUCCESS"
               tdkTestObj.executeTestCase(expectedresult);
               actualresult = tdkTestObj.getResult();
               details=tdkTestObj.getResultDetails();
               #Check for SUCCESS return value of IARMBUS_Connect
               if expectedresult in actualresult:
                   tdkTestObj.setResultStatus("SUCCESS");
                   print "SUCCESS: Application successfully connected with IARMBUS ";
                   #Test component to be tested
                   obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");
                   obj.configureTestCase(ip,port,'SM_WH_GetDeviceInfo_18573_4');
                   #Get the result of connection with test component and STB
                   result =obj.getLoadModuleResult();
                   print "[LIB LOAD STATUS] : %s" %result;
                   if "SUCCESS" in result.upper():
                       #Set the module loading status
                       obj.setLoadModuleStatus("SUCCESS");

                       tdkTestObj = obj.createTestStep('SM_RegisterService');
                       expectedresult = "SUCCESS"
                       service_name = "Warehouse"
                       tdkTestObj.addParameter("service_name",service_name);
                       tdkTestObj.executeTestCase(expectedresult);
                       actualresult = tdkTestObj.getResult();
                       serviceDetail = tdkTestObj.getResultDetails();
                       print "[REGISTRATION DETAILS] : %s"%serviceDetail;
                       #Check for SUCCESS/FAILURE return value of SM_RegisterService
                       if expectedresult in actualresult:
                          tdkTestObj.setResultStatus("SUCCESS");
                          print "SUCCESS: Registered %s with serviceManager"%service_name
                          tdkTestObj = obj.createTestStep('SM_Generic_CallMethod');
                          expectedresult="SUCCESS"
                          tdkTestObj.addParameter("service_name", service_name);
                          tdkTestObj.addParameter("method_name", "getDeviceInfo");
                          tdkTestObj.executeTestCase(expectedresult);
                          actualresult = tdkTestObj.getResult();
                          serviceDetail = tdkTestObj.getResultDetails();
                          print "[TEST EXECUTION DETAILS]: %s"%serviceDetail;
                          if expectedresult in actualresult:
                              print "SUCCESS: getDeviceInfo successful";
                              tdkTestObj.setResultStatus("SUCCESS");
                          else:
                              print "FAILURE: getDeviceInfo failure";
                              tdkTestObj.setResultStatus("FAILURE");
                          #Call ServiceManger - UnregisterService API
                          tdkTestObj = obj.createTestStep('SM_UnRegisterService');
                          expectedresult="SUCCESS"
                          tdkTestObj.addParameter("service_name",service_name);
                          tdkTestObj.executeTestCase(expectedresult);
                          actualresult = tdkTestObj.getResult();
                          serviceDetail = tdkTestObj.getResultDetails();
                          print "[UNREGISTRATION DETAILS] : %s"%serviceDetail;
                #Check for SUCCESS/FAILURE return value of SM_UnRegisterService
                          if expectedresult in actualresult:
                              tdkTestObj.setResultStatus("SUCCESS");
                              print "SUCCESS: UnRegistered %s with serviceManager"%service_name
                          else:
                              tdkTestObj.setResultStatus("FAILURE");
                              print "FAILURE: Failed to unRegister service %s"%service_name
                       else:
                           tdkTestObj.setResultStatus("FAILURE");
                           print "FAILURE: Failed to register service %s"%service_name;
                       #Unload the servicemanager module
                       obj.unloadModule("servicemanager");
                   else:
                       print"Load module failed";
                       #Set the module loading status
                       obj.setLoadModuleStatus("FAILURE");
                   #calling IARMBUS API "IARM_Bus_Disconnect"
                   tdkTestObj = dsobj.createTestStep('IARMBUS_DisConnect');
                   expectedresult="SUCCESS"
                   tdkTestObj.executeTestCase(expectedresult);
                   actualresult = tdkTestObj.getResult();
                   details=tdkTestObj.getResultDetails();
                   #Check for SUCCESS/FAILURE return value of IARMBUS_DisConnect
                   if expectedresult in actualresult:
                       tdkTestObj.setResultStatus("SUCCESS");
                       print "SUCCESS: Application successfully disconnected from IARMBus";
                   else:
                       tdkTestObj.setResultStatus("FAILURE");
                       print "FAILURE: IARM_Bus_Disconnect failed. %s " %details;
               else:
                   tdkTestObj.setResultStatus("FAILURE");
                   print "FAILURE: IARM_Bus_Connect failed. %s" %details;
               #calling IARMBUS API "IARM_Bus_Term"
               tdkTestObj = dsobj.createTestStep('IARMBUS_Term');
               expectedresult="SUCCESS";
               tdkTestObj.executeTestCase(expectedresult);
               actualresult = tdkTestObj.getResult();
               details=tdkTestObj.getResultDetails();
               #Check for SUCCESS/FAILURE return value of IARMBUS_Term
               if expectedresult in actualresult:
                   tdkTestObj.setResultStatus("SUCCESS");
                   print "SUCCESS: IARM_Bus term success";
               else:
                   tdkTestObj.setResultStatus("FAILURE");
                   print "FAILURE: IARM_Bus Term failed";
                
           else:
               tdkTestObj.setResultStatus("FAILURE");
               print "FAILURE: IARM_Bus_Init failed. %s " %details;
           dsobj.unloadModule("iarmbus");
                
else:
        exit()



