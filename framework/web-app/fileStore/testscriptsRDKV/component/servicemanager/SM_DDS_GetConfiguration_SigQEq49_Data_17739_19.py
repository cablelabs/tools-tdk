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
  <name>SM_DDS_GetConfiguration_SigQEq49_Data_17739_19</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_DDS_GetConfiguration</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks if the service manager wrapper for TR-181 returns the correct value for Pre-equalization data for the down stream channel 49</synopsis>
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
    <box_type>Hybrid-1</box_type>
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
import servicemanager;
import snmplib;

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
snmpObj = tdklib.TDKScriptingLibrary("snmp","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_DDS_GetConfiguration_SigQEq49_Data_17739_19');
snmpObj.configureTestCase(ip,port,'SM_DDS_GetConfiguration_SigQEq49_Data_17739_19');


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
                names = "Device.X_RDKCENTRAL-COM_DocsIf.docsIfSigQEqualizationData_49";
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
                        for index in range(len(configTokens)):
                                if index%2 == 0:
                                        configDict[configTokens[index]] = configTokens[index+1];
                        tdkTestObj.setResultStatus("SUCCESS");

                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to get TR-181 value\n";

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
                                        snmpOid = [".1.3.6.1.2.1.10.127.1.1.4.1.7.49"];
                                        status = "SUCCESS";
                                        for index in range(len(snmpOid)):
                                                tdkTestObj = snmpObj.createTestStep('SNMP_GetCommString');
                                                actResponse =snmplib.SnmpExecuteCmd(tdkTestObj, "snmpget", "-v 2c", snmpOid[index], ecmIp);
                                                print "SNMP response is %s" %actResponse;
                                                snmpValue = actResponse.split(": ");
						preeqData = configDict[nameList[index]].strip();
						preeqData = preeqData.strip("\\\"").strip();
                                                if preeqData != snmpValue[-1].strip().replace("\n", "\\n"):
							print "**%s**" %preeqData;
							print "**%s**" %snmpValue[-1].strip().replace("\n", "\\n");
                                                        status = "FAILURE";
                                                        print "The values are not equal";
                                                        break;
                                        tdkTestObj.setResultStatus(status);
                                        if status == "SUCCESS":
                                                print "Values are equal";

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

