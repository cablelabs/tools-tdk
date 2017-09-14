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
  <name>SM_System_SetandGet_Multiple_TimeZones</name>
  <primitive_test_id/>
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <primitive_test_version>7</primitive_test_version>
  <status>FREE</status>
  <synopsis>To set and get multiple time zones</synopsis>
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
    <test_case_id>CT_Service Manager_89</test_case_id>
    <test_objective>To check whether available time zones are set and get successfully.</test_objective>
    <test_type>Positive</test_type>
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
5.Set some of the available timezone and check
6.TM will check the values and return SUCCESS/FAILURE status.
7. Service_Manager_Agent will deregister the given service from ServiceManager component</automation_approch>
    <except_output>Checkpoint 1.System service should register successfully
Checkpoint 2.Check the timezones are set properly.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_System_SetandGet_Multiple_TimeZones</test_script>
    <skipped>No</skipped>
    <release_version>M50</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import servicemanager;

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_System_SetandGet_Multiple_TimeZones');

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus.upper());


def setandgetTimeZone(settimeZone):
    tdkTestObj1 = smObj.createTestStep('SM_Generic_CallMethod');
    expectedresult="SUCCESS"
    methodName="setTimeZoneDST"
    tdkTestObj1.addParameter("service_name", serviceName);
    tdkTestObj1.addParameter("method_name", methodName);
    tdkTestObj1.addParameter("params",settimeZone);
    tdkTestObj1.addParameter("inputCount", 1);
    tdkTestObj1.executeTestCase(expectedresult);
    print "Calling method :",methodName
    actualresult = tdkTestObj1.getResult();

    if expectedresult in actualresult:
        tdkTestObj1.setResultStatus("SUCCESS");
        print methodName, "call is successful with parameter" , settimeZone;
        methodDetail = tdkTestObj1.getResultDetails();
        print methodName, ": Details :" ,methodDetail

        getTimeZone();

    else:
        print methodName, "call is NOT successful with parameter" , settimeZone;
        tdkTestObj1.setResultStatus("FAILURE");


def getTimeZone():
    #Getting the time zone
    tdkTestObj2 = smObj.createTestStep('SM_Generic_CallMethod');
    expectedresult="SUCCESS"
    methodName="getTimeZoneDST"
    tdkTestObj2.addParameter("service_name", serviceName);
    tdkTestObj2.addParameter("method_name", methodName);
    tdkTestObj2.executeTestCase(expectedresult);
    print "Calling method :",methodName
    actualresult = tdkTestObj2.getResult();

    if expectedresult in actualresult:
        tdkTestObj2.setResultStatus("SUCCESS");
        print methodName, "call is successful";
        methodDetail = tdkTestObj2.getResultDetails();
        print methodName, ": Details :" ,methodDetail
        gettimeZone = methodDetail.replace("\\","");
        if gettimeZone == settimeZone:
            tdkTestObj2.setResultStatus("SUCCESS");
            print "Successfully gets the time zone as " ,gettimeZone
        else:
            print "Unable to get time zone as " , gettimeZone,
            tdkTestObj2.setResultStatus("FAILURE");
    else:
        print methodName, "call is NOT successful";
        tdkTestObj2.setResultStatus("FAILURE");

           

if "SUCCESS" in smLoadStatus.upper():
    serviceName = "systemService";
    print "going to register"
    register = servicemanager.registerService(smObj,serviceName)
    if "SUCCESS" in register:
        tdkTestObj3 = smObj.createTestStep('SM_SetAPIVersion');
        expectedresult = "SUCCESS"
        apiVersion = 11;
        tdkTestObj3.addParameter("apiVersion",apiVersion);
        tdkTestObj3.addParameter("service_name",serviceName);
        tdkTestObj3.executeTestCase(expectedresult);
        actualresult = tdkTestObj3.getResult();
        if expectedresult in actualresult:
            print "Set the API version %s succesfully" % apiVersion

	    #Giving the input in the format "std offset" as per GNU specification
            settimeZone="EST+5:30:12"
            setandgetTimeZone(settimeZone);         
         
	    #Giving the input in the format "std offset dst [offset],start[/time],end[/time]" as per GNU specification
	    #DST Start and End in "Mm.w.d" format
            settimeZone="EST+12EDT+09:12:23,M10.1.2/+12,M12.3.4/+5"
            setandgetTimeZone(settimeZone);
          
	    #Giving the input in the format "std offset dst [offset],start[/time],end[/time]" as per GNU specification
	    #DST Start and End in "Jn" and "Mm.w.d" format
            settimeZone="IST-2IDT+00:00:00,J234/+26,M10.5.0/-12"
            setandgetTimeZone(settimeZone);
     
	    #Giving the input in the format "std offset dst [offset],start[/time],end[/time]" as per GNU specification
	    #DST Start and End in "n" format
            settimeZone="IST-24IDT+12:34:56,124/+10,237/+167"
            setandgetTimeZone(settimeZone);
       
        else:
            print "Unable to set the API version"
            tdkTestObj3.setResultStatus("FAILURE");

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

