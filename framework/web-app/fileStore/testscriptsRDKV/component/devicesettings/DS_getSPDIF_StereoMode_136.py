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
  <name>DS_getSPDIF_StereoMode_136</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetStereoMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_DS_136 - DS_getSPDIF_StereoMode_136 - This test is executed to get the Stereo Mode of SPDIF and expect the result to be SURROUND</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>8</execution_time>
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
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_getSPDIF_StereoMode_136');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
	print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize 
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");

                #calling DS_SetStereoMode to get the current stereo mode
                tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                tdkTestObj.addParameter("port_name","SPDIF0");
                tdkTestObj.addParameter("get_only",1);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                stereomodedetails = tdkTestObj.getResultDetails();
                print "Port: SPDIF0 ",stereomodedetails;

                #Check for SUCCESS/FAILURE return value of DS_SetStereoMode
                if expectedresult in actualresult:
                        print "Application successfully fetched Stereomode for SPDIF0";
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Application failed to get the Stereomode for SPDIF0";


		if "SURROUND" in stereomodedetails:
			print "Stereo Mode for port SPDIF0 already set to SURROUND";
		else:

                	#calling DS_GetSupportedStereoModes get list of StereoModes.
                	tdkTestObj = obj.createTestStep('DS_GetSupportedStereoModes');
                	tdkTestObj.addParameter("port_name","SPDIF0");
                	expectedresult="SUCCESS"
                	tdkTestObj.executeTestCase(expectedresult);
                	actualresult = tdkTestObj.getResult();
                	supportedModes = tdkTestObj.getResultDetails();
                	print supportedModes
                	#Check for SUCCESS/FAILURE return value of DS_GetSupportedStereoModes
                	if expectedresult in actualresult:
                        	print "Successfully fetched list of supported StereoModes for SPDIF0";
                        	tdkTestObj.setResultStatus("SUCCESS");
				if "SURROUND" in supportedModes:
					print "SURROUND StereoMode is supported"
				else:
					print "SURROUND is not a supported StereoMode"
                	else:
                        	tdkTestObj.setResultStatus("FAILURE");
                        	print "Failed to get supported stereo modes";

			obj.initiateReboot();

			print "Get Stereo Mode for port SPDIF0 after Reboot";
                	#calling DS_SetStereoMode to get and set the stereo modes
                	tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                	tdkTestObj.addParameter("port_name","SPDIF0");
                	tdkTestObj.addParameter("get_only",1);
                	expectedresult="SUCCESS"
                	tdkTestObj.executeTestCase(expectedresult);
                	actualresult = tdkTestObj.getResult();
                	stereomodedetails = tdkTestObj.getResultDetails();
			print "Port: SPDIF0 ",stereomodedetails;
                	#Check for SUCCESS/FAILURE return value of DS_SetStereoMode
                	if expectedresult in actualresult:
                        	print "SUCCESS :Application successfully get the Stereomode for SPDIF";
                        	#comparing stereo modes before and after setting
                        	if "SURROUND" in stereomodedetails:
                                	tdkTestObj.setResultStatus("SUCCESS");
                                	print "SUCCESS: SURROUND Mode set for SPDIF after Reboot";
                        	else:
                                	tdkTestObj.setResultStatus("FAILURE");
                                	print "FAILURE: SURROUND Mode not set for SPDIF after Reboot";
                	else:
                        	tdkTestObj.setResultStatus("FAILURE");
                        	print "FAILURE :Application failed to get the Stereomode for SPDIF";

                #calling DS_ManagerDeInitialize to DeInitialize API 
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize 
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Deinitalize failed" ;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";