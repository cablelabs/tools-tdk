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
  <version>10</version>
  <name>DTCP_ReleasePacket_07</name>
  <primitive_test_id/>
  <primitive_test_name>DTCP_Comp_Test</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>To release DTCP-IP packet. The processed packet may contain DTCP Manager allocated/owned buffers/memory - this call frees up these resources. 
TestType: Positive
TestCaseID: CT_DTCP_07</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DTCP_07</test_case_id>
    <test_objective>To release DTCP-IP packet. The processed packet may contain DTCP Manager allocated/owned buffers/memory - this call frees up these resources.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>DTCPMgrInitialize, DTCPMgrCreateSourceSession, DTCPMgrProcessPacket</pre_requisite>
    <api_or_interface_used>dtcp_result_t DTCPMgrCreateSourceSession(char *sinkIpAddress, int key_label, int PCPPacketSize, int maxPacketSize, DTCP_SESSION_HANDLE *handle);
dtcp_result_t DTCPMgrProcessPacket(DTCP_SESSION_HANDLE session, DTCPIP_Packet *packet);
dtcp_result_t DTCPMgrReleasePacket(DTCPIP_Packet *packet);
dtcp_result_t DTCPMgrDeleteDTCPSession(DTCP_SESSION_HANDLE session);</api_or_interface_used>
    <input_parameters>"sinkIp":'127.0.0.1',"keyLabel":0,"pcpPacketSize":0,"maxPacketSize":4096</input_parameters>
    <automation_approch>1.TM loads DTCP_agent via the test agent. 
2.The stub will invokes the RPC method for to Release the packet.
3. The stub function will call the API and result will be shared back to TM
4. TM will receive and display the result.</automation_approch>
    <except_output>Checkpoint 1 stub will check for the return value of the function.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DTCP_Test_Execute</test_stub_interface>
    <test_script>DTCP_ReleasePacket_07</test_script>
    <skipped>No</skipped>
    <release_version>M30</release_version>
    <remarks>Renamed from DTCP_ReleaseSrcPacket_07 to DTCP_ReleasePacket_07</remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
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
obj.configureTestCase(ip,port,'DTCP_ReleasePacket_07');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "DTCP module loading status :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
  #Primitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('DTCP_Comp_Test');

  expectedresult="SUCCESS";
  #Pre-Cond: Init,StartSource,CreateSrcSession,CreateSinkSession
  dtcp.init(tdkTestObj,expectedresult);
  dtcp.setLogLevel(tdkTestObj,expectedresult,kwargs={"level":3})
  dtcp.startSource(tdkTestObj,expectedresult,kwargs={'ifName':'lo','port':5017})
  result = tdkTestObj.getResult();
  if "SUCCESS" in result:
        #Disable unique key exchange
        dtcp.createSinkSession(tdkTestObj,expectedresult,kwargs={'srcIp':'127.0.0.1','srcPort':5017,'uniqueKey':0,'maxPacketSize':4096})
        #No session exchange key
        dtcp.createSourceSession(tdkTestObj,expectedresult,kwargs={'sinkIp':'127.0.0.1','keyLabel':0,'pcpPacketSize':0,'maxPacketSize':4096})
        #Calling Release Packet
        dtcp.releasePacket(tdkTestObj,expectedresult,kwargs={})
        #Post-Cond: DeleteSinkSession,DeleteSrcSession,StopSource
        dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"deviceType":0})
        dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"deviceType":1})
        dtcp.stopSource(tdkTestObj,expectedresult)
  else:
        print "DTCP StartSource failed"
  #Unload the dtcp module
  obj.unloadModule("dtcp");
else:
  print"DTCP module load failed"
