'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>93</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARMBUS Register for Resource Available event test</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>22</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_RegisterEventHandler</primitive_test_name>
  <!--  -->
  <primitive_test_version>15</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script tests the receiving of RESOURCE_AVAILABLE Event when one application releases a resource.Test Case ID:CT_IARMBUS_29</synopsis>
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
    <box_type>IPClient-3</box_type>
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
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_IARMBUS_29');
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
                        #calling IARMBUS API "IARM_BusDaemon_RequestOwnership"
                        tdkTestObj = obj.createTestStep('IARMBUS_RequestResource');
                        tdkTestObj.addParameter("resource_type",1);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RequestResource
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Requested resource is allocated successfully for the application";
                                #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                                tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                                #passing parameter for receving RESOURCE_AVAILABLE event
                                tdkTestObj.addParameter("owner_name","Daemon");
                                tdkTestObj.addParameter("event_id",0);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS :Event Handler registered successfully";
                                        #Call second application to check for resource available event
                                        tdkTestObj = obj.createTestStep('IARMBUS_InvokeSecondApplication');
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS:InvokeSecondApplication success";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE:InvokeSecondApplication fails";
                                        #wait for 10 sec
                                        time.sleep(10);
                                        #Get last received event details
                                        tdkTestObj = obj.createTestStep('IARMBUS_GetLastReceivedEventDetails');
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        #checking for event receiving status
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print details;
                                                print "SUCCESS: Event is Received";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Event is not Received";

                                        #calling IARMBUS API "IARM_Bus_UnRegisterEventHandler"
                                        tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                        tdkTestObj.addParameter("owner_name","Daemon");
                                        tdkTestObj.addParameter("event_id",0);
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                        if expectedresult in actualresult:
                                                print "SUCCESS :Event Handler unregistered successfully";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: IARM_Bus_UnRegisterEventHandler failed. %s" %details;
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARM_Bus_RegisterEventHandler failed. %s" %details;
                                #calling IARMBUS API "IARM_BusDaemon_ReleaseOwnership"
                                tdkTestObj = obj.createTestStep('IARMBUS_ReleaseResource');
                                tdkTestObj.addParameter("resource_type",1);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of IARMBUS_ReleaseResource
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: IARM_BusDaemon_ReleaseOwnership success";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARM_BusDaemon_ReleaseOwnership failed. %s" %details;

                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: IARM_BusDaemon_RequestOwnership failed %s" %details;

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
