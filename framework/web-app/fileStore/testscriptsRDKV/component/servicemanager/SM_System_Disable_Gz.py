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
  <name>SM_System_Disable_Gz</name>
  <primitive_test_id/>
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <primitive_test_version>7</primitive_test_version>
  <status>FREE</status>
  <synopsis>To disable GZ</synopsis>
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
    <test_case_id>CT_Service Manager_83</test_case_id>
    <test_objective>To disable the GZ using system service</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Generic_CallMethod(const QString&amp; servicename,const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, 
Generic_CallMethod - system service , getAvailableStandbyModes
setGzEnabled
isGzEnabled
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "systemService" with ServiceManager component.
3.Set the api version as 7
4.Service_Manager_Agent will invoke the api setGzEnabled,isGzEnabled
5.Get the existing GZ value then disable the GZ
6.Get the GZ state and revert the value. 
7.TM will check the values and return SUCCESS/FAILURE status.
8. Service_Manager_Agent will deregister the given service from ServiceManager component</automation_approch>
    <except_output>Checkpoint 1.System service should register successfully
Checkpoint 2.Check the GZ value as False</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_System_Disable_Gz</test_script>
    <skipped>No</skipped>
    <release_version/>
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
smObj.configureTestCase(ip,port,'SM_System_Disable_Gz');

def revertGzValue(gzValue):
    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
    methodName="setGzEnabled";
    valueToSetEnabled=gzValue;
    tdkTestObj.addParameter("service_name", serviceName);
    tdkTestObj.addParameter("method_name", methodName);
    tdkTestObj.addParameter("params", valueToSetEnabled);
    tdkTestObj.addParameter("inputCount", 1);
    tdkTestObj.executeTestCase(expectedresult);
    print "Calling method :",methodName
    actualresult = tdkTestObj.getResult();

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print methodName, "call is successful with parameter" , gzValue;
        methodDetail = tdkTestObj.getResultDetails();
        print methodName, ": Details :" ,methodDetail
        print "GZ value is successfully reverted"
    else:
       tdkTestObj.setResultStatus("FAILURE");
       print methodName, "call is NOT successful with parameter" , gzValue;
       print "Unable to revert GZ value"

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[service manager LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper():
    serviceName = "systemService";
    register = servicemanager.registerService(smObj,serviceName)
    if "SUCCESS" in register:
        tdkTestObj = smObj.createTestStep('SM_SetAPIVersion');
        expectedresult = "SUCCESS"
        apiVersion = 5;
        tdkTestObj.addParameter("apiVersion",apiVersion);
        tdkTestObj.addParameter("service_name",serviceName);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Set the API version %s succesfully" % apiVersion
            tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
            methodName="isGzEnabled";
            tdkTestObj.addParameter("service_name", serviceName);
            tdkTestObj.addParameter("method_name", methodName);
            tdkTestObj.executeTestCase(expectedresult);
            print "Calling method :",methodName, "before disabling GZ"
            actualresult = tdkTestObj.getResult();

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print methodName, "call is successful";
                gzValue = tdkTestObj.getResultDetails();
                print methodName, ": Details :" ,gzValue
                print "GZ value before disabling is" , gzValue
                #Disable GZ 
                tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                methodName="setGzEnabled";
                valueToSetEnabled=False;
                tdkTestObj.addParameter("service_name", serviceName);
                tdkTestObj.addParameter("method_name", methodName);
                tdkTestObj.addParameter("params", valueToSetEnabled);
                tdkTestObj.addParameter("inputCount", 1);
                tdkTestObj.executeTestCase(expectedresult);
                print "Calling method :",methodName , "with parameter" , valueToSetEnabled
                actualresult = tdkTestObj.getResult();

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print methodName, "call is successfull " "with parameter" , valueToSetEnabled; 
                    methodDetail = tdkTestObj.getResultDetails();
                    print methodName, ": Details :" ,methodDetail
  
                    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                    methodName="isGzEnabled";
                    tdkTestObj.addParameter("service_name", serviceName);
                    tdkTestObj.addParameter("method_name", methodName);
                    tdkTestObj.executeTestCase(expectedresult);
                    print "Calling method :",methodName
                    actualresult = tdkTestObj.getResult();

                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print methodName, "call is successful";
                        gzNewValue = tdkTestObj.getResultDetails();
                        print methodName, ": Details :" ,gzNewValue
                        if gzNewValue == "false":
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Successfully disabled GZ"

                            if gzValue != gzNewValue:
                                #Revert the GZ value
                                print "Reverting the GZ value with " , gzValue
                                revertGzValue(gzValue)
                            else:
                                pass;
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "GZ is not disabled"
                    else:
                        print methodName, "call is NOT successful";
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print methodName, "call is NOT successful";
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

    else:
        print "Unable to register the System service"

    #Unloading service manager module
    smObj.unloadModule("servicemanager");
else:
    print "Failed to load service manager module\n"; 
    #Set the module loading status
    smObj.setLoadModuleStatus("FAILURE");
