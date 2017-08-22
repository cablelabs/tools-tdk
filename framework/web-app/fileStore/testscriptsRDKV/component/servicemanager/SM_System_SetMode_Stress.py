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
  <name>SM_System_SetMode_Stress</name>
  <primitive_test_id/>
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test case is to set the mode of the STB multiple times</synopsis>
  <groups_id/>
  <execution_time>20</execution_time>
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
    <test_case_id>CT_Service Manager_121</test_case_id>
    <test_objective>To set different modes(NORMAL, EAS and WAREHOUSE) with different durations to perfor ma stress test on the STB using system service</test_objective>
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
4.Service_Manager_Agent will invoke the api setMode with mode as any of the EAS,NORMAL or WAREHOUSE and varying duration
5.Service_Manager_Agent will invoke the api getMode after duration time
6.Depending upon the return value of getMode api, SUCCESS/FAILURE status is returned
7. Service_Manager_Agent will deregister the given service from ServiceManager component</automation_approch>
    <except_output>Checkpoint 1.System service should register successfully
Checkpoint 2.Check the  mode set with setMode by getting it using getMode</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_System_SetMode_Stress</test_script>
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
smObj.configureTestCase(ip,port,'SM_System_SetMode_Stress');
iarmObj.configureTestCase(ip,port,'SM_System_SetMode_Stress');

#Function to set the mode with parameters as the mode to be set and duration for that mode
def setMode(timeDuration,mode):
    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
    paramValue = {"duration":timeDuration,"mode":mode}
    methodName="setMode"
    expectedresult = "SUCCESS"
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

    else:
        print methodName, " call is NOT successful with ",paramValue;
        tdkTestObj.setResultStatus("FAILURE");

#Function to get the mode with parameters as mode supposed to be set by setMode API and duration of it
def getMode(timeDuration,mode):
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
        if timeDuration > 0:
            if "NORMAL" in getModeValue:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Successfully switched to NORMAL mode"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Failed to switch to NORMAL mode"
	elif timeDuration < 0:
            if mode in getModeValue:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Successfully retained the", mode, " mode"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Failed to retain the", mode, " mode"
        else:
            if mode not in getModeValue:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS:", mode, " mode not set"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE:", mode, " mode set"
    else:
        print "getMode call is NOT successful";
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
                    print "Set the API version %s succesfully\n\n" % apiVersion

		    print "***********Set and Get Mode : 1***********"
		    inputDuration=20;
		    inputMode="EAS";
		    setMode(inputDuration,inputMode);
		    time.sleep(inputDuration);
		    getMode(inputDuration,inputMode);

		    print "\n\n***********Set and Get Mode : 2***********"
                    inputDuration=30;
                    inputMode="WAREHOUSE";
		    setMode(inputDuration,inputMode);
		    time.sleep(30);
		    getMode(inputDuration,inputMode);

		    print "\n\n***********Set and Get Mode : 3***********"
		    inputDuration=35;
		    inputMode="NORMAL";
		    setMode(inputDuration,inputMode);
		    time.sleep(inputDuration);
		    getMode(inputDuration,inputMode);

		    print "\n\n***********Set and Get Mode : 4***********"
		    inputDuration=-1;
		    inputMode="EAS";
		    setMode(inputDuration,inputMode);
		    time.sleep(10);
		    getMode(inputDuration,inputMode);

		    print "\n\n***********Set and Get Mode : 5***********"
		    inputDuration=-1;
		    inputMode="WAREHOUSE";
		    setMode(inputDuration,inputMode);
		    time.sleep(10);
		    getMode(inputDuration,inputMode);

                    print "\n\n***********Set and Get Mode : 6***********"
		    inputDuration=100;
		    inputMode="EAS";
		    setMode(inputDuration,inputMode);
		    time.sleep(inputDuration);
		    getMode(inputDuration,inputMode);

                    print "\n\n***********Set and Get Mode : 7***********"
		    inputDuration=0;
		    inputMode="WAREHOUSE";
		    setMode(inputDuration,inputMode);
		    time.sleep(60);
		    getMode(inputDuration,inputMode);

                    print "\n\n***********Set and Get Mode : 8***********"
		    inputDuration=100;
		    inputMode="WAREHOUSE";
		    setMode(inputDuration,inputMode);
		    time.sleep(inputDuration);
		    getMode(inputDuration,inputMode);

                    print "\n\n***********Set and Get Mode : 9***********"
		    inputDuration=10;
		    inputMode="NORMAL";
		    setMode(inputDuration,inputMode);
		    time.sleep(inputDuration);
		    getMode(inputDuration,inputMode);

                    print "\n\n***********Set and Get Mode : 10***********"
		    inputDuration=-2;
		    inputMode="EAS";
		    setMode(inputDuration,inputMode);
		    time.sleep(60);
		    getMode(inputDuration,inputMode);

                    print "\n\n***********Set and Get Mode : 11***********"
		    inputDuration=0;
		    inputMode="NORMAL";
		    setMode(inputDuration,inputMode);
		    time.sleep(60);
		    getMode(inputDuration,inputMode);

                    print "\n\n***********Set and Get Mode : 12***********"
		    inputDuration=80;
		    inputMode="WAREHOUSE";
		    setMode(inputDuration,inputMode);
		    time.sleep(inputDuration);
		    getMode(inputDuration,inputMode);

                    print "\n\n***********Set and Get Mode : 13***********"
		    inputDuration=-2;
		    inputMode="NORMAL";
		    setMode(inputDuration,inputMode);
		    time.sleep(60);
		    getMode(inputDuration,inputMode);

                    print "\n\n***********Set and Get Mode : 14***********"
		    inputDuration=0;
		    inputMode="EAS";
		    setMode(inputDuration,inputMode);
		    time.sleep(60);
		    getMode(inputDuration,inputMode);
		    
		    #Reverting to NORMAL
                    print "\n\n***********Set and Get Mode : 15***********"
		    inputDuration=30;
		    inputMode="NORMAL";
		    setMode(inputDuration,inputMode);
		    time.sleep(60);
		    getMode(inputDuration,inputMode);

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


		    
