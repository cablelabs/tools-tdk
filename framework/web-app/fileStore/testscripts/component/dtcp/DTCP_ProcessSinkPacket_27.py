'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DTCP_ProcessSinkPacket_27</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DTCP_Comp_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To process DTCP-IP packet and return decrypted buffers.
TestType: Positive
TestcaseID: CT_DTCP_27</synopsis>
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
obj.configureTestCase(ip,port,'DTCP_ProcessSinkPacket_27');

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
  dtcp.startSource(tdkTestObj,expectedresult,kwargs={'ifName':'lo','port':5003})
  #Enable uniqueKey flag to request unique exchange key
  dtcp.createSinkSession(tdkTestObj,expectedresult,kwargs={'srcIp':'127.0.0.1','srcPort':5003,'uniqueKey':1,'maxPacketSize':4096})
  #Provide session exchange key sink generates (decimal 87 or 0x57)
  dtcp.createSourceSession(tdkTestObj,expectedresult,kwargs={'sinkIp':'127.0.0.1','keyLabel':87,'pcpPacketSize':0,'maxPacketSize':4096})
  #Calling Process Packet
  dtcp.processPacket(tdkTestObj,expectedresult,kwargs={"index":0})
  #Post-Cond: DeleteSinkSession,DeleteSrcSession,StopSource
  dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"index":0,"deviceType":0})
  dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"index":0,"deviceType":1})
  dtcp.stopSource(tdkTestObj,expectedresult)

  #Unload the dtcp module
  obj.unloadModule("dtcp");
else:
  print"DTCP module load failed"
