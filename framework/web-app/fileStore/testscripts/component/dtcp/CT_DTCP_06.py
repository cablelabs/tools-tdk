'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1717</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>CT_DTCP_06</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>661</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TestMgr_DTCPAgent_Init</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>DTCP – processes a DTCP-IP packet - encrypts or decrypts buffers,		TCID: CT_DTCP_06</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dtcp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DTCP_06');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "DTCP module loading status :  %s" %loadmodulestatus;

if "Success" in loadmodulestatus:
  print "DTCP module loaded successfully";
  #Set the module loading status
  obj.setLoadModuleStatus("SUCCESS");

  #calling DTCP API Initialization
  tdkTestObj = obj.createTestStep('TestMgr_DTCPAgent_Init');
  dtcp_Init_expectedresult="SUCCESS";
  #Configuring the test object for starting test execution
  fnName="DTCPMgrProcessPacket";
  tdkTestObj.addParameter("funcName", fnName);
  tdkTestObj.executeTestCase(dtcp_Init_expectedresult);
  dtcp_Init_actualresult = tdkTestObj.getResult();
  details=tdkTestObj.getResultDetails();
  print "dtcp_Init_actualresult  :%s" %dtcp_Init_actualresult; 
  time.sleep(10);
  #Check for SUCCESS return value of dtcp_Initialization
  if "SUCCESS" in dtcp_Init_actualresult.upper():
    tdkTestObj.setResultStatus("SUCCESS");
    print "SUCCESS: Application successfully executed the API :%s" %fnName;
  else:
    tdkTestObj.setResultStatus("FAILURE");
    print "FAILURE: In executed the API  with details %s " %details;   
    print "Initialization result of DTCP : %s" %dtcp_Init_actualresult;

  #Unload the dtcp module
  obj.unloadModule("dtcp");

else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
