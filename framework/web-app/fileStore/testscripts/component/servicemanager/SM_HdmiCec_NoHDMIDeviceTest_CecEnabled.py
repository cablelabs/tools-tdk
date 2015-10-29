'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_HdmiCec_NoHDMIDeviceTest_CecEnabled</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>106</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_RegisterService</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: Service Manager - Checking the number of cec devices connected after enabling CEC without any hdmicec device connected.
Test Case Id: CT_Service Manager_51.
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
import iarmbus;
import servicemanager;

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
        	tdkTestObj = dsObj.createTestStep('DS_IsDisplayConnectedStatus');
        	expectedresult = "SUCCESS"
        	#Execute the test case in STB
        	tdkTestObj.executeTestCase(expectedresult);
        	#Get the result of execution
        	result = tdkTestObj.getResult();
        	details = tdkTestObj.getResultDetails();
        	print "Result: [%s] Details: [%s]"%(result,details)
        	#Set the result status of execution
        	if expectedresult in result:
			tdkTestObj.setResultStatus("SUCCESS");
                	if "TRUE" in details:
                        	isDisplayConnected = "TRUE"
        	else:
                	tdkTestObj.setResultStatus("FAILURE");

                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");

        if "TRUE" == isDisplayConnected:
		print "\nPlease test without HDMI device. Exiting....!!!"
		exit()
else:
	exit()


#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

smObj.configureTestCase(ip,port,'SM_HdmiCec_NoHDMIDeviceTest_CecEnabled');
iarmObj.configureTestCase(ip,port,'SM_HdmiCec_NoHDMIDeviceTest_CecEnabled');

#Get the result of connection with test component and STB
smLoadStatus = smObj.getLoadModuleResult();
print "[servicemanager LIB LOAD STATUS]  :  %s" %smLoadStatus;
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[iarmbus LIB LOAD STATUS]  :  %s" %iarmLoadStatus;
#Set the module loading status
smObj.setLoadModuleStatus(smLoadStatus.upper());
iarmObj.setLoadModuleStatus(iarmLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper() and "SUCCESS" in iarmLoadStatus.upper():

	service_name = "com.comcast.hdmiCec_1"

	register = servicemanager.registerService(smObj,service_name)
        if "SUCCESS" in register:

                #Calling IARM Bus Init
		init=iarmbus.IARMBUS_Init(iarmObj,'SUCCESS')
		if "SUCCESS" in init:
			connect=iarmbus.IARMBUS_Connect(iarmObj,'SUCCESS')
			if "SUCCESS" in connect:

                                #Get CEC enabled value
                                print "Get default CEC Enable value"
                                defaultCec = 0
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_GetEnabled');
                                expectedresult = "SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                getEnabledDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",getEnabledDetails;
                                if expectedresult in actualresult:
                                        #Compare the default value with get value
                                        if defaultCec == int(getEnabledDetails):
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Get Default CecSupport returned false as expected"
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Get Default CecSupport did not return false as expected"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");

                                #Get the device Name
                                print "Get default device name"
				defaultName = "STB"
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_GetName');
                                expectedresult = "SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                setNameDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",setNameDetails;
                                if expectedresult in actualresult:
                                        print "DefaultName: %s GetName return value: %s"%(defaultName,getNameDetails)
                                        #Compare the default name with current name.
                                        if defaultName == getNameDetails:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "getName return value matches with default name"
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "getName return value does not match with default name"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");

                                #Enable the cec support setting it true.
				print "Set CEC Enabled"
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_SetEnabled');
                                expectedresult = "SUCCESS"
				valueToSetEnabled = 1
				tdkTestObj.addParameter("valueToSetEnabled",valueToSetEnabled);
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                setEnabledDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",setEnabledDetails;
                                if expectedresult in actualresult:
					tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");

                                print "Get CEC Enable value"
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_GetEnabled');
                                expectedresult = "SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                setEnabledDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",setEnabledDetails;
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");

                                #Set the device Name
				nameToSet = "tdktestname"
				print "Set device name to ", nameToSet
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_SetName');
                                expectedresult = "SUCCESS"
                                tdkTestObj.addParameter("nameToSet",nameToSet);
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                setNameDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",setNameDetails;
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");

                                #Get the device Name
                                print "Get device name"
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_GetName');
                                expectedresult = "SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                setNameDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",setNameDetails;
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");

				#Get the number of devices connected
				tdkTestObj = smObj.createTestStep('SM_HdmiCec_GetConnectedDevices');
	                        expectedresult = "SUCCESS"
        	                tdkTestObj.executeTestCase(expectedresult);
                             	actualresult = tdkTestObj.getResult();
                        	getConnDevDetails = tdkTestObj.getResultDetails();
	                        print "[TEST EXECUTION DETAILS] : ",getConnDevDetails;
				if expectedresult in actualresult:
					#Value must be greater than 0
       	                                defCount = 1
               	                        deviceCount = int(getConnDevDetails)
                               	        #Compare the deviceCount with default Count
                                        if deviceCount == defCount:
      	                                        tdkTestObj.setResultStatus("SUCCESS");
						print "deviceCount matches default count 1 without TV connected"
                        	        else:
                                	        tdkTestObj.setResultStatus("FAILURE");
						print "deviceCount does not match default count 1 without TV connected"
	                        else:
        	                        tdkTestObj.setResultStatus("FAILURE");

                                #Calling IARM_Bus_DisConnect API
                                disconnect=iarmbus.IARMBUS_DisConnect(iarmObj,'SUCCESS')
                        term=iarmbus.IARMBUS_Term(iarmObj,'SUCCESS')

                #Unregister hdmicec service
		unregister = servicemanager.unRegisterService(smObj,service_name)

        #Unload the modules
        smObj.unloadModule("servicemanager");
        iarmObj.unloadModule("iarmbus");
