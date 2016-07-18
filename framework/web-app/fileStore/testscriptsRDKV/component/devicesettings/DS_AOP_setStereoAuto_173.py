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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_AOP_setStereoAuto_173</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_AOP_setStereoAuto</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: This API is used to set the stereo mode to be auto.
Test Case CT_DS_173
Test Type: Positive</synopsis>
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
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_AOP_setStereoAuto_173');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;

if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;

        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");

		#Get the Audio types supported.	
                tdkTestObj = obj.createTestStep('DS_HOST_getAudioOutputPorts');
		expectedresult="SUCCESS"
		print " "
		tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails()
                print "[DS_HOST_getAudioOutputPorts RESULT] : %s" %actualresult;
                print "[DS_HOST_getAudioOutputPorts DETAILS] : %s" %details;

		#Check for SUCCESS/FAILURE return value of DS_HOST_getAudioOutputPorts.
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Get DS_HOST_getAudioOutputPorts";
	
	                #calling Device Settings - Set Stereo Auto.
        	        tdkTestObj = obj.createTestStep('DS_AOP_setStereoAuto');

			portNameLst = details.split(',')
			print "portName: ",portNameLst

			for portName in portNameLst:
				for autoMode in range(0,2):
		                	tdkTestObj.addParameter("autoMode",autoMode);
					tdkTestObj.addParameter("port_name",portName);
        		        	expectedresult="SUCCESS"
                			print " "
		                	tdkTestObj.executeTestCase(expectedresult);
        		        	actualresult = tdkTestObj.getResult();
	        	        	details = tdkTestObj.getResultDetails()
        	        		print "[DS_AOP_setStereoAuto RESULT] : %s" %actualresult;
		                	print "[PortName:%s setStereoAuto DETAILS: %s]" %(portName,details);

        		        	#Check for SUCCESS/FAILURE return value of DS_AOP_setStereoAuto
                			if expectedresult in actualresult:
                        			tdkTestObj.setResultStatus("SUCCESS");
	                		else:
        		                	tdkTestObj.setResultStatus("FAILURE");
                			print " "
		else:
                	tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Get DS_HOST_getAudioOutputPorts"

                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS Deinitalize RESULT] : %s" %actualresult;

                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
        else:
                tdkTestObj.setResultStatus("FAILURE");

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
