##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>Recorder_RMF_RWSOutage_CheckConnectionRetrial_64</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Check that after RWS Get and Post server outage recorder attempts no more than 1 concurrent connection with randomized  exponentially-longer retry intervals each time, to avoid overwhelming the server after a systemwide outage.</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <remarks>retrieveDisabledStatus api support for rws status server is removed from recorder</remarks>
  <skip>true</skip>
  <box_types>
    <box_type>Emulator-HYB</box_type>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Recoder_DVR_Protocol_64</test_case_id>
    <test_objective>Check that after RWS Get and Post server outage recorder attempts no more than 1 concurrent connection with randomized  exponentially-longer retry intervals each time, to avoid overwhelming the server after a systemwide outage.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,"FEATURE.RWS.GET.URL" and "FEATURE.RWS.POST.URL" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to RecorderAgent to generate request url.
3.RecorderAgent / Python lib interface will down the RWS GET and RSW Postserver URL 
4. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
5.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the list of recordings to check all current and future recordings</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_RWSOutage_CheckConnectionRetrial_64</test_script>
    <skipped>Yes</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import recorderlib
from time import sleep


#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_RWSOutage_CheckConnectionRetrial_64');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper());

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot();
               print "Sleeping to wait for the recoder to be up"
	       sleep(300);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
	recorderlib.callServerHandlerWithType('clearDisabledStatus','RWSStatus',ip)
	recorderlib.callServerHandlerWithType('clearDisabledStatus','RWSServer',ip)
        recorderlib.callServerHandler('clearStatus',ip)

        #Disable RWS status and RWS server
        recorderlib.callServerHandlerWithType('disableServer','RWSStatus',ip)
        status = recorderlib.callServerHandlerWithType('isEnabledServer','RWSStatus',ip)
        print "RWSStatus server status: ",status

        recorderlib.callServerHandlerWithType('disableServer','RWSServer',ip)
        status2 = recorderlib.callServerHandlerWithType('isEnabledServer','RWSServer',ip)
        print "RWSStatus server status: ",status2

        if( ("FALSE" in status.upper()) and ("FALSE" in status2.upper()) ):
                print "Waiting for 550s to get connection retrial attempts from recorder"
                sleep(550)

                #Checkpoint-1: Get the time between each re-trials
                print "Checking status of disabled servers"
                status = recorderlib.callServerHandlerWithType('retrieveDisabledStatus','RWSStatus',ip)
                print "RWSStatus server Status: ",status
                status2 = recorderlib.callServerHandlerWithType('retrieveDisabledStatus','RWSServer',ip)
                print "RWSserver Status: ",status2
                #Check if status is not empty
                if ( '[]' in status ):
                        print "ERROR: No status available for RWSStatus"
                        tdkTestObj.setResultStatus("FAILURE")
		elif ( '[]' in status2 ):
			print "ERROR: No status available for RWSServer"
			tdkTestObj.setResultStatus("FAILURE")
                else:
                        #Get retry interval for RWS status server
                        intervalPrev = 0
                        ret = recorderlib.getTimeListFromStatus(status)
                        print "RWS status server timelist = ",ret
                        if (1 == len(ret)):
                            tdkTestObj.setResultStatus("FAILURE")
                            print "Only one connection retry from recorder in 550s"
                        else:
                            for x in range(len(ret)-1):
                                intervalCurr = int( (ret[x+1] - ret[x])/1000 )
                                print "Retry interval for RWS status server: ",intervalCurr,"sec"
                                if intervalCurr <= intervalPrev:
                                        print "Retry interval for RWS status server not incrementing from ",intervalPrev,"sec to ",intervalCurr,"sec"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                        print "Retry interval for RWS status server incrementing from ",intervalPrev,"sec to ",intervalCurr,"sec"
                                intervalPrev = intervalCurr

                        #Get retry interval for RWSserver
                        intervalPrev = 0
                        ret = recorderlib.getTimeListFromStatus(status2)
                        print "RWS server timelist = ",ret
                        if (1 == len(ret)):
                            tdkTestObj.setResultStatus("FAILURE")
                            print "Only one connection retry from recorder in 550s"
                        else:
                            for x in range(len(ret)-1):
                                intervalCurr = int( (ret[x+1] - ret[x])/1000 )
                                print "Retry interval for RWSServer: ",intervalCurr,"sec"
                                if intervalCurr <= intervalPrev:
                                        print "Retry interval for RWSServer not incrementing from ",intervalPrev,"sec to ",intervalCurr,"sec"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                        print "Retry interval for RWSServer incrementing from ",intervalPrev,"sec to ",intervalCurr,"sec"
                                intervalPrev = intervalCurr

                #Checkpoint-2: Check no status from both RWS status and RWS Server
                response = recorderlib.callServerHandler('retrieveStatus',ip);
                print "response = ",response
                if 'RWSStatus' in response:
                        print "Recorder communicated with RWSStatus in disabled state"
                        tdkTestObj.setResultStatus("FAILURE")
		elif 'RWSServer' in response:
			print "Recorder communicated with RWSServer in disabled state"
			tdkTestObj.setResultStatus("FAILURE")
                else:
                        print "Recorder did not communicate with RWSStatus or RWSServer in disabled state as expected"

                #post-req: Enable RWSStatus
                recorderlib.callServerHandlerWithType('enableServer','RWSStatus',ip)
                status = recorderlib.callServerHandlerWithType('isEnabledServer','RWSStatus',ip)
                print "RWSStatus server status: ",status

                recorderlib.callServerHandlerWithType('enableServer','RWSServer',ip)
                status2 = recorderlib.callServerHandlerWithType('isEnabledServer','RWSServer',ip)
                print "RWS server status: ",status2

                if "FALSE" in status.upper():
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to enable RWS status Server"
		elif "FALSE" in status2.upper():
			tdkTestObj.setResultStatus("FAILURE");
			print "Failed to enable RWS Server"
                else:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Enabled RWS status and RWS Server"
        else:
                print "Failed to disable RWS status or RWS Server. Exiting.."
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        recObj.unloadModule("Recorder");
