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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DTCP_CreateMaxSrcSess_36</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DTCP_Comp_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check that max of 8 source sessions can be created if no sink sessions are there.
TestType: Positive
TestcaseID: CT_DTCP_36</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>As per PACXG1V3-5022 test case is  DTCP library vendor specific</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
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
