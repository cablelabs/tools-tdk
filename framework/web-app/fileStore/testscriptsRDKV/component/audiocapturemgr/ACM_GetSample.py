##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>ACM_GetSample</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>AudioCaptureMgr_Session_Open</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify that audio sample is captured</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
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
  <test_cases>
    <test_case_id>CT_ACM_15</test_case_id>
    <test_objective>To verify that audio sample is captured</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xg1v3</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_OPEN, (void *) &amp;param, sizeof(param))
IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_START, (void *) &amp;param, sizeof(param))
IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_STOP, (void *) &amp;param, sizeof(param))
IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_CLOSE, (void *) &amp;param, sizeof(param))</api_or_interface_used>
    <input_parameters>iarmbus_acm_arg_t param</input_parameters>
    <automation_approch>1. TM loads the AudioCaptureMgr agent via the test agent.
2. AudioCaptureMgr agent will invoke the IARM_Bus_Call for IARMBUS_AUDIOCAPTUREMGR_OPEN
3. AudiCaptureMgr agent will invoke the IARM_Bus_Call for IARMBUS_AUDIOCAPTUREMGR_START
4. AudiCaptureMgr agent will invoke the IARM_Bus_Call for IARMBUS_AUDIOCAPTUREMGR_STOP after a delay
5. AudiCaptureMgr agent will invoke the IARM_Bus_Call for IARMBUS_AUDIOCAPTUREMGR_CLOSE
6. Check if the output file is created and the file size is non zero and return SUCCESS/FAILURE</automation_approch>
    <except_output>Checkpoint 1.Verify the IARMBUS calls are SUCCESS 
Checkpoint 2.Verify the output file is created and value is non zero</except_output>
    <priority>High</priority>
    <test_stub_interface>libaudiocapturemgrstub.so</test_stub_interface>
    <test_script>ACM_GetSample</test_script>
    <skipped>No</skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from iarmbus import IARMBUS_Init,IARMBUS_Connect,IARMBUS_DisConnect,IARMBUS_Term;
from time import sleep;
import os;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");
iarmObj.configureTestCase(ip,port,'ACM_GetSample');

def getOutputProperties():
	properties = "";
	#Prmitive test case which associated to this Script
	tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_GetOutputProperties');

	#Execute the test case in STB
	expectedresult="SUCCESS"
	tdkTestObj.executeTestCase(expectedresult);

	#Get the result of execution
	actualresult = tdkTestObj.getResult();
	print "[TEST EXECUTION RESULT] : %s" %actualresult;


	#Set the result status of execution
	if expectedresult in actualresult:
		properties = tdkTestObj.getResultDetails();
		print "Output Properties: %s"%properties;
		tdkTestObj.setResultStatus("SUCCESS");
		print "Output Properties retrieved";
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Failed to retrieve Output Properties";

	return properties;

def acmStartStop(action):
	status = "";
        #Prmitive test case which associated to this Script
        tdkTestObj = acmObj.createTestStep(action);

        #Execute the test case in STB
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %actualresult;

	status = tdkTestObj.getResultDetails();
	print status;

        #Set the result status of execution
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
        else:
                tdkTestObj.setResultStatus("FAILURE");

        return actualresult,status;


#Get the result of connection with test component and STB
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "Iarmbus module loading status : %s" %iarmLoadStatus ;
#Set the module loading status
iarmObj.setLoadModuleStatus(iarmLoadStatus);

if "SUCCESS" in iarmLoadStatus.upper():
        #Calling IARMBUS API "IARM_Bus_Init"
        result = IARMBUS_Init(iarmObj,"SUCCESS")
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if "SUCCESS" in result:
                #Calling IARMBUS API "IARM_Bus_Connect"
                result = IARMBUS_Connect(iarmObj,"SUCCESS")
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
                if "SUCCESS" in result:
                        #Test component to be tested
                        acmObj = tdklib.TDKScriptingLibrary("audiocapturemgr","1");
                        acmObj.configureTestCase(ip,port,'ACM_GetSample');

                        #Get the result of connection with test component and STB
                        acmLoadStatus = acmObj.getLoadModuleResult();
                        print "[LIB LOAD STATUS]  :  %s" %acmLoadStatus;
                        #Set the module loading status
                        acmObj.setLoadModuleStatus(acmLoadStatus);

                        if "SUCCESS" in acmLoadStatus.upper():
				tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_ExecuteCmd');
        			tdkTestObj.addParameter("command","source /opt/TDK/StartTDK.sh > /dev/null 2>&1 &");
			        expectedresult = "SUCCESS"
			        tdkTestObj.executeTestCase(expectedresult);
				actualresult = tdkTestObj.getResult();
				if expectedresult in actualresult:
					filename = "";
					tdkTestObj.setResultStatus("SUCCESS");
					print "AudioCaptureMgr_ExecuteCmd call is successful";
					tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_ExecuteCmd');
					streamDetails = tdkTestObj.getStreamDetails('02');
					print "OCAPID: ",streamDetails.getOCAPID();
					tdkTestObj.addParameter("command","tdkRmfApp play  -l ocap://"+streamDetails.getOCAPID()+" > /dev/null 2>&1 &");
					expectedresult = "SUCCESS"
					tdkTestObj.executeTestCase(expectedresult);
					actualresult = tdkTestObj.getResult();
					if expectedresult in actualresult:
						tdkTestObj.setResultStatus("SUCCESS");
						print "Invoked tdkRmfApp play";

						#Prmitive test case which associated to this Script
						tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_Session_Open');

						#Execute the test case in STB
						expectedresult="SUCCESS"
						tdkTestObj.executeTestCase(expectedresult);

						#Get the result of execution
						actualresult = tdkTestObj.getResult();
						print "[TEST EXECUTION RESULT] : %s" %actualresult;

						#Set the result status of execution
						if expectedresult in actualresult:
							sessionId = tdkTestObj.getResultDetails();
							print "Session ID: %s"%sessionId;
							if sessionId == -1:
								tdkTestObj.setResultStatus("FAILURE");
								print "Failed to open AudioCaptureMgr session";
							else:
								tdkTestObj.setResultStatus("SUCCESS");
								print "AudioCaptureMgr session opened successfully";

								socketPath = getOutputProperties();
								if socketPath != "":
									startStatus,details = acmStartStop('AudioCaptureMgr_Start');
									if startStatus == "SUCCESS":
										filename = details;
										sleep(20);
										stopStatus,details = acmStartStop('AudioCaptureMgr_Stop');
									
								#Prmitive test case which associated to this Script
								tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_Session_Close');

								#Execute the test case in STB
								expectedresult="SUCCESS"
								tdkTestObj.executeTestCase(expectedresult);

								#Get the result of execution
								actualresult = tdkTestObj.getResult();
								print "[TEST EXECUTION RESULT] : %s" %actualresult;

								#Set the result status of execution
								if expectedresult in actualresult:
									tdkTestObj.setResultStatus("SUCCESS");
									print "AudioCaptureMgr session closed successfully";
									if filename != "":
										print "FILENAME: ", filename;
										tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_ExecuteCmd');
										tdkTestObj.addParameter("command","stat -c \"%s\" /opt/TDK/tmp/acm_ipout_dump");
										expectedresult = "SUCCESS"
										tdkTestObj.executeTestCase(expectedresult);
										actualresult = tdkTestObj.getResult();
										if expectedresult in actualresult:
											tdkTestObj.setResultStatus("SUCCESS");
											details = tdkTestObj.getResultDetails();
											print "FILE SIZE DETAILS: ", details;
											if "No such file or directory" not in details: 
												details = details.rstrip('\\n');
												if int(details) > 0:
													tdkTestObj.setResultStatus("SUCCESS");
	                                                                                                print "Output file created and size is non zero";
												else:
                                                                                                	tdkTestObj.setResultStatus("FAILURE")
	                                                                                                print "Output file size is zero";
											
								else:
									tdkTestObj.setResultStatus("FAILURE");
									print "Failed to close AudioCaptureMgr session";
						else:
							tdkTestObj.setResultStatus("FAILURE");
							print "Call to open AudioCaptureMgr session failed";
							
					else:
						tdkTestObj.setResultStatus("FAILURE");
						print "Command to play tdkRmfApp failed";
				else:
					tdkTestObj.setResultStatus("FAILURE");
					print "Command to source failed";
				
						

                                acmObj.unloadModule("audiocapturemgr");

                        else :
                                print "Failed to Load audiocapturemgr Module "

                        #Calling IARM_Bus_DisConnect API
                        result = IARMBUS_DisConnect(iarmObj,"SUCCESS")
                #calling IARMBUS API "IARM_Bus_Term"
                result = IARMBUS_Term(iarmObj,"SUCCESS")
        #Unload iarmbus module
        iarmObj.unloadModule("iarmbus");

