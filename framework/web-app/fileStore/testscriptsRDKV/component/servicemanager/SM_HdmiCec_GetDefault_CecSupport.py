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
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_HdmiCec_GetDefault_CecSupport</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>106</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_RegisterService</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: Service Manager - Checking for CEC support default value (Enabled / Disabled). Default value: false(Disabled).
Test Case Id: CT_Service Manager_31
Test Type: Positive.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This testcase will fail because of RDKTT-618</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
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
import devicesettings;
import iarmbus;
import servicemanager;
from time import sleep;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#To Check whether HDMI device is connected or not.
#Test component to be tested
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
dsObj.configureTestCase(ip,port,'DS_isDisplayConnected');
#Get the result of connection with test component and STB
result = dsObj.getLoadModuleResult();
print "[devicesettings LIB LOAD STATUS]  :  %s" %result;
dsObj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
	isDisplayConnected = "FALSE"
	#Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj);
	#Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                isDisplayConnected = devicesettings.dsIsDisplayConnected(dsObj)
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");

        if "FALSE" == isDisplayConnected:
		print "\nPlease test with HDMI device connected. Exiting....!!!"
		exit()
else:
	exit()


#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");

smObj.configureTestCase(ip,port,'SM_HdmiCec_GetDefault_CecSupport');
iarmObj.configureTestCase(ip,port,'SM_HdmiCec_GetDefault_CecSupport');

#Get the result of connection with test component and STB
smLoadStatus = smObj.getLoadModuleResult();
print "[servicemanager LIB LOAD STATUS]  :  %s" %smLoadStatus;
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[iarmbus LIB LOAD STATUS]  :  %s" %iarmLoadStatus;
#Set the module loading status
smObj.setLoadModuleStatus(smLoadStatus.upper());
iarmObj.setLoadModuleStatus(iarmLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper() and "SUCCESS" in iarmLoadStatus.upper():

	#Calling IARM Bus Init
	init=iarmbus.IARMBUS_Init(iarmObj,'SUCCESS')	
        if "SUCCESS" in init:
		connect=iarmbus.IARMBUS_Connect(iarmObj,'SUCCESS')
		if "SUCCESS" in connect:

        		#Remove cecData file
        		print "Flush CEC persistent data"
        		tdkTestObj = smObj.createTestStep('SM_HdmiCec_FlushCecData');
        		expectedresult = "SUCCESS"
        		tdkTestObj.executeTestCase(expectedresult);
        		actualresult = tdkTestObj.getResult();
        		details = tdkTestObj.getResultDetails();
        		print "[TEST EXECUTION DETAILS] : ",details;
        		if expectedresult in actualresult:
                		tdkTestObj.setResultStatus("SUCCESS");
        		else:
                		tdkTestObj.setResultStatus("FAILURE");

			#Create HdmiCecService
			service_name = "com.comcast.hdmiCec_1"
			register = servicemanager.registerService(smObj,service_name)
			if "SUCCESS" in register:	
				print "Get default cec support value"
				defaultCec = 0
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_GetEnabled');
                                expectedresult = "SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                getEnabledDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",getEnabledDetails;
                                if expectedresult in actualresult:
                                        #Compare the set value with get value
                                        if defaultCec == int(getEnabledDetails):
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Get Default CecSupport returned false as expected"
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Get Default CecSupport did not return false as expected"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");


                                #Verify the presence of the cecData file
                                print "Verify the presence of CEC data"
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_CheckCecData');
                                expectedresult = "SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",details;
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");

                                #Delete HdmiCecService
                                unregister = servicemanager.unRegisterService(smObj,service_name)

                        #Calling IARM_Bus_DisConnect API
                        disconnect=iarmbus.IARMBUS_DisConnect(iarmObj,'SUCCESS')
                term=iarmbus.IARMBUS_Term(iarmObj,'SUCCESS')

        #Unload the modules
        smObj.unloadModule("servicemanager");
        iarmObj.unloadModule("iarmbus");
