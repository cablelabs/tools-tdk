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
  <name>SM_DDS_GetConfiguration_Descr_Group3_17</name>
  <primitive_test_id/>
  <primitive_test_name>SM_DDS_GetConfiguration</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Checks if the service manager wrapper for TR-181 returns the correct value for the textual string containing information about the interface-(48-50)</synopsis>
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
    <test_case_id>CT_17739_17</test_case_id>
    <test_objective>Checks if the service manager wrapper for TR-181 returns the correct value for the textual string containing information about the interface-(48-50)</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3	</test_setup>
    <pre_requisite>HostIF should be enabled</pre_requisite>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)	
</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring â&#128;&#147; serviceName                                
CallMethod : const QString - "getConfiguration" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2.Service_Manager_Agent will register "org.rdk.DeviceDiagnostics_1" with ServiceManager component.
3.On Success of registerService , Service_Manager_Agent will invoke "getConfiguration" API to get the value of the objects "Device.X_RDKCENTRAL-COM_DocsIf.ifDescr_48,Device.X_RDKCENTRAL-COM_DocsIf.ifDescr_49,Device.X_RDKCENTRAL-COM_DocsIf.ifDescr_50".
4. TM invokes snmpget method using snmp library to get the value of corresponding OIDs.
5. TM will check if the values are same and return SUCCESS/FAILURE status.
6.Service_Manager_Agent will deregister the given service from ServiceManager component.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.
Checkpoint 2. Check the value retrieved using API is same as the value retrieved using snmp command.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_DDS_GetConfiguration_Descr_Group3_17</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import servicemanager;
import snmplib;
import sys;

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
snmpObj = tdklib.TDKScriptingLibrary("snmp","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_DDS_GetConfiguration_Descr_Group3_17');
snmpObj.configureTestCase(ip,port,'SM_DDS_GetConfiguration_Descr_Group3_17');


#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[SM LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus);

#Get the result of connection with test component and STB
snmpLoadStatus =snmpObj.getLoadModuleResult();
print "[SNMP LIB LOAD STATUS]  :  %s" %snmpLoadStatus;
snmpObj.setLoadModuleStatus(snmpLoadStatus);

if "SUCCESS" in smLoadStatus.upper() and "SUCCESS" in snmpLoadStatus.upper():
        serviceName = "org.rdk.DeviceDiagnostics_1";
        #Register Service
        register = servicemanager.registerService(smObj,serviceName);
        if "SUCCESS" in register:
                #Prmitive test case which associated to this Script
                tdkTestObj = smObj.createTestStep('SM_DDS_GetConfiguration');
                names = "Device.X_RDKCENTRAL-COM_DocsIf.ifDescr_48,Device.X_RDKCENTRAL-COM_DocsIf.ifDescr_49,Device.X_RDKCENTRAL-COM_DocsIf.ifDescr_50";
                nameList = names.split(',');
                expectedresult = "SUCCESS";
                tdkTestObj.addParameter("names",names);

                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                        resultDetails = tdkTestObj.getResultDetails();
                        resultDetails = resultDetails.replace(" name: ","").lstrip('[');
                        resultDetails = resultDetails.replace(" value: ","").rstrip(']');
                        resultDetails = resultDetails.rstrip('; ')
                        print resultDetails;
                        configTokens = resultDetails.split(";");
                        configDict = {};
			print configTokens;
                        if len(configTokens) == (len(nameList) * 2):
                                for index in range(len(configTokens)):
                                        if index%2 == 0:
                                                configDict[configTokens[index]] = configTokens[index+1];
                                tdkTestObj.setResultStatus("SUCCESS");
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Response is empty";

                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to get TR-181 value\n";
			unregister = servicemanager.unRegisterService(smObj,serviceName);
                        smObj.unloadModule("servicemanager");
                        snmpObj.unloadModule("snmp");
                        sys.exit();

                unregister = servicemanager.unRegisterService(smObj,serviceName);

                dsServiceName="deviceSettingService";
                #Register Service
                register = servicemanager.registerService(smObj,dsServiceName);
                if "SUCCESS" in register:
                        #Call GetDeviceInfo API
                        tdkTestObj = smObj.createTestStep('SM_DeviceSetting_GetDeviceInfo');
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        #Check for SUCCESS/FAILURE return value of SM_DeviceSetting_GetDeviceInfo
                        if expectedresult in actualresult:
                                print "SUCCESS: GetDeviceInfo successful";
                                tdkTestObj.setResultStatus("SUCCESS");
                                serviceDetail = tdkTestObj.getResultDetails();
                                tokens = serviceDetail.split(" ");
                                ecmIp = "";
                                for index in range(len(tokens)):
                                        if "ecm_ip" in tokens[index]:
                                                ecmIp = tokens[index+1];
                                                break;
                                if ecmIp != "":
                                        print "ECM IP: %s" %ecmIp;
                                        snmpOid = [".1.3.6.1.2.1.2.2.1.2.48",".1.3.6.1.2.1.2.2.1.2.49",".1.3.6.1.2.1.2.2.1.2.50"]
                                        status = "SUCCESS";
					tdkTestObj = snmpObj.createTestStep('SNMP_GetCommString');
                                        expectedresult="SUCCESS";
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        if expectedresult in actualresult:
                                                commString = tdkTestObj.getResultDetails();
                                                print "Community String is %s" %commString;

                                                for index in range(len(snmpOid)):
                                                        actResponse =snmplib.SnmpExecuteCmd("snmpget", commString, "-v 2c", snmpOid[index], ecmIp);
                                                        print "SNMP response is %s" %actResponse;
                                                        snmpValue = actResponse.split(": ");
                                                        value = snmpValue[-1].strip();

                                                        if configDict:
                                                                preeqData = configDict[nameList[index]].strip();
                                                                if preeqData != value.strip('\"'):
                                                                        status = "FAILURE";
                                                                        print "The values are not equal";
                                                                        break;
                                                        else:
                                                                print "TR-181 values not available for comparison";
                                                                status = "FAILURE";
                                                tdkTestObj.setResultStatus(status);
                                                if status == "SUCCESS":
                                                        print "Values are equal";
                                        else:
                                                print "Failed to get community string";
                                                tdkTestObj.setResultStatus("FAILURE");

                                else:
                                        print "Failed to get ECM IP";
                                        tdkTestObj.setResultStatus("FAILURE");

                        else:
                                print "FAILURE: GetDeviceInfo failure";
                                tdkTestObj.setResultStatus("FAILURE");
                        unregister = servicemanager.unRegisterService(smObj,dsServiceName);

        smObj.unloadModule("servicemanager");
        snmpObj.unloadModule("snmp");
else:
         print "Module loading failed";

