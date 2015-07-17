'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_HdmiCec_GetNumOfDevicesConnected_CecDisabled</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>106</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_RegisterService</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: Service Manager – Checking the number of cec devices connected after disabling CEC. Default value: 0 (If no devices connected)
Test Case Id: CT_Service Manager_35
Test Type: Negative</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4</execution_time>
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
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import devicesettings;

#To Check whether HDMI device is connected or not.
#Test component to be tested
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

dsObj.configureTestCase(ip,port,'DS_isDisplayConnected');

isDisplayConnected = "false"

#Get the result of connection with test component and STB
result =dsObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper():
	#Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj);
	#Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                result = devicesettings.dsIsDisplayConnected(dsObj)
                if "TRUE" in result:
			#Get the result of execution
			print "HDMI display connected"
			isDisplayConnected = "true"
		else:
                        print "HDMI display not connected."
			isDisplayConnected = "false"
	        #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(dsObj)
	else:
		print "Failed to initialize DSMgr"
	
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
else:
	print "DS loading failed";


if isDisplayConnected == "true":
	print " "
	print "[This Script as to be tested with no HDMI device connected!!!]"
	print "[Please test removing HDMI device. Exiting....!!!]"
	print " "
	exit()
else:
	print " "
	print "[HDMI device not connected proceeding to execute the script.]"
	print " "


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
iarm_obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'SM_HdmiCec_GetNumOfDevicesConnected_CecDisabled');
iarm_obj.configureTestCase(ip,port,'SM_HdmiCec_GetNumOfDevicesConnected_CecDisabled');

#Get the result of connection with test component and STB
loadModuleStatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

loadModuleStatus_iarm = iarm_obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus_iarm;

expected_Result = "SUCCESS"

if expected_Result in loadModuleStatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        expectedresult="SUCCESS"
        #Register the service hdmicecservice.
        service_name_hdmicec = "com.comcast.hdmiCec_1"
        tdkTestObj = obj.createTestStep('SM_RegisterService');
        tdkTestObj.addParameter("service_name",service_name_hdmicec);

        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        serviceRegDetails = tdkTestObj.getResultDetails();
        print "[REGISTRATION DETAILS] : ",serviceRegDetails
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");

                #Check whether the service exists.
                tdkTestObj = obj.createTestStep('SM_DoesServiceExist');
                expectedresult="SUCCESS"
                tdkTestObj.addParameter("service_name",service_name_hdmicec);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                existdetails = tdkTestObj.getResultDetails();
                print "[TEST EXECUTION DETAILS] : ",existdetails;

                if expectedresult in actualresult:
                        if "PRESENT" in existdetails:
                                tdkTestObj.setResultStatus("SUCCESS");

                                #Call IARM Bus API's
                                #Calling IARM Bus Init
                                iarm_obj.setLoadModuleStatus("SUCCESS");
                                actualresult,Obj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Init', 'SUCCESS',verifyList ={});
                                print "Status of IARM Init: ",actualresult

                                #calling IARMBUS API IARM_Bus_Connect
                                actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});
                                print "Status of IARM Connect: ",actualresult

                                #Disable the cec support setting it false.
                                tdkTestObj = obj.createTestStep('SM_HdmiCec_SetEnabled');
                                expectedresult = "SUCCESS"
				valueToSetEnabled = 0
				tdkTestObj.addParameter("valueToSetEnabled",valueToSetEnabled);
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                setEnabledDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",setEnabledDetails;

                                if expectedresult in actualresult:
					tdkTestObj.setResultStatus("SUCCESS");
					
					#Get the default number of devices connected after disabling the CEC support.
					tdkTestObj = obj.createTestStep('SM_HdmiCec_GetConnectedDevices');
	                                expectedresult = "SUCCESS"
        	                        tdkTestObj.executeTestCase(expectedresult);
                	                actualresult = tdkTestObj.getResult();
                        	        getConnDevDetails = tdkTestObj.getResultDetails();
	                                print "[TEST EXECUTION DETAILS] : ",getConnDevDetails;
					
					if expectedresult in actualresult:
						#Default value must be 0.
        	                                deviceCount = 0
                	                        deviceCountReturned = int(getConnDevDetails[5:])
                        	                print "GetConnectedDevices returned count: ",deviceCountReturned

                                	        #Compare the deviceCount with current Count returned.
	                                        if deviceCountReturned == deviceCount:
        	                                        tdkTestObj.setResultStatus("SUCCESS");
                	                                print "[COMPARING DEFAULT COUNT WITH RETURNED COUNT] : The getConnectedDevices() API SUCCESS"
                        	                else:
                                	                tdkTestObj.setResultStatus("FAILURE");
                                        	        print "[COMPARING DEFAULT COUNT WITH RETURNED COUNT] : The getConnectedDevices() API FAILURE"
	                                else:
        	                                tdkTestObj.setResultStatus("FAILURE");
                	                        print "getConnectedDevices FAILURE"
				else:
					tdkTestObj.setResultStatus("FAILURE");
					print "setEnabled FAILURE";

                                #Calling IARM_Bus_DisConnect API
                                actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});
                                print "Status of IARM DisConnect: ",actualresult

                                #calling IARMBUS API "IARM_Bus_Term"
                                actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Term', 'SUCCESS',verifyList ={});
                                print "Status of IARM Term: ",actualresult	

                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "HDMICEC service is not supported: FAILURE"
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "doesServiceExist FAILURE"

                #Unregister hdmicec service
                tdkTestObj = obj.createTestStep('SM_UnRegisterService');
                expectedresult="SUCCESS"
                tdkTestObj.addParameter("service_name",service_name_hdmicec);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                serviceUnRegDetails = tdkTestObj.getResultDetails();
                print "[UNREGISTRATION DETAILS] : %s"%serviceUnRegDetails;

                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Unregistration of HDMICEC service is SUCCESS"
                        print " "
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Unregistration of HDMICEC service is FAILURE"
                        print " "
	else:
		tdkTestObj.setResultStatus("FAILURE");
                print "Registration of HDMICEC service is FAILURE"
                print " "

        #Unload the servicemanager module
        obj.unloadModule("servicemanager");
        iarm_obj.unloadModule("iarmbus");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");			
