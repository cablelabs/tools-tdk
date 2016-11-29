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
  <version>6</version>
  <name>DTCP_CreateMaxSrcSess_36</name>
  <primitive_test_id/>
  <primitive_test_name>DTCP_Comp_Test</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check that max of 8 source sessions can be created if no sink sessions are there.
TestType: Positive
TestcaseID: CT_DTCP_36</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks>As per PACXG1V3-5022 test case is  DTCP library vendor specific</remarks>
  <skip>true</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DTCP_36</test_case_id>
    <test_objective>To check that max of 8 source sessions can be created if no sink sessions are there</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>DTCPMgrInitialize</pre_requisite>
    <api_or_interface_used>dtcp_result_t DTCPMgrCreateSourceSession(char *sinkIpAddress, int key_label, int PCPPacketSize, int maxPacketSize, DTCP_SESSION_HANDLE *handle);
dtcp_result_t DTCPMgrDeleteDTCPSession(DTCP_SESSION_HANDLE session);</api_or_interface_used>
    <input_parameters>sinkIp':lan0-ip,'keyLabel':0,'pcpPacketSize':0,'maxPacketSize':4096</input_parameters>
    <automation_approch>1.TM loads DTCP_agent via the test agent. 
2.The stub will invokes the RPC method for to stop active session.
3. The stub function will call the API and result will be shared back to TM
4. TM will receive and display the result.</automation_approch>
    <except_output>Checkpoint 1 stub will check for the return value of the function.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DTCP_Test_Execute</test_stub_interface>
    <test_script>DTCP_CreateMaxSrcSess_36</test_script>
    <skipped>Yes</skipped>
    <release_version>M29</release_version>
    <remarks>Skipped from testsuite as per PACXG1V3-5022. This test case is DTCP library vendor specific</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import dtcp;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dtcp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DTCP_CreateMaxSrcSess_36');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "DTCP module loading status :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
  #Primitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('DTCP_Comp_Test');

  expectedresult="SUCCESS";
  #Pre-cond: Init,StartSrc
  dtcp.init(tdkTestObj,expectedresult);
  dtcp.setLogLevel(tdkTestObj,expectedresult,kwargs={"level":5})
  dtcp.startSource(tdkTestObj,expectedresult,kwargs={'ifName':'lo','port':5003})
  result = tdkTestObj.getResult();
  if "SUCCESS" in result:
        srcNum = int(dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':0}))
        sinkNum = int(dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':1}))
        print "Total sessions present: %d"%(srcNum+sinkNum)
        #Creating max of 8 source sessions are allowed if no sink sessions are there
        maxNum = 5003+(8-srcNum-sinkNum)
        for port in range (5003,maxNum):
              dtcp.createSinkSession(tdkTestObj,expectedresult,kwargs={'srcIp':'127.0.0.1','srcPort':port,'uniqueKey':0,'maxPacketSize':4096})
              dtcp.createSourceSession(tdkTestObj,expectedresult,kwargs={'sinkIp':'127.0.0.1','keyLabel':0,'pcpPacketSize':0,'maxPacketSize':4096})
        #Creating 8th source session should be denied
        dtcp.createSinkSession(tdkTestObj,expectedresult,kwargs={'srcIp':'127.0.0.1','srcPort':5020,'uniqueKey':0,'maxPacketSize':4096})
        dtcp.createSourceSession(tdkTestObj,'FAILURE',kwargs={'sinkIp':'127.0.0.1','keyLabel':0,'pcpPacketSize':0,'maxPacketSize':4096})
        #Post-Cond: Deleting all source sessions,stopSource
        srcNum = int(dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':0}))
        for index in range (0,srcNum):
              dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"deviceType":0})
        dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"deviceType":1})
        dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':0})
        dtcp.stopSource(tdkTestObj,expectedresult)

  else:
        print "DTCP StartSource failed"
  #Unload the dtcp module
  obj.unloadModule("dtcp");
