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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Delete_Lastid_And_Check_Recordings_Legacy_283</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Reboot the box after removing lastid.dat file from recdbser folder and reboot.All the recordings  should be available in box</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>60</execution_time>
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
  <script_tags />
</xml>
'''
#use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import recorderlib
from random import randint
from time import sleep


#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Delete_Lastid_And_Check_Recordings_Legacy_283');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper())

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       print "Sleeping to wait for the recoder to be up"
	       sleep(300);

	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
	sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        expectedResult="SUCCESS";
        tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
        tdkTestObj1.executeTestCase(expectedResult);
        recorderlib.callServerHandlerWithMsg('updateMessage','{\"getRecordings\":{}}',ip)
        print "Wait for 1 min to get response from recorder"
        sleep(60);
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
        print "Recordings in the box before reboot" , actResponse;
        totalrec_before = recorderlib.getTotalNumberofRecordings(actResponse)
        print "Total number of recordings before reboot " ,totalrec_before
        
        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_ExecuteCmd');
        tdkTestObj.addParameter("command","rm /tmp/mnt/diska3/persistent/dvr/recdbser/lastid.dat");
        #Execute the test case in STB
        tdkTestObj.executeTestCase("SUCCESS");
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "lastid.dat file deleted succesfully"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "lastid.dat file NOT deleted"
        sleep(30);
       
        # Reboot the STB
        print "Rebooting the STB"
        recObj.initiateReboot();
        print "Sleeping to wait for the recoder to be up"
        sleep(300);
        tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
        tdkTestObj1.executeTestCase(expectedResult);
        response = recorderlib.callServerHandler('clearStatus',ip);
        recorderlib.callServerHandlerWithMsg('updateMessage','{\"getRecordings\":{}}',ip)
        print "Wait for 1 min to get response from recorder"
        sleep(60);
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
        print "Recordings in the box after reboot " , actResponse;
        totalrec_after = recorderlib.getTotalNumberofRecordings(actResponse)
        print "Total number of recordings after reboot " ,totalrec_after
        if totalrec_before <= totalrec_after:
            tdkTestObj1.setResultStatus("SUCCESS");
            print "No recordings got deleted"
        else:
          tdkTestObj1.setResultStatus("FAILURE");
          print "Recordings got deleted"

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module"
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");

