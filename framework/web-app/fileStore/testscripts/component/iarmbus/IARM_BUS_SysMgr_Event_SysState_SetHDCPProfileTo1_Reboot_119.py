'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARM_BUS_SysMgr_Event_SysState_SetHDCPProfileTo1_Reboot_119</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>8</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <!--  -->
  <primitive_test_version>8</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>IARMBUS – Set HDCP profile 1 using  IARM_BUS_SYSMGR_API_GetHDCPProfile RPC call.IARM_BUS_SYSMGR_API_SetHDCPProfile RPC call and check for persistence after reboot.
Test case Id - CT_IARMBUS_119</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>6</execution_time>
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
obj.configureTestCase(ip,port,'IARM_BUS_SysMgr_Event_SysState_SetHDCPProfileTo1_Reboot_119');
loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status :  %s" %loadmodulestatus ;


def iarmBus_Connect(testObj):
        #calling IARMBUS API "IARM_Bus_Init"
        tdkTestObj = testObj.createTestStep('IARMBUS_Init');
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
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: IARM_Bus_Connect failed. %s" %details;
                        return 1
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: IARM_Bus_Init failed. %s " %details;
                return 1

        return 0

def iarmBus_Disconnect(testObj):
        flagDisconnect = 0
        flagTerm = 0
        # Calling IARM_Bus_DisConnect API
        tdkTestObj = testObj.createTestStep('IARMBUS_DisConnect');
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
                flagDisconnect = 1

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
                flagTerm = 1

        if (flagDisconnect == 1) or (flagTerm == 1):
                return 1

        return 0

if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        ret = iarmBus_Connect(obj)
        if ret == 0:
                #Setting the POWER state
                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                tdkTestObj.addParameter("method_name","SetHDCPProfile");
                tdkTestObj.addParameter("owner_name","SYSMgr");

                # setting state to 1
                set_HDCPstate = 1
                tdkTestObj.addParameter("newState",set_HDCPstate);

                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                print "set HDCP profile value: %s" %details;
                #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Setting STB HDCP profile state -RPC method invoked successfully";
                        ret = iarmBus_Disconnect(obj)
                        if ret == 0:
                                obj.initiateReboot();
                                ret = iarmBus_Connect(obj)
                                if ret == 0:
                                        #calling IARMBUS API "IARM_Bus_Call"
                                        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                        #passing parameter for querying STB HDCP profile state
                                        tdkTestObj.addParameter("method_name","GetHDCPProfile");
                                        tdkTestObj.addParameter("owner_name","SYSMgr");
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        print "current HDCP state: %s" %details;
                                        curstate=details;
                                        #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Querying HDCP profile state -RPC method invoked successfully";
                                                if set_HDCPstate == int(curstate):
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "SUCCESS: Both the HDCP states are equal";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: Both HDCP states are different";
                                        ret = iarmBus_Disconnect(obj);
                                        if ret != 0:
                                                print "Failure returned from the iarmBus_Disconnect after reboot"
                                else:
                                        print "Failure returned from the iarmBus_Connect after reboot"
                        else:
                                print "Failure returned from the iarmBus_Disconnect";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Setting STB HDCP profile state - IARM_Bus_Call failed. %s " %details;
                        ret = iarmBus_Disconnect(obj);
                        if ret != 0:
                                print "Failure returned from the iarmBus_Disconnect after setting the profile"
        else:
                print "Failure returned from the iarmBus_Connect";
        #Unload the iarmbus module
        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
