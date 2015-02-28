'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARMBUS_Two_Evt_Sender_Two_Evt_Receiver</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUSPERF_RegisterTwoEvtHandlersTwoEvents</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis></synopsis>
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
    <rdk_version>RDK1.2</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import time;
from resetAgent import resetAgent;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'IR_event_performance');

loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS"); 

	#Prmitive test case which associated to this Script
	tdkTestObj = obj.createTestStep('IARMBUSPERF_Init');
        expectedresult="SUCCESS/FAILURE"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult or ("FAILURE" in actualresult and "INVALID_PARAM" in details)):
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Application successfully initialized with IARMBUSPERF library";
                #calling IARMBUS API "IARM_Bus_Connect"
                tdkTestObj = obj.createTestStep('IARMBUSPERF_Connect');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Application successfully connected with IARM-Bus Daemon";
	
			#Prmitive test case which associated to this Script
			tdkTestObj = obj.createTestStep('IARMBUSPERF_RegisterEventHandler');
			#registering event handler for IR Key events
			tdkTestObj.addParameter("owner_name","IRMgr");
			tdkTestObj.addParameter("event_id",0);
			expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Event Handler registered for IR key events";
                                #sleep for 3 sec to receive IR key event that is broadcasted from second app.
                                time.sleep(3);

				#Prmitive test case which associated to this Script
				tdkTestObj = obj.createTestStep('IARMBUSPERF_RegisterEventHandler');
				#registering event handler for IR Key events
				tdkTestObj.addParameter("owner_name","Daemon");
				tdkTestObj.addParameter("event_id",1);
				expectedresult="SUCCESS"
                        	tdkTestObj.executeTestCase(expectedresult);
	                        actualresult = tdkTestObj.getResult();
        	                details=tdkTestObj.getResultDetails();
                	        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                        	if expectedresult in actualresult:
                                	tdkTestObj.setResultStatus("SUCCESS");
	                                print "SUCCESS: Event Handler registered for IR key events";
        	                        #sleep for 3 sec to receive IR key event that is broadcasted from second app.
                	                time.sleep(3);

					#Prmitive test case which associated to this Script
					tdkTestObj = obj.createTestStep('IARMBUSPERF_InvokeEventTransmitterApp');
					#registering event handler for IR Key events
					tdkTestObj.addParameter("owner_name","IRMgr");
					tdkTestObj.addParameter("event_id",0);
					tdkTestObj.addParameter("evttxappname","gen_single_event");
					tdkTestObj.addParameter("keyType",32768);
					tdkTestObj.addParameter("keyCode",301);
					expectedresult="SUCCESS"
                                	tdkTestObj.executeTestCase(expectedresult);
	                                actualresult = tdkTestObj.getResult();
        	                        #details=tdkTestObj.getResultDetails();
                	                #Check for SUCCESS/FAILURE return value of IARMBUS_InvokeSecondApplication
                        	        if expectedresult in actualresult:
                                	        tdkTestObj.setResultStatus("SUCCESS");
                                        	print "SUCCESS: Second application Invoked successfully";
	                                else:
        	                                tdkTestObj.setResultStatus("FAILURE");
                	                        print "FAILURE: Second application failed to execute";
                        	        time.sleep(2);
					#Prmitive test case which associated to this Script
					tdkTestObj = obj.createTestStep('IARMBUSPERF_InvokeEventTransmitterApp');
					#registering event handler for IARMBUS Daemon Key events
					tdkTestObj.addParameter("owner_name","Daemon");
					tdkTestObj.addParameter("event_id",1);
					tdkTestObj.addParameter("evttxappname","gen_single_event");
					expectedresult="SUCCESS"
                                	tdkTestObj.executeTestCase(expectedresult);
	                                actualresult = tdkTestObj.getResult();
        	                        #details=tdkTestObj.getResultDetails();
                	                #Check for SUCCESS/FAILURE return value of IARMBUS_InvokeSecondApplication
                        	        if expectedresult in actualresult:
                                	        tdkTestObj.setResultStatus("SUCCESS");
                                        	print "SUCCESS: Second application Invoked successfully";
	                                else:
        	                                tdkTestObj.setResultStatus("FAILURE");
                	                        print "FAILURE: Second application failed to execute";
                        	        time.sleep(2);									
					#Prmitive test case which associated to this Script
					tdkTestObj = obj.createTestStep('IARMBUSPERF_GetLastReceivedEventDetails');
					expectedresult="SUCCESS"
                	                tdkTestObj.executeTestCase(expectedresult);
                        	        actualresult = tdkTestObj.getResult();
                                	details=tdkTestObj.getResultDetails();
	                                print details;
        	                        #Check for SUCCESS/FAILURE return value of IARMBUS_GetLastReceivedEventDetails
                	                if expectedresult in actualresult:
                        	                tdkTestObj.setResultStatus("SUCCESS");
                                	        print "SUCCESS: GetLastReceivedEventDetails executed successfully";
	                                else:
        	                                tdkTestObj.setResultStatus("FAILURE");
                	                        print "FAILURE: GetLastReceivedEventDetails failed";
	
					tdkTestObj = obj.createTestStep('IARMBUSPERF_UnRegisterEventHandler');
					#Transmit IR Key events
					tdkTestObj.addParameter("owner_name","Daemon");
					tdkTestObj.addParameter("event_id",1);

					expectedresult="SUCCESS"
                        	        tdkTestObj.executeTestCase(expectedresult);
                                	actualresult = tdkTestObj.getResult();
	                                details=tdkTestObj.getResultDetails();
        	                        #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                	                if expectedresult in actualresult:
                        	                tdkTestObj.setResultStatus("SUCCESS");
                                	        print "SUCCESS: UnRegister Event Handler for IR key events";
	                                else:
        	                                tdkTestObj.setResultStatus("FAILURE");
                	                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
 	                        else:
        	                    tdkTestObj.setResultStatus("FAILURE");
                	            print "FAILURE : IARM_Bus_RegisterEventHandler Daemon Events failed. %s " %details;

				tdkTestObj = obj.createTestStep('IARMBUSPERF_UnRegisterEventHandler');
				#Transmit IR Key events
				tdkTestObj.addParameter("owner_name","IRMgr");
				tdkTestObj.addParameter("event_id",0);
				expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: UnRegister Event Handler for IR key events";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;

                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE : IARM_Bus_RegisterEventHandler IR Events failed. %s " %details;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: IARM_Bus_Connect failed. %s" %details;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: IARM_Bus_Init failed. %s " %details;

	#calling IARMBUS API "IARM_Bus_DisConnect"
        tdkTestObj = obj.createTestStep('IARMBUSPERF_DisConnect');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_DisConnect
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Application successfully disconnected from IARMBus";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: IARM_Bus_Disconnect failed. %s " %details;
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        
	obj.unloadModule("iarmbus");
	#resetAgent(ip,8090,"true");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");