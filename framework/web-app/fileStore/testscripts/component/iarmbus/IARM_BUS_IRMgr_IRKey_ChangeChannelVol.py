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
  <id>1603</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARM_BUS_IRMgr_IRKey_ChangeChannelVol</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>18</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_BroadcastEvent</primitive_test_name>
  <!--  -->
  <primitive_test_version>6</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check if multiple IR event notification is received for repeated key press/release for keys: channel up, channel down, Volume Up, Volume Down.
Testcase ID: CT_IARMBUS_109</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
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
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'IARM_BUS_IRMgr_IRKey_ChangeChannelVol');
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
                        #set owner to IRMgr
                        ownerName="IRMgr"
                        # IR KEY Event
                        eventId=0
                        #passing parameter for receiving IRMgr events
                        tdkTestObj.addParameter("owner_name",ownerName);
                        tdkTestObj.addParameter("event_id",eventId);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Event Handler registered successfully";
                                #Broadcast IR Key event (CHANNELUP/CHANNELDOWN/VOLUMEUP/VOLUMEDOWN) from IR Mgr
                                for keyCode in range(0x00000088,0x0000008C):
                                    if keyCode == 0x00000088:
					keyCodeStr = "CHANNELUP"
                                    elif keyCode == 0x00000089:
					keyCodeStr = "CHANNELDOWN"
                                    elif keyCode == 0x0000008A:
					keyCodeStr = "VOLUMEUP"
                                    elif keyCode == 0x0000008B:
					keyCodeStr = "VOLUMEDOWN"
                                    # Repeat Key Press/Release for 6 times
                                    for x in range(0,6):
					print '\n******** Iteration %d **********' % x ;
					tdkTestObj = obj.createTestStep('IARMBUS_InvokeEventTransmitterApp',0);
                                        if (x % 2 == 0):
                                                # Key Press
                                                keyType=0x00008000
						keyTypeStr="PRESS"
                                        else:
                                                # Key Release
                                                keyType=0x00008100
						keyTypeStr="RELEASE"

                                        tdkTestObj.addParameter("owner_name",ownerName);
                                        tdkTestObj.addParameter("event_id",eventId);
					tdkTestObj.addParameter("evttxappname","gen_single_event");
                                        tdkTestObj.addParameter("keyCode",keyCode);
                                        tdkTestObj.addParameter("keyType",keyType);
                                        print "Broadcasting IR Key Event (%s:%x,%s:%x)"%(keyCodeStr,keyCode,keyTypeStr,keyType)
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        #checking for Broadcast event invocation status
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Broadcasting Key success";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Broadcasting Key failed";

					#sleep for 1 sec to receive IR key event that is broadcasted from second app
					time.sleep(2);

                                        #Getting last received event details
                                        tdkTestObj = obj.createTestStep('IARMBUS_GetLastReceivedEventDetails');
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        print details
                                        #checking for event received status
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
						print "Successfully received broadcasted Event"
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
						print "Failed to receive broadcasted Event"
				    # End of for loop
				    print '\n********************************\n';
                                # End of for loop

                                #calling IARM_Bus_UnRegisterEventHandler API
                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                tdkTestObj.addParameter("owner_name",ownerName);
                                #Register for Broadcast event
                                tdkTestObj.addParameter("event_id",eventId);
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
        #Unload the iarmbus module
        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
