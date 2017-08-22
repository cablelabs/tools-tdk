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
  <name>SM_System_SetandGet_WAREHOUSE_NegativeDuration</name>
  <primitive_test_id/>
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To set WAREHOUSE mode with negative duration and verify that the mode is retained</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>CT_Service Manager_119</test_case_id>
    <test_objective>To set WAREHOUSE mode with negative duration and to verify that the mode is retained using system service</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Generic_CallMethod(const QString&amp; servicename,const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, 
Generic_CallMethod - system service , setMode, getMode
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "systemService" with ServiceManager component.
3.Set the api version as 6
4.Service_Manager_Agent will invoke the api setMode with mode as WAREHOUSE and duration as a negative value
5.Service_Manager_Agent will invoke the api getMode after duration time and verify that the mode is retained 
6.Depending upon the return value of getMode api, SUCCESS/FAILURE status is returned
7. Service_Manager_Agent will deregister the given service from ServiceManager component</automation_approch>
    <except_output>Checkpoint 1.System service should register successfully
Checkpoint 2.Check the  mode set with setMode by getting it using getMode</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_System_SetandGet_WAREHOUSE_NegativeDuration</test_script>
    <skipped>No</skipped>
    <release_version>M51</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import servicemanager;
import iarmbus;
import time;


#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");


#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_System_SetandGet_WAREHOUSE_NegativeDuration');
iarmObj.configureTestCase(ip,port,'SM_System_SetandGet_WAREHOUSE_NegativeDuration');

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[service manager LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus.upper());

iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[iarmbus LIB LOAD STATUS]  :  %s" %iarmLoadStatus;
iarmObj.setLoadModuleStatus(iarmLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper() and "SUCCESS" in iarmLoadStatus.upper():
    #Calling IARM Bus Init
    init=iarmbus.IARMBUS_Init(iarmObj,'SUCCESS')
    if "SUCCESS" in init:
        connect=iarmbus.IARMBUS_Connect(iarmObj,'SUCCESS')
        if "SUCCESS" in connect:
            serviceName = "systemService";
            #Register the system service
            register = servicemanager.registerService(smObj,serviceName)
            if "SUCCESS" in register:
                tdkTestObj = smObj.createTestStep('SM_SetAPIVersion');
                expectedresult = "SUCCESS"
                apiVersion =6;
                tdkTestObj.addParameter("apiVersion",apiVersion);
                tdkTestObj.addParameter("service_name",serviceName);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Set the API version %s succesfully" % apiVersion
                    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                    paramValue = {"duration":-1,"mode":"WAREHOUSE"}
                    methodName="setMode"
                    tdkTestObj.addParameter("service_name", serviceName);
                    tdkTestObj.addParameter("method_name", methodName);
                    tdkTestObj.addParameter("params", paramValue);
                    tdkTestObj.addParameter("inputCount", 1);
                    tdkTestObj.executeTestCase(expectedresult);
                    print "Calling method :",methodName
                    actualresult = tdkTestObj.getResult();
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print methodName, " call is successful with" ,paramValue;
                        methodDetail = tdkTestObj.getResultDetails();
                        print methodName, ": Details :" ,methodDetail

                        #Get the currently set mode
                        tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                        expectedresult="SUCCESS"
                        methodName="getMode"
                        tdkTestObj.addParameter("service_name", serviceName);
                        tdkTestObj.addParameter("method_name", methodName);
                        tdkTestObj.executeTestCase(expectedresult);
                        print "Calling method :",methodName
                        actualresult = tdkTestObj.getResult();
                        if expectedresult in actualresult:
                            getModeValue = tdkTestObj.getResultDetails();
                            print "GetMode : Details :" ,getModeValue
                            if "WAREHOUSE" in getModeValue:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Successfully set to WAREHOUSE mode"

                                #sleep for duration time
                                time.sleep(20);

                                tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                                expectedresult="SUCCESS"
                                methodName="getMode"
                                tdkTestObj.addParameter("service_name", serviceName);
                                tdkTestObj.addParameter("method_name", methodName);
                                tdkTestObj.executeTestCase(expectedresult);
                                print "Calling method :",methodName
                                actualresult = tdkTestObj.getResult();
                                if expectedresult in actualresult:
                                    getModeValue = tdkTestObj.getResultDetails();
                                    print "GetMode : Details :" ,getModeValue
                                    if "WAREHOUSE" in getModeValue:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Successfully retains the WAREHOUSE mode"
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Failed to retain the WAREHOUSE mode"

                                    #Reverting the mode to NORMAL
                                    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                                    paramValue = {"duration":0,"mode":"NORMAL"}
                                    methodName="setMode"
                                    expectedresult="SUCCESS"
                                    tdkTestObj.addParameter("service_name", serviceName);
                                    tdkTestObj.addParameter("method_name", methodName);
                                    tdkTestObj.addParameter("params", paramValue);
                                    tdkTestObj.addParameter("inputCount", 1);
                                    tdkTestObj.executeTestCase(expectedresult);
                                    print "Calling method :",methodName
                                    actualresult = tdkTestObj.getResult();

                                    if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print methodName, " call is successful with" ,paramValue;
                                        methodDetail = tdkTestObj.getResultDetails();
                                        print methodName, ": Details :" ,methodDetail

                                        #Get the currently set mode
                                        tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                                        expectedresult="SUCCESS"
                                        methodName="getMode"
                                        tdkTestObj.addParameter("service_name", serviceName);
                                        tdkTestObj.addParameter("method_name", methodName);
                                        tdkTestObj.executeTestCase(expectedresult);
                                        print "Calling method :",methodName
                                        actualresult = tdkTestObj.getResult();
                                        if expectedresult in actualresult:
                                            getModeValue = tdkTestObj.getResultDetails();
                                            print "GetMode : Details :" ,getModeValue
                                            if "NORMAL" in getModeValue:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Successfully reverted to the NORMAL mode"
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Unable to revert to the NORMAL mode"
                                        else:
                                            print "getMode call is NOT successful";
                                            tdkTestObj.setResultStatus("FAILURE");
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print methodName, "call is NOT successful with ",paramValue;

                                else:
                                    print "getMode call is NOT successful";
                                    tdkTestObj.setResultStatus("FAILURE");

                            else:
                                print methodName, "could not set WAREHOUSE mode";
                                tdkTestObj.setResultStatus("FAILURE");

                        else:
                            print "getMode call is NOT successful";
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        print methodName, " call is NOT successful with ",paramValue;
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Unable to set the API Version " , apiVersion

                #Unregister System service
                print "Unregistering the System Service"
                unregister = servicemanager.unRegisterService(smObj,serviceName);

                #Calling IARM_Bus_DisConnect API
                disconnect=iarmbus.IARMBUS_DisConnect(iarmObj,'SUCCESS')
                term=iarmbus.IARMBUS_Term(iarmObj,'SUCCESS')

            else:
                print "Unable to register the System service"
            #Unloading service manager module
            smObj.unloadModule("servicemanager");
            #Unloading iarmbus module
            iarmObj.unloadModule("iarmbus");
else:
    print "Failed to load service manager module\n";
    #Set the module loading status^M
    smObj.setLoadModuleStatus("FAILURE");
    iarmObj.setLoadModuleStatus("FAILURE");

