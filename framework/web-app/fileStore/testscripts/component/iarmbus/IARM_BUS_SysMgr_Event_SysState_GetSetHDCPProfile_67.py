'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1413</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARM_BUS_SysMgr_Event_SysState_GetSetHDCPProfile_67</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>8</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <!--  -->
  <primitive_test_version>8</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>IARMBUS –Get and set HDCP profile using  IARM_BUS_SYSMGR_API_GetHDCPProfile RPC call.IARM_BUS_SYSMGR_API_SetHDCPProfile RPC call
Test case Id - CT_IARMBUS_67</synopsis>
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
    <box_type>Hybrid-1</box_type>
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
from tdklib import TDKScriptingLibrary;
#Test component to be tested
obj = TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_IARMBUS_67');
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
			for hdcpProfile in range(0,2):
					#Setting the HdcpProfile, RNG supports HDCPProfile = 0 and 1, others HDCPProfile = 1
                                	tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                	tdkTestObj.addParameter("method_name","SetHDCPProfile");
                                	tdkTestObj.addParameter("owner_name","SYSMgr");
					tdkTestObj.addParameter("newState",hdcpProfile);
                                	expectedresult="SUCCESS"
                                	tdkTestObj.executeTestCase(expectedresult);
                                	actualresult = tdkTestObj.getResult();
                                	details=tdkTestObj.getResultDetails();
                                	print "Set HDCP profile: %d"%(hdcpProfile);
                                	#Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                	if expectedresult in actualresult:
                                        	tdkTestObj.setResultStatus("SUCCESS");
                                        	print "SUCCESS: Setting STB HDCP profile is successful";
					else:
						tdkTestObj.setResultStatus("FAILURE");
						print "FAILURE: Setting STB HDCP profile failed. ",details;

                                        #Querying the STB HDCP profile
                                        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                        tdkTestObj.addParameter("method_name","GetHDCPProfile");
                                        tdkTestObj.addParameter("owner_name","SYSMgr");
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        print "Get HDCP profile: %s" %details;
                                        #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                        if expectedresult in actualresult:
                                                if str(hdcpProfile) == details:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "SUCCESS: HDCPProfile fetched is same as HDCPProfile set";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: HDCPProfile fetched is not same as HDCPProfile set";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Querying STB HDCP Profile. ",details;
			#End for loop

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
