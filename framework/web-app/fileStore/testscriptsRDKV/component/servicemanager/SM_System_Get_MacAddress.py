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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_System_Get_MacAddress</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To get the ecm_mac, estb_mac, eth_mac and wifi_mac of the box</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_124</test_case_id>
    <test_objective>To get the estb mac, ecm mac, moca mac,eth mac and wifi mac using system service</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>"bool registerService(const QString&amp; , ServiceStruct )
Generic_CallMethod(const QString&amp; servicename,const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)"</api_or_interface_used>
    <input_parameters>"registerService : Qstring-serviceName, 
Generic_CallMethod - system service , setMode, getMode
UnregisterService : Qstring-serviceName"</input_parameters>
    <automation_approch>"1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register ""systemService"" with ServiceManager component.
3.Set the api version as 11
4.Service_Manager_Agent will invoke the api getMacAddresses
5. The API cal will return the various mac addresses.
6.Depending upon the return value of getMacAddresses, SUCCESS/FAILURE status is returned
7. Service_Manager_Agent will deregister the given service from ServiceManager component"</automation_approch>
    <except_output>"Checkpoint 1.System service should register successfully
Checkpoint 2.Get the mac addresses with getMAcAddresses API and compare it with the result obtained by reading the deviceDetails.cache file from the box"</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_System_Get_MacAddress</test_script>
    <skipped>No</skipped>
    <release_version>M51</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import servicemanager;
import json;


#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");


#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_System_Get_MacAddress');

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus.upper());


if "SUCCESS" in smLoadStatus.upper():
    serviceName = "systemService";
    #Register system service 
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
            tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
            expectedresult="SUCCESS"
            methodName="getMacAddresses"
            tdkTestObj.addParameter("service_name", serviceName);
            tdkTestObj.addParameter("method_name", methodName);
            tdkTestObj.executeTestCase(expectedresult);
            print "Calling method :",methodName
            actualresult = tdkTestObj.getResult();

            if expectedresult in actualresult:
                print methodName, "call is successful";
                tdkTestObj.setResultStatus("SUCCESS");
                macAddresses_api = tdkTestObj.getResultDetails();
                print methodName, ": Details :" ,macAddresses_api

                #Execute cat /tmp/.deviceDetails.cache if API call is success
                tdkTestObj = smObj.createTestStep('SM_ExecuteCmd');
		tdkTestObj.addParameter("command",'cat /tmp/.deviceDetails.cache');
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                    macDetails = tdkTestObj.getResultDetails();
		    macList=macDetails.split('\\n');
		    macList.pop();
		    macAddresses_cmd=[];
                    print "ExecuteCmd : Details :" 
		    for i in macList:
			if "ecm_mac" in i:
			    ecm_mac = i.split('=')[1];
			    print "ecm_mac: ",ecm_mac
			    macAddresses_cmd.append(ecm_mac);
			if "estb_mac" in i:
			    estb_mac = i.split('=')[1];
                            print "estb_mac: ",estb_mac
			    macAddresses_cmd.append(estb_mac);
			if "eth_mac" in i:
			    eth_mac = i.split('=')[1];
			    print "eth_mac: ",eth_mac
			    macAddresses_cmd.append(eth_mac);
			if "moca_mac" in i:
			    moca_mac = i.split('=')[1];
 			    print "moca_mac: ",moca_mac
			    macAddresses_cmd.append(moca_mac);
			if "wifi_mac" in i:
			    wifi_mac = i.split('=')[1];
			    print "wifi_mac: ",wifi_mac
			    macAddresses_cmd.append(wifi_mac);

		    #Check if the return values of execute cmd and API call are the same
		    if macAddresses_api in macAddresses_cmd:
			print "MAC Address obtained from getMacAddresses API and Execute command are the same"
			tdkTestObj.setResultStatus("SUCCESS");
		    else:
			print "MAC Address obtained from getMacAddresses API and Execute command are NOT same"
			tdkTestObj.setResultStatus("FAILURE");
		else:
		    print "ExecuteCmd call is NOT successful";
                    tdkTestObj.setResultStatus("FAILURE");
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

