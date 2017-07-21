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
  <name>SM_System_Default_Preferred_Standby_Mode</name>
  <primitive_test_id/>
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <primitive_test_version>7</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check whether default  standby mode is getting set or not</synopsis>
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
    <test_case_id>CT_Service Manager_76</test_case_id>
    <test_objective>To check whether when preferred standby mode is empty it should set with first element in the available standby modes</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Generic_CallMethod(const QString&amp; servicename,const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, 
Generic_CallMethod - system service ,
getPreferredStandbyMode
setPreferredStandbyMode
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "systemService" with ServiceManager component.
3.Set the api version as 7
4.Service_Manager_Agent will invoke the api getPreferredStandbyMode,setPowerState
5.If getPreferredStandbyMode returns empty then set power state as STANDBY
6.TM will check the values and return SUCCESS/FAILURE status.
7. Service_Manager_Agent will deregister the given service from ServiceManager component</automation_approch>
    <except_output>Checkpoint 1.System service should register successfully
Checkpoint 2.If getPreferredStandbyMode returns empty standby mode should set with first element in the available standby modes</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_System_Default_Preferred_Standby_Mode</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import servicemanager;
import iarmbus;

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_System_Default_Preferred_Standby_Mode');
iarmObj.configureTestCase(ip,port,'SM_System_Default_Preferred_Standby_Mode');

def setPowerStateOn():
    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
    expectedresult="SUCCESS"
    methodName="setPowerState"
    powerState="ON"
    tdkTestObj.addParameter("service_name", serviceName);
    tdkTestObj.addParameter("method_name", methodName);
    tdkTestObj.addParameter("params",powerState);
    tdkTestObj.addParameter("inputCount", 1);
    tdkTestObj.executeTestCase(expectedresult);
    print "Calling method :",methodName
    actualresult = tdkTestObj.getResult();

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print methodName, "call is successful with parameter" , powerState;
        methodDetail = tdkTestObj.getResultDetails();
        print methodName, ": Details :" ,methodDetail
    else:
        print methodName, "call is NOT successful with parameter" , powerState;
        tdkTestObj.setResultStatus("FAILURE");

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
            register = servicemanager.registerService(smObj,serviceName)
            if "SUCCESS" in register:
                tdkTestObj = smObj.createTestStep('SM_SetAPIVersion');
                expectedresult = "SUCCESS"
                apiVersion = 7;
                tdkTestObj.addParameter("apiVersion",apiVersion);
                tdkTestObj.addParameter("service_name",serviceName);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Set the API version %s succesfully" % apiVersion
                    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                    methodName="getPreferredStandbyMode"
                    tdkTestObj.addParameter("service_name", serviceName);
                    tdkTestObj.addParameter("method_name", methodName);
                    tdkTestObj.executeTestCase(expectedresult);
                    print "Calling method :",methodName
                    actualresult = tdkTestObj.getResult();

                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print methodName, "call is successful";
                        methodDetail = tdkTestObj.getResultDetails();
                        print methodName, ": Details :" ,methodDetail
                        #check Preferred Standby Mode is empty or not
                        if not methodDetail:
                            print "Preferred Standby Mode is empty"
                            tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                            expectedresult="SUCCESS"
                            methodName="getAvailableStandbyModes"
                            tdkTestObj.addParameter("service_name", serviceName);
                            tdkTestObj.addParameter("method_name", methodName);
                            tdkTestObj.executeTestCase(expectedresult);
                            print "Calling method :",methodName
                            actualresult = tdkTestObj.getResult();

                            if expectedresult in actualresult:
                                print methodName, "call is successful";
                                standbyModes = tdkTestObj.getResultDetails();
                                print methodName, ": Details :" , standbyModes
                                standbyModes = json.loads(standbyModes);

                                tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                                expectedresult="SUCCESS"
                                methodName="setPowerState"
                                powerState="STANDBY"
                                tdkTestObj.addParameter("service_name", serviceName);
                                tdkTestObj.addParameter("method_name", methodName);
                                tdkTestObj.addParameter("params",powerState);
                                tdkTestObj.addParameter("inputCount", 1);
                                tdkTestObj.executeTestCase(expectedresult);
                                print "Calling method :",methodName
                                actualresult = tdkTestObj.getResult();

                                if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print methodName, "call is successful with parameter" , powerState;
                                    methodDetail = tdkTestObj.getResultDetails();
                                    print methodName, ": Details :" ,methodDetail
                                    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                                    methodName="getPreferredStandbyMode"
                                    tdkTestObj.addParameter("service_name", serviceName);
                                    tdkTestObj.addParameter("method_name", methodName);
                                    tdkTestObj.executeTestCase(expectedresult);
                                    print "Calling method :",methodName
                                    actualresult = tdkTestObj.getResult();

                                    if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print methodName, "call is successful";
                                        methodDetail = tdkTestObj.getResultDetails();
                                        print methodName, ": Details :" ,methodDetail 
                                        if methodDetail == standbyModes[0]:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "Standby mode is set by the  first element in getAvailableStandbyModes"
                                            print "Reverting the power state as ON"
                                            setPowerStateOn()
                                        else:
                                           print "Standby mode is NOT set by the  first element in getAvailableStandbyModes"
                                           tdkTestObj.setResultStatus("FAILURE");
                                    else:
                                       print methodName, "call is NOT successful";
                                       tdkTestObj.setResultStatus("FAILURE");
                                else:
                                    print methodName, "call is NOT successful with parameter" , powerState;
                                    tdkTestObj.setResultStatus("FAILURE");
                        else:
                            print "Preferred Standby Mode is NOT empty"
                            tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                            expectedresult="SUCCESS"
                            methodName="setPowerState"
                            powerState="STANDBY"
                            tdkTestObj.addParameter("service_name", serviceName);
                            tdkTestObj.addParameter("method_name", methodName);
                            tdkTestObj.addParameter("params",powerState);
                            tdkTestObj.addParameter("inputCount", 1);
                            tdkTestObj.executeTestCase(expectedresult);
                            print "Calling method :",methodName
                            actualresult = tdkTestObj.getResult();

                            if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print methodName, "call is successful with parameter" , powerState;
                                methodDetail = tdkTestObj.getResultDetails();
                                print methodName, ": Details :" ,methodDetail
                             
                                tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                                methodName="getPowerState"
                                tdkTestObj.addParameter("service_name", serviceName);
                                tdkTestObj.addParameter("method_name", methodName);
                                tdkTestObj.executeTestCase(expectedresult);
                                print "Calling method :",methodName
                                actualresult = tdkTestObj.getResult();
   
                                if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print methodName, "call is successful";
                                    methodDetail = tdkTestObj.getResultDetails();
                                    print methodName, ": Details :" ,methodDetail
                                    if powerState==methodDetail:
                                        print "Successfully power state is set as ",powerState
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Reverting the power state as ON"
                                        setPowerStateOn()
                                    else:
                                        print "Power state is NOT set as ",powerState
                                        tdkTestObj.setResultStatus("FAILURE");
                                else:
                                    print methodName, "call is NOT successful";
                                    tdkTestObj.setResultStatus("FAILURE");
                            else:
                                print methodName, "call is NOT successful with parameter" , powerState;
                                tdkTestObj.setResultStatus("FAILURE");
                    else:
                        print methodName, "call is NOT successful";
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
    #Set the module loading status
    smObj.setLoadModuleStatus("FAILURE");
    iarmObj.setLoadModuleStatus("FAILURE");
