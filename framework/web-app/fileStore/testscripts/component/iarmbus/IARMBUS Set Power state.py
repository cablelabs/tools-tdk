'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>91</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARMBUS Set Power state</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>8</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <!--  -->
  <primitive_test_version>8</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script sets the Power state of the STB to the desired state
Test Case ID : CT_IARMBUS_27</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
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
obj.configureTestCase(ip,port,'CT_IARMBUS_27');
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
                        print "Application is successfully connected with IARM-BUS Daemon";
                        #calling IARMBUS API "IARM_Bus_Call"
                        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                        #passing parameter for querying STB power state
                        tdkTestObj.addParameter("method_name","GetPowerState");
                        tdkTestObj.addParameter("owner_name","PWRMgr");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        print "current power state: %s" %details;
                        curstate=details;
                        #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Querying STB power state -RPC method invoked successfully";
                                #Setting the POWER state
                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                tdkTestObj.addParameter("method_name","SetPowerState");
                                tdkTestObj.addParameter("owner_name","PWRMgr");
                                # setting state to ON
                                if curstate == "POWERSTATE_ON" :
                                        #change to STANDBY
                                        tdkTestObj.addParameter("newState",1);
                                elif curstate == "POWERSTATE_OFF":
                                        #change to ON
                                        tdkTestObj.addParameter("newState",2);
                                else:
                                        #change to ON
                                        tdkTestObj.addParameter("newState",2);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                print "set power state: %s" %details;
                                #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                before_set_powerstate = details;
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Setting STB power state -RPC method invoked successfully";
                                        #Querying the STB power state
                                        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                        tdkTestObj.addParameter("method_name","GetPowerState");
                                        tdkTestObj.addParameter("owner_name","PWRMgr");
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        print "current power state: %s" %details;
                                        #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                        after_set_powerset=details;
                                        if expectedresult in actualresult:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "SUCCESS: Querying STB power state -RPC method invoked successfully";
                                            if before_set_powerstate == after_set_powerset :
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Both the Power states are equal";
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Both power states are different";
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "FAILURE: Querying STB power state - IARM_Bus_Call failed. %s " %details;
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Set STB power state - IARM_Bus_Call failed. %s " %details;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Querying STB power state - IARM_Bus_Call failed. %s " %details;
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
