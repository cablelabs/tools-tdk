'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DTCP_CreateMaxSinkSess_35</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DTCP_Comp_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check that max of only 1 sink session is created which is persistent on every channel change. 
TestType: Positive
TestcaseID: CT_DTCP_35</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
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
obj.configureTestCase(ip,port,'DTCP_CreateMaxSinkSess_35');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "DTCP module loading status :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
  #Primitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('DTCP_Comp_Test');

  expectedresult="SUCCESS";
  #Pre-cond: Init
  dtcp.init(tdkTestObj,expectedresult);
  dtcp.setLogLevel(tdkTestObj,expectedresult,kwargs={"level":3})
  dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':1})
  #Creating 10 instances of StartSource,CreateSinkSession
  for port in range (5000,5010):
      dtcp.startSource(tdkTestObj,expectedresult,kwargs={'ifName':'lo','port':port})
      dtcp.createSinkSession(tdkTestObj,expectedresult,kwargs={'srcIp':'127.0.0.1','srcPort':port,'uniqueKey':0,'maxPacketSize':4096})
  #Post-Cond: Stop all source after deleting all sink sessions
  sinkNum = int(dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':1}))
  for index in range (0,sinkNum):
      dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"index":index,"deviceType":1})
  dtcp.stopSource(tdkTestObj,expectedresult)

  #Unload the dtcp module
  obj.unloadModule("dtcp");
else:
  print"DTCP module load failed";
