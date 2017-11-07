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
  <version>3</version>
  <name>IARM_BUS_SysMgr_Event_SysState_SetHDCPProfileTo1_Reboot_119</name>
  <primitive_test_id>8</primitive_test_id>
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <primitive_test_version>8</primitive_test_version>
  <status>FREE</status>
  <synopsis>IARMBUS – Set HDCP profile 1 using  IARM_BUS_SYSMGR_API_GetHDCPProfile RPC call.IARM_BUS_SYSMGR_API_SetHDCPProfile RPC call and check for persistence after reboot.
Test case Id - CT_IARMBUS_119</synopsis>
  <groups_id/>
  <execution_time>6</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_IARMBUS_119</test_case_id>
    <test_objective>IARMBUS – Set HDCP profile1 using IARM_BUS_SYSMGR_API_GetHDCPProfile RPC call and verify if the value is persisted after reboot using IARM_BUS_SYSMGR_API_GetHDCPProfile RPC call.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1 / XG1-1</test_setup>
    <pre_requisite>“IARMDaemonMain” and "sysMgrMain" process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *)
IARM_Bus_Connect()
IARM_Bus_Call(const char *,  const char *, void *, size_t )
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_Call : const char * - IARM_BUS_SYSMGR_NAME, const char * - IARM_BUS_SYSMGR_API_GetHDCPProfile
(&amp;IARM_BUS_SYSMGR_API_SetHDCPProfile) void * - param, size_t -sizeof(param)
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon (First Application).
3.Set HDCP profile value to 1 using IARM_BUS_SYSMGR_API_SetHDCPProfile.
4. Reboot the device.
5.Compare the set HDCP profile value by getting the value from (IARM_BUS_SYSMGR_API_GetHDCPProfile) RPC call.
6.IARMBUS_Agent deregisters from the IARM Bus Daemon.
7.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return value of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.

Checkpoint 2. Check for the HDCP profile set and get value using the RPC call</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_BusCall</test_stub_interface>
    <test_script>IARM_BUS_SysMgr_Event_SysState_SetHDCPProfileTo1_Reboot_119</test_script>
    <skipped>No</skipped>
    <release_version>M23</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'IARM_BUS_SysMgr_Event_SysState_SetHDCPProfileTo1_Reboot_119');
loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status :  %s" %loadmodulestatus ;


def iarmBus_Connect(testObj):
        #calling IARMBUS API "IARM_Bus_Init"
        tdkTestObj = testObj.createTestStep('IARMBUS_Init');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult):
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with IARMBUS library";
                #calling IARMBUS API "IARM_Bus_Connect"
                tdkTestObj = obj.createTestStep('IARMBUS_Connect');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Application is successfully connected with IARM-BUS Daemon";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: IARM_Bus_Connect failed. %s" %details;
                        return 1
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: IARM_Bus_Init failed. %s " %details;
                return 1

        return 0

def iarmBus_Disconnect(testObj):
        flagDisconnect = 0
        flagTerm = 0
        # Calling IARM_Bus_DisConnect API
        tdkTestObj = testObj.createTestStep('IARMBUS_DisConnect');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_DisConnect
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully disconnected from IARMBus";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: IARM_Bus_Disconnect failed. %s " %details;
                flagDisconnect = 1

        #calling IARMBUS API "IARM_Bus_Term"
        tdkTestObj = obj.createTestStep('IARMBUS_Term');
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_Term
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: IARM_Bus term success";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: IARM_Bus Term failed";
                flagTerm = 1

        if (flagDisconnect == 1) or (flagTerm == 1):
                return 1

        return 0

if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        ret = iarmBus_Connect(obj)
        if ret == 0:
                #Setting the POWER state
                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                tdkTestObj.addParameter("method_name","SetHDCPProfile");
                tdkTestObj.addParameter("owner_name","SYSMgr");

                # setting state to 1
                set_HDCPstate = 1
                tdkTestObj.addParameter("newState",set_HDCPstate);

                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                print "set HDCP profile value: %s" %details;
                #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Setting STB HDCP profile state -RPC method invoked successfully";
                        ret = iarmBus_Disconnect(obj)
                        if ret == 0:
                                obj.initiateReboot();
                                ret = iarmBus_Connect(obj)
                                if ret == 0:
                                        #calling IARMBUS API "IARM_Bus_Call"
                                        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                        #passing parameter for querying STB HDCP profile state
                                        tdkTestObj.addParameter("method_name","GetHDCPProfile");
                                        tdkTestObj.addParameter("owner_name","SYSMgr");
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        print "current HDCP state: %s" %details;
                                        curstate=details;
                                        #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Querying HDCP profile state -RPC method invoked successfully";
                                                if set_HDCPstate == int(curstate):
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "SUCCESS: Both the HDCP states are equal";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: Both HDCP states are different";
                                        ret = iarmBus_Disconnect(obj);
                                        if ret != 0:
                                                print "Failure returned from the iarmBus_Disconnect after reboot"
                                else:
                                        print "Failure returned from the iarmBus_Connect after reboot"
                        else:
                                print "Failure returned from the iarmBus_Disconnect";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Setting STB HDCP profile state - IARM_Bus_Call failed. %s " %details;
                        ret = iarmBus_Disconnect(obj);
                        if ret != 0:
                                print "Failure returned from the iarmBus_Disconnect after setting the profile"
        else:
                print "Failure returned from the iarmBus_Connect";
        #Unload the iarmbus module
        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
