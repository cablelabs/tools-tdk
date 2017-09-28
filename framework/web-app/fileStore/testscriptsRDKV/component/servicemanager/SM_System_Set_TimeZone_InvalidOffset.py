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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>SM_System_Set_TimeZone_InvalidOffset</name>
  <primitive_test_id/>
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check if the time zone is changed when an invalid offset is given</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_138</test_case_id>
    <test_objective>To check whether the time zones are set when invalid offset is passed</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Xg1V3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Generic_CallMethod(const QString&amp; servicename,const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, 
Generic_CallMethod - system service , 
getTimeZoneDST
setTimeZoneDST
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "systemService" with ServiceManager component.
3.Set the api version as 11
4.Service_Manager_Agent will invoke the api setTimeZoneDST and getTimeZoneDST
5.Set one of the available timezone and check
6.TM will check the values and return SUCCESS/FAILURE status.
7. Service_Manager_Agent will deregister the given service from ServiceManager component</automation_approch>
    <except_output>Checkpoint 1.System service should register successfully
Checkpoint 2.Check the timezone is set properly.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_System_Set_TimeZone_InvalidOffset</test_script>
    <skipped>No</skipped>
    <release_version>M52</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script ^M
import tdklib; 
import servicemanager;

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");

#IP and Port of box, No need to change,^M
#This will be replaced with correspoing Box Ip and port while executing script^M
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_System_Set_TimeZone_InvalidOffset');

def setTimeZone(settimeZone):
    tdkTestObj1 = smObj.createTestStep('SM_Generic_CallMethod');
    expectedresult="FAILURE"
    methodName="setTimeZoneDST"
    tdkTestObj1.addParameter("service_name", serviceName);
    tdkTestObj1.addParameter("method_name", methodName);
    tdkTestObj1.addParameter("params",settimeZone);
    tdkTestObj1.addParameter("inputCount", 1);
    tdkTestObj1.executeTestCase(expectedresult);
    print "Calling method :",methodName
    actualresult = tdkTestObj1.getResult();
    print "EXPECTED RESULT: FAILURE";
    print "ACTUAL RESULT: ",actualresult; 
    if expectedresult in actualresult:
        tdkTestObj1.setResultStatus("SUCCESS");
        print methodName, "call does not set the invalid time zone" , settimeZone;
        methodDetail = tdkTestObj1.getResultDetails();
        print methodName, ": Details :" ,methodDetail;

    else:
        print methodName, "call sets the invalid time zone" , settimeZone;
        tdkTestObj1.setResultStatus("FAILURE");

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper():
    serviceName = "systemService";
    register = servicemanager.registerService(smObj,serviceName)
    if "SUCCESS" in register:
        tdkTestObj = smObj.createTestStep('SM_SetAPIVersion');
        expectedresult = "SUCCESS"
        apiVersion = 11;
        tdkTestObj.addParameter("apiVersion",apiVersion);
        tdkTestObj.addParameter("service_name",serviceName);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Set the API version %s succesfully" % apiVersion
        
            #Giving the input in the format "std offset dst [offset],start[/time],end[/time]" as per GNU specification
	    #Invalid hour
            settimeZone = "EST+25:12:34EDT+09:12:23,M10.1.2/+12,M12.3.4/+5"
	    setTimeZone(settimeZone)

	    #Invalid minute
	    settimeZone = "EST+12:67:13EDT+09:12:23,M10.1.2/+12,M12.3.4/+5"
	    setTimeZone(settimeZone)

	    #Invalid second
	    settimeZone = "EST+12:23:70EDT+09:12:23,M10.1.2/+12,M12.3.4/+5"
	    setTimeZone(settimeZone)

	else:
            print "Unable to set the API version"
            tdkTestObj.setResultStatus("FAILURE");

        #Unregister System service
        print "Unregistering the System Service"
        unregister = servicemanager.unRegisterService(smObj,serviceName);

    else:
        print "Unable to register the System service"

    #Unloading service manager module
    smObj.unloadModule("servicemanager");
else:
    print "Failed to load service manager module\n";
    #Set the module loading status
    smObj.setLoadModuleStatus("FAILURE");

