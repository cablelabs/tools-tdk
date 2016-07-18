#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARMBUS_DummyEvt_Persistent_test_LD</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>22</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_RegisterEventHandler</primitive_test_name>
  <!--  -->
  <primitive_test_version>15</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>As per RDKTT-620</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>300</execution_time>
  <!--  -->
  <long_duration>true</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <script_tags />
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import re
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'IARMBUS_DummyEvt_Persistent_test_LD');
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
                print "SUCCESS: Application successfully initialized with IARMBUS library";
                #calling IARMBUS API "IARM_Bus_Connect"
                tdkTestObj = obj.createTestStep('IARMBUS_Connect');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Application successfully connected with IARM-Bus Daemon";
                        i=0;
                        for i in range(0,100000):
                                				
                                print "**************** Iteration ", (i+1), " ****************";
                                tdkTestObj = obj.createTestStep('IARMBUS_InvokeSecondApplication');
                                tdkTestObj.addParameter("appname","Test_Event_Mgr");
                                tdkTestObj.addParameter("argv1","");
                                tdkTestObj.addParameter("apptype","background");
                                tdkTestObj.addParameter("iterationcount",i);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                #details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Second application Invoked successfully";

                                        time.sleep(2)			
                                        #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                                        tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                                        tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                        tdkTestObj.addParameter("event_id",0);
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Event Handler registered for Event-X";
                                                #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                                                tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                                                tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                                tdkTestObj.addParameter("event_id",1);
                                                expectedresult="SUCCESS"
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                details=tdkTestObj.getResultDetails();
                                                #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                                                if expectedresult in actualresult:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "SUCCESS: Event Handler registered for Event-Y";
                                                        #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                                                        tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                                                        tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                                        tdkTestObj.addParameter("event_id",2);
                                                        expectedresult="SUCCESS"
                                                        tdkTestObj.executeTestCase(expectedresult);
                                                        actualresult = tdkTestObj.getResult();
                                                        details=tdkTestObj.getResultDetails();
                                                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                                                        if expectedresult in actualresult:
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print "SUCCESS: Event Handler registered for Event-Z";
                                     
				        			#Syncing Second Application
                                                                tdkTestObj = obj.createTestStep('IARMBUS_SyncSecondApplication');
                                                                tdkTestObj.addParameter("lockenabled","false");
                                                                expectedresult="SUCCESS"
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult = tdkTestObj.getResult();
                                                                #Check for SUCCESS/FAILURE for syncing second application
                                                                if expectedresult in actualresult:
                                                                       tdkTestObj.setResultStatus("SUCCESS");
                                                                       print "SUCCESS: Second application synced successfully";
                                                                else:
                                                                       tdkTestObj.setResultStatus("FAILURE");
                                                                       print "FAILURE: Failed to sync second application";
                                     
                                                                time.sleep(1.2);
                                                                tdkTestObj = obj.createTestStep('IARMBUS_GetLastReceivedEventDetails');
                                                                expectedresult="SUCCESS"
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult = tdkTestObj.getResult();
                                                                details=tdkTestObj.getResultDetails();
                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_GetLastReceivedEventDetails
                                                                if "SUCCESS" in expectedresult:
                                                                        print "SUCCESS: GetLastReceivedEventDetails executed Successfully"
                                                                        line = details;
                                                                        matchObj = re.match( r'(.*)X(.*)Y(.*)Z.*',line)
                                                                        if matchObj:
                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                print "SUCCESS: All events are received successfully in order";
                                                                        else:
                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                                print "FAILURE: Events are not received in order";
                                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                                #deregistering event handler for event-X
                                                                                tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                                                                tdkTestObj.addParameter("event_id",0);
                                                                                expectedresult="SUCCESS"
                                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                                actualresult = tdkTestObj.getResult();
                                                                                details=tdkTestObj.getResultDetails();
                                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                                if expectedresult in actualresult:
                                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                                        print "SUCCESS: UnRegister Event Handler for Event-X";
                                                                                else:
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                                #deregistering event handler for event-Y
                                                                                tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                                                                tdkTestObj.addParameter("event_id",1);
                                                                                expectedresult="SUCCESS"
                                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                                actualresult = tdkTestObj.getResult();
                                                                                details=tdkTestObj.getResultDetails();
                                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                                if expectedresult in actualresult:
                                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                                        print "SUCCESS: UnRegister Event Handler for Event-Y";
                                                                                else:
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                                #deregistering event handler for event-Z
                                                                                tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                                                                tdkTestObj.addParameter("event_id",2);
                                                                                expectedresult="SUCCESS"
                                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                                actualresult = tdkTestObj.getResult();
                                                                                details=tdkTestObj.getResultDetails();
                                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                                if expectedresult in actualresult:
                                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                                        print "SUCCESS: UnRegister Event Handler Event-Z";
                                                                                else:
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                                                break;
                                                                else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print "FAILURE: GetLastReceivedEventDetails failed and all the events are not received";
                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                #deregistering event handler for event-X
                                                                tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                                                tdkTestObj.addParameter("event_id",0);
                                                                expectedresult="SUCCESS"
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult = tdkTestObj.getResult();
                                                                details=tdkTestObj.getResultDetails();
                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                if expectedresult in actualresult:
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                        print "SUCCESS: UnRegister Event Handler for Event-X";
                                                                else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                #deregistering event handler for event-Y
                                                                tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                                                tdkTestObj.addParameter("event_id",1);
                                                                expectedresult="SUCCESS"
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult = tdkTestObj.getResult();
                                                                details=tdkTestObj.getResultDetails();
                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                if expectedresult in actualresult:
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                        print "SUCCESS: UnRegister Event Handler for Event-Y";
                                                                else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                #deregistering event handler for event-Z
                                                                tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                                                tdkTestObj.addParameter("event_id",2);
                                                                expectedresult="SUCCESS"
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult = tdkTestObj.getResult();
                                                                details=tdkTestObj.getResultDetails();
                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                if expectedresult in actualresult:
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                        print "SUCCESS: UnRegister Event Handler Event-Z";
                                                                else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                        else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print "FAILURE : IARM_Bus_RegisterEventHandler failed. %s " %details;
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE : IARM_Bus_RegisterEventHandler failed. %s " %details;
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE : IARM_Bus_RegisterEventHandler failed. %s " %details;
				        	
				        	
				        time.sleep(2)
                                        #Syncing Second Application
                                        tdkTestObj = obj.createTestStep('IARMBUS_SyncSecondApplication');
                                        tdkTestObj.addParameter("lockenabled","false");
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        #Check for SUCCESS/FAILURE for syncing second application
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Second application synced successfully";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Failed to sync second application";				
                                
                                else:
				        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Failed to invoke Second application"
					
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
