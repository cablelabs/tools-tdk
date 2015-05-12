'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DTCP_DeleteSinkSess_20</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DTCP_Comp_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To stop an active DTCP-IP sink session.
TestType: Positive
TestcaseID: CT_DTCP_20</synopsis>
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
obj.configureTestCase(ip,port,'DTCP_DeleteSinkSess_20');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "DTCP module loading status :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
  #Primitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('DTCP_Comp_Test');

  expectedresult="SUCCESS";
  #Pre-cond: Init,SetLoglevel,StartSource,CreateSinkSession
  dtcp.init(tdkTestObj,expectedresult);
  dtcp.setLogLevel(tdkTestObj,expectedresult,kwargs={"level":3})
  dtcp.startSource(tdkTestObj,expectedresult,kwargs={'ifName':'lo','port':5000})
  prevNum = dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':1})
  print "num of sink sessions before creating new session: [%s]"%prevNum
  dtcp.createSinkSession(tdkTestObj,expectedresult,kwargs={'srcIp':'127.0.0.1','srcPort':5000,'uniqueKey':0,'maxPacketSize':4096})
  #Calling DeleteSinkSession
  dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"index":0,"deviceType":1})
  #Check if session is deleted successfully
  fnName="DTCPMgrGetNumSessions";
  #Add parameters to test object
  deviceType=1
  tdkTestObj.addParameter("funcName", fnName);
  tdkTestObj.addParameter("intParam2", deviceType);
  #Execute the test case in STB
  tdkTestObj.executeTestCase(expectedresult);
  #Get the result of execution
  result = tdkTestObj.getResult();
  currNum = tdkTestObj.getResultDetails();
  print "Input: [funcName:%s deviceType:%d]"%(fnName,deviceType);
  print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
  print "num of sink sessions after deleting session: [%s]"%currNum

  #As per RDKTT-242,DTCP sink session is persistent and on every channel change, dtcp uses the same session
  #Set the result status of execution
  if ((expectedresult in result) and (1 == int(currNum))):
       tdkTestObj.setResultStatus("SUCCESS");
  else:
       tdkTestObj.setResultStatus("FAILURE");

  #Post-Cond: StopSrc
  dtcp.stopSource(tdkTestObj,expectedresult)

  #Unload the dtcp module
  obj.unloadModule("dtcp");
else:
  print"DTCP module load failed";
