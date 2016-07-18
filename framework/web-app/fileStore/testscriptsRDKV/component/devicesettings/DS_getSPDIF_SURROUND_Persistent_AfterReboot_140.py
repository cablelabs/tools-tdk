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
  <name>DS_getSPDIF_SURROUND_Persistent_AfterReboot_140</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetStereoMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_DS_140-DS_getSPDIF_SURROUND_Persistent_AfterReboot_140-This test gets the stereo mode value of SPDIF before and after reboot</synopsis>
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
from devicesettings import dsManagerInitialize, dsManagerDeInitialize;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_getSPDIF_SURROUND_Persistent_AfterReboot_140');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():

        #calling Device Settings - initialize API
	result = dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
	if "SUCCESS" in result:
                #calling DS_GetSupportedStereoModes get list of StereoModes
                tdkTestObj = obj.createTestStep('DS_GetSupportedStereoModes');
                tdkTestObj.addParameter("port_name","SPDIF0");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                supportedModes = tdkTestObj.getResultDetails();
                print supportedModes
                #Check for SUCCESS/FAILURE return value of DS_GetSupportedStereoModes
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
			print "Successfully fetched list of supported StereoModes for SPDIF0";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to get supported stereo modes";

		if "SURROUND" in supportedModes:
                	#calling DS_SetStereoMode to set stereo mode to "SURROUND"
                	tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                	stereomode="SURROUND";
                	print "Set stereo mode value to %s" %stereomode;
                	tdkTestObj.addParameter("stereo_mode",stereomode);
                	tdkTestObj.addParameter("port_name","SPDIF0");
                	expectedresult="SUCCESS"
                	tdkTestObj.executeTestCase(expectedresult);
                	actualresult = tdkTestObj.getResult();
                	stereomodedetails = tdkTestObj.getResultDetails();
                	#Check for return value
                	if expectedresult in actualresult:
                        	tdkTestObj.setResultStatus("SUCCESS");
				print "SUCCESS: Setting stereo mode value";
                	else:
                        	tdkTestObj.setResultStatus("FAILURE");
				print "FAILURE: Setting stereo mode value";

			#Calling DS_ManagerDeInitialize to DeInitialize API
			result = dsManagerDeInitialize(obj)

                	#Reboot the STB
                	obj.initiateReboot();

			#Calling Device Settings - initialize API
			result = dsManagerInitialize(obj)
			if "SUCCESS" in result:
                        	#calling DS_SetStereoMode to get the stereo mode
                        	tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                        	tdkTestObj.addParameter("port_name","SPDIF0");
                        	tdkTestObj.addParameter("get_only",1);
                        	expectedresult="SUCCESS"
                        	stereomode="SURROUND"
                        	tdkTestObj.executeTestCase(expectedresult);
                        	actualresult = tdkTestObj.getResult();
                        	stereomodedetails = tdkTestObj.getResultDetails();
				print "get mode: %s" %stereomodedetails;
                        	#Check for SUCCESS/FAILURE return value of DS_SetStereoMode
                        	if expectedresult in actualresult:
                                	#comparing stereo modes before and after setting
                                	if stereomode in stereomodedetails:
                                        	tdkTestObj.setResultStatus("SUCCESS");
                                        	print "SUCCESS: SURROUND Mode persisted for SPDIF after Reboot";
                                	else:
                                        	tdkTestObj.setResultStatus("FAILURE");
                                        	print "FAILURE: SURROUND Mode not persisted for SPDIF after Reboot";
                        	else:
                                	tdkTestObj.setResultStatus("FAILURE");
                               	 	print "FAILURE :Application failed to get the Stereomode for SPDIF";
                		#calling DS_ManagerDeInitialize to DeInitialize API 
				result = dsManagerDeInitialize(obj)
        	else:
                	print "SURROUND Mode not supported by audio port";
			#Calling Device Settings - DeInitialize API
			result = dsManagerDeInitialize(obj)

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
