'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>803</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARMBUS_RegisterEvtHandler_With_NegId_48</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>22</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_RegisterEventHandler</primitive_test_name>
  <!--  -->
  <primitive_test_version>15</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test script tests Register event handler and deregistering for negative event ID 
TEST CASE ID:	CT_IARMBUS_48</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This test is skipped as it is not a valid scenario (XONE-14090)</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_IARMBUS_48');
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
                #Check for SUCCESS/FAILURE return value of IARM_Bus_Connect
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully connected with IARMBUS ";
                        #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                        tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                        # Register for IR Key event.
                        tdkTestObj.addParameter("owner_name","IRMgr");
                        tdkTestObj.addParameter("event_id",-9);
                        expectedresult="FAILURE";
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                        if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "SUCCESS :Event Handler not registered";
                            #calling IARMBUS API "IARM_Bus_UnRegisterEventHandler"
                            tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                            tdkTestObj.addParameter("owner_name","IRMgr");
                            tdkTestObj.addParameter("event_id",0);
                            expectedresult="FAILURE";
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            details=tdkTestObj.getResultDetails();
                            #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                            if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Event Handler unregistered successfully";
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: IARM_Bus_UnRegisterEventHandler success %s" %details;
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "FAILURE: IARM_Bus_RegisterEventHandler failed %s" %details;
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
        #Unload the iarmbus module
        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
