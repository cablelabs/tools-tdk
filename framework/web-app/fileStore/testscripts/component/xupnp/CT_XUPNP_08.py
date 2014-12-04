'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1701</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>CT_XUPNP_08</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>669</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TestMgr_XUPNPAgent_evtCheck</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>XUPNP – To check the serial no is updating or not when the event is triggered from the IARM test app	TCID: CT_XUPNP_08</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>7</execution_time>
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
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","2.0");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_IARMBUS_65');
loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling IARMBUS API "IARM_Bus_Init"
        tdkTestObj = obj.createTestStep('IARMBUS_Init');
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
                        print "SUCCESS :Application successfully connected with IARMBUS ";                      
                        #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                        tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                        #passing parameter for receiving SYSMgr event sys state STB Serial No
                        tdkTestObj.addParameter("owner_name","SYSMgr");
                        tdkTestObj.addParameter("event_id",0);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Event Handler registered successfully";
                                #invoking application to broadcast event
                                tdkTestObj = obj.createTestStep('IARMBUS_BroadcastEvent');
                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                tdkTestObj.addParameter("event_id",0);
                                tdkTestObj.addParameter("newState",33);
                                setstate=11;
                                seterror=22;
                                setpayload="PAPV00000408";
                                tdkTestObj.addParameter("state",setstate);
                                tdkTestObj.addParameter("error",seterror);
                                tdkTestObj.addParameter("payload",setpayload);

                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                #checking for Broadcast event invokation status
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS:Broadcast event success";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE:Broadcast event fails";
                                time.sleep(10);
                                #calling IARMBUS API "IARM_Bus_Call"
                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                tdkTestObj.addParameter("method_name","GetSystemStates");
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #checking for event received status
                                if expectedresult in actualresult:
                                        if str(seterror) in details:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print details;
                                                print "SUCCESS: RPC method invoked and STB Serial No value for state and error properly set";
                                        else :
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print details;
                                                print "FAILURE: RPC method invoked and STB Serial No value for state and error has not been set";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARMBUS call failed";
                                #calling IARM_Bus_UnRegisterEventHandler API
                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                #Register for Broadcast event
                                tdkTestObj.addParameter("event_id",0);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS:UnRegister Event Handler registered successfully";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARM_Bus_UnRegisterEventHandler failed %s" %details;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: IARM_Bus_RegisterEventHandler %s" %details;
                        # Calling IARM_Bus_DisConnect API
                        tdkTestObj = obj.createTestStep('IARMBUS_DisConnect');
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
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: IARM_Bus_Connect failed. %s" %details;
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
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: IARM_Bus_Init failed. %s " %details;
        
        print "[TEST EXECUTION RESULT] : %s" %actualresult;

else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");


#Test component to be tested
obj1 = tdklib.TDKScriptingLibrary("xupnp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
obj1.configureTestCase(ip,port,'CT_XUPNP_08');

#Get the result of connection with test component and STB
loadmodulestatus = obj1.getLoadModuleResult();
print "XUPNP module loading status :  %s" %loadmodulestatus;

if "Success" in loadmodulestatus:
  print "XUPNP module loaded successfully";
  #Set the module loading status
  obj1.setLoadModuleStatus("SUCCESS");

  #calling XUPNP API "TestMgr_XUPNPAgent_evtCheck"
  tdkTestObj1 = obj1.createTestStep('TestMgr_XUPNPAgent_evtCheck');
  expectedresult="SUCCESS";
  #Configuring the test object for starting test execution
  tdkTestObj1.addParameter("evtName","serialNo");
  tdkTestObj1.addParameter("evtValue","PAPV00000408");
  tdkTestObj1.executeTestCase(expectedresult);
  actualresult = tdkTestObj1.getResult();
  details=tdkTestObj1.getResultDetails();
  print "XUPNPAgent_evtCheck_actualresult  :%s" %actualresult; 
  #Check for SUCCESS return value of XUPNPAgent_evtCheck
  if "SUCCESS" in actualresult.upper():
    tdkTestObj1.setResultStatus("SUCCESS");
    print "SUCCESS: XUPNPAgent_evtCheck";
  else:
    tdkTestObj1.setResultStatus("FAILURE");
    print "FAILURE:  XUPNPAgent_evtCheck %s " %details;   

  #Unload the modules
  obj1.unloadModule("xupnp");
  obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj1.setLoadModuleStatus("FAILURE");		

