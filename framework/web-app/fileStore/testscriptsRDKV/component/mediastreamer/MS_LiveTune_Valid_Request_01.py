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
  <id>231</id>
  <version>1</version>
  <name>MS_LiveTune_Valid_Request_01</name>
  <primitive_test_id>88</primitive_test_id>
  <primitive_test_name>MediaStreamer_LiveTune_Request</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This script tests Requesting Live Tune response of Mediastreamer.
Test Case ID:CT_Mediastreamer_01</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Mediastreamer_01</test_case_id>
    <test_objective>Mediastreamer – Requesting Live tuning playback via webservice interface</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1.Mediastreamer executable should be running</pre_requisite>
    <api_or_interface_used>Webservice Interface</api_or_interface_used>
    <input_parameters>string-ocapId</input_parameters>
    <automation_approch>1.TM loads Mediastreamer_agent via the test agent. 
2.TM gets an ocapid from the streaming details page of the FW and sends it to Mediastreamer_agent to generate request url.
3.Mediastreamer_agent will get RecorderId from wbdevice.dat file in XG1 and frames the query url for live tune like  “http://localhostip:port/videoStreamInit?recorderId=&amp;live=ocapid” and send to the mediastreamer. 
4.Upon receiving the Json response from mediastreamer, Mediastreamer_agent will extract the Json parameters like error code and error description and send to TM.
5.TM will do the error checking by verifying Error code and Error description parameters.</automation_approch>
    <except_output>Checkpoint 1 Error code and Error description parameter of Json response is verified as success or failure.</except_output>
    <priority>High</priority>
    <test_stub_interface>Mediastreamer_agent
1.TestMgr_MediaStreamer_LiveTune_Request</test_stub_interface>
    <test_script>MS_LiveTune_Valid_Request_01</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import re;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediastreamer","1.3");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_Mediastreamer_01');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaastreamer module loading status :%s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of Mediastreamer module
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS"); 

        print "Mediastreamer module loaded successfully";
        #Calling the MediaStreamer_LiveTune_Request function
        tdkTestObj = obj.createTestStep('MediaStreamer_LiveTune_Request');
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Adding ocapid parameter
        validid=streamDetails.getOCAPID();
        Id = re.search(r"(\w\w\w\w)", validid);
        if Id:
                print "ocapid : %s" %validid;
                tdkTestObj.addParameter("ocapId","ocap://"+validid);
                #Execute the test case in STB and pass the expected result
                expectedresult="0";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the actual result of execution
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                print "Live Tune Response of Json parameter : %s" %actualresult;
                #compare the actual result with expected result of Json response Parameter
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Json Response Parameter is success";
                        print "Live Tune description:Success";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Json response parameter is Failed";
                        print "Failure scenarios : %s" %details;
        else:
                print "getOcapId is failed";
                tdkTestObj.setResultStatus("FAILURE");
        #unloading mediastreamer module
        obj.unloadModule("mediastreamer");
else:
        print "Failed to load mediastreamer module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
