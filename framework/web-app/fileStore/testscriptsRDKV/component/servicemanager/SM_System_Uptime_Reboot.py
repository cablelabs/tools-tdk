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
  <version>2</version>
  <name>SM_System_Uptime_Reboot</name>
  <primitive_test_id/>
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <primitive_test_version>7</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check the  system up time before and after reboot</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <test_case_id>CT_Service Manager_72</test_case_id>
    <test_objective>To check whether system up time changes after reboot</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Generic_CallMethod(const QString&amp; servicename,const QString&amp; method,const ServiceParams&amp; params)
ExecuteCmd
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, 
Generic_CallMethod - system service , requestSystemUptime
ExecuteCmd - Command
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "systemService" with ServiceManager component.
3.Service_Manager_Agent will invoke the api requestSystemUptime to get the uptime
4.Reboot the box and Verify the uptime with the system command
5.TM will check if the values are same and return SUCCESS/FAILURE status.
6.Service_Manager_Agent will deregister the given service from ServiceManager component</automation_approch>
    <except_output>Checkpoint 1.System service should register successfully
Checkpoint 2.After reboot Check the  value retrieved using requestSystemUptime  api and system command</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_System_Uptime_Reboot</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags/>
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
smObj.configureTestCase(ip,port,'SM_System_Uptime_Reboot');

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper():
        serviceName = "systemService";
        register = servicemanager.registerService(smObj,serviceName)
        if "SUCCESS" in register:
            tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
            expectedresult="SUCCESS"
            methodName="requestSystemUptime"
            tdkTestObj.addParameter("service_name", serviceName);
            tdkTestObj.addParameter("method_name", methodName);
            tdkTestObj.executeTestCase(expectedresult);
            print "Calling method :",methodName
            actualresult = tdkTestObj.getResult();

            if expectedresult in actualresult:
                print methodName, "call is successful";
                tdkTestObj.setResultStatus("SUCCESS");
                uptimeBefore = tdkTestObj.getResultDetails();
                print methodName, ": Details :" ,uptimeBefore

                #Reboot the STB
                smObj.initiateReboot();

                serviceName = "systemService";
                register = servicemanager.registerService(smObj,serviceName)
                if "SUCCESS" in register: 
                    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                    expectedresult="SUCCESS"
                    methodName="requestSystemUptime"
                    tdkTestObj.addParameter("service_name", serviceName);
                    tdkTestObj.addParameter("method_name", methodName);
                    tdkTestObj.executeTestCase(expectedresult);
                    print "Calling method after reboot:",methodName
                    actualresult = tdkTestObj.getResult();

                    if expectedresult in actualresult:
                        print methodName, "call after reboot is successful";
                        tdkTestObj.setResultStatus("SUCCESS");
                        uptimeAfter = tdkTestObj.getResultDetails();
                        print methodName, ": Details :" ,uptimeAfter
                    
                        if int((float)(uptimeBefore)) > int((float)(uptimeAfter)):
                            tdkTestObj = smObj.createTestStep('SM_ExecuteCmd');
                            tdkTestObj.addParameter("command",'awk \'{print $1}\' /proc/uptime | tr -d \'\n\'');
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            if expectedresult in actualresult:
                                uptimeValue = tdkTestObj.getResultDetails();
                                print "ExecuteCmd : Details :" ,uptimeValue
                                if (int((float)(uptimeAfter)) == int((float)(uptimeValue))) or (int((float)(uptimeAfter))+1 == int((float)(uptimeValue))):
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "Uptime value found using SM API and system command are same"
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Uptime value found using SM API and system command are NOT same"
                            else:
                                print "ExecuteCmd call is NOT successful";
                                tdkTestObj.setResultStatus("FAILURE");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");              
                            print "Uptime value before reboot is less than after reboot"
                    else:
                        print methodName, "call after reboot is NOT successful";
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print "Unable to register the System service"
            else:
                print methodName, "call is NOT successful";
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
