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
  <id>1284</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>8</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_MDVR_LivePlay_DvrPlay</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>583</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_MDVR_GetResult</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify that 2 client boxes [XI3] connected to an XG1 box can perform live trickplay on one client box and playback recorded content on another client box simultaneously.
Test Case ID : CT_MDVR_05</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
  <script_tags>
    <script_tag>BASIC</script_tag>
    <!--  -->
  </script_tags>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import tdkintegration;
from tdklib import CreateTestThread

globalObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

# ## START ## Function for dvr playback or live trickplay
def TDKE2E_mDVR_PlayUrl(IP,PORT,args=(),kwargs={}):

   print "TDKE2E_mDVR_PlayUrl called"
   retValue = "FAILURE"

   #Test component to be tested
   obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

   #IP and Port of client box.
   ip = IP
   port = PORT
   url = str(kwargs["URL"])
   macAdd = str(kwargs["MAC"])

   print "Box with IP: %s PORT: %d MAC Address: %s"%(ip,port,macAdd)

   obj.configureTestCase(ip,port,'E2E_RMF_MDVR_LivePlay_DvrPlay');

   #Get the result of connection with test component and STB
   result = obj.getLoadModuleResult();
   print "[LIB LOAD STATUS in Client [%s]]  :  %s" %(macAdd,result);

   ##Check for SUCCESS/FAILURE of TDK Integration module
   if "SUCCESS" in result.upper():
       obj.setLoadModuleStatus("SUCCESS");
       print "tdkintegration module load successful in client [%s]"%(macAdd);

       expectedresult="SUCCESS";
       #Prmitive test case which associated to this Script
       tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

       print "Client [%s] Play Url Requested: %s"%(macAdd,url)
       tdkTestObj.addParameter("playUrl",url);

       #Execute the test case in STB
       tdkTestObj.executeTestCase(expectedresult);

       #Get the result of execution
       actualresult = tdkTestObj.getResult();
       details = tdkTestObj.getResultDetails();
       print "[TEST EXECUTION RESULT in CLIENT [%s]] : %s"%(macAdd,actualresult);

       #Set the result status of execution
       if "SUCCESS" in actualresult.upper():
           tdkTestObj.setResultStatus("SUCCESS");
           print "Execution in Client [%s] Successful: [%s]"%(macAdd,details);
           retValue = "SUCCESS"
       else:
           tdkTestObj.setResultStatus("FAILURE");
           print "Execution in Client [%s] Failed: [%s]"%(macAdd,details);

       #unloading tdkintegration module
       obj.unloadModule("tdkintegration");
   else:
       obj.setLoadModuleStatus("FAILURE");
       print "Failed to load tdkintegration module in Client [%s]"%(macAdd);

   return retValue

# ## END TDKE2E_mDVR_PlayUrl ##

#IP and Port of DVR box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

globalObj.configureTestCase(ip,port,'E2E_RMF_MDVR_LivePlay_DvrPlay');

#Get the result of connection with test component and STB
result =globalObj.getLoadModuleResult();
print "[LIB LOAD STATUS in Gateway]  :  %s" %result;
loadmoduledetails = globalObj.getLoadModuleDetails();

#Reboot if rmfstreamer is not running
if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                globalObj.initiateReboot();
                #Reload Test component to be tested
                globalObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                globalObj.configureTestCase(ip,port,'E2E_RMF_MDVR_LivePlay_DvrPlay');
                #Get the result of connection with test component and STB
                result =globalObj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails;
                print "Tdkintegration module loading status :  %s" %result;
#Check for SUCCESS/FAILURE of module load
if "SUCCESS" in result.upper():
    globalObj.setLoadModuleStatus("SUCCESS");
    #Primitive test case which associated to this Script
    tdkTestObj = globalObj.createTestStep('TDKE2E_MDVR_GetResult');

    # Call tdklib interface to get port number and mac address of the client devices under test
    clientlist = <clientlist>
    ClientListObj = tdklib.ClientList(clientlist)

    #Find total number of available clients
    clientsCount = ClientListObj.getNumberOfClientDevices()
    print "Detected %d client(s) connected"%(clientsCount)

    threadRetVal = []
    if (clientsCount >= 2):

        clientIP = ip

        # Request for live trick playing on client 1
        clientPORT1 = ClientListObj.getAgentPort(1)
        clientMAC1 = ClientListObj.getClientMACAddress(1)
   
        streamDetails = tdkTestObj.getStreamDetails('01');
        URL1 = tdkintegration.E2E_getStreamingURL(globalObj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if URL1 == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
        thread1 = CreateTestThread(clientIP,clientPORT1,TDKE2E_mDVR_PlayUrl,kwargs={"URL":URL1,"MAC":clientMAC1})

        # Request for playing recorded content on client 2
        clientPORT2 = ClientListObj.getAgentPort(2)
        clientMAC2 = ClientListObj.getClientMACAddress(2)

        
        duration = 4	
        #recInfoAsList = [index,recordingId,recordingTitle,duration,segmentName]
        recInfoAsList = tdkTestObj.getRecordingDetails(duration);
        if not recInfoAsList:
	        print "Recording details list is empty";
		tdkTestObj.setResultStatus("FAILURE");
        recordID = recInfoAsList[1]
    
	URL2 = tdkintegration.E2E_getStreamingURL(globalObj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1]);
	if URL2 == "NULL":
		print "Failed to generate the Streaming URL";
		tdkTestObj.setResultStatus("FAILURE");	
        thread2 = CreateTestThread(clientIP,clientPORT2,TDKE2E_mDVR_PlayUrl,kwargs={"URL":URL2,"MAC":clientMAC2})

        # Start the threads and wait for all threads to finish
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        try:
                print "Return status for client [%s] = %s"%(clientMAC1,thread1.returnValue)
                threadRetVal.append(thread1.returnValue)
        except AttributeError:
                print "Client [%s] failed to return status"%(clientMAC1)
                threadRetVal.append("FAILURE")
        try:
                print "Return status for client [%s] = %s"%(clientMAC2,thread2.returnValue)
                threadRetVal.append(thread2.returnValue)
        except AttributeError:
                print "Client [%s] failed to return status"%(clientMAC2)
                threadRetVal.append("FAILURE")

        print "Execution results for all clients: ",
        print threadRetVal

        #Get the result of execution
        if "FAILURE" in threadRetVal:
                details = "One or more clients failed to execute successfully"
        else:
                details = "All Clients executed successfully"
    else:
        threadRetVal.append("FAILURE")
        details = "Pre-Condition not met. Connect atleast two client boxes in MoCA network"

    expectedresult="SUCCESS";

    resList = ''.join(threadRetVal)

    tdkTestObj.addParameter("resultList",resList);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
    resDetails = tdkTestObj.getResultDetails();

    print "[TEST EXECUTION RESULT in Gateway] : %s"%actualresult
    print "[TEST EXECUTION DETAILS in Gateway] : %s"%resDetails

    #Set the result status of execution
    if "SUCCESS" in actualresult.upper():
       tdkTestObj.setResultStatus("SUCCESS");
       print "Execution Successful in Gw : [%s]"%details
    else:
       tdkTestObj.setResultStatus("FAILURE");
       print "Execution Failed in Gw: [%s]"%details

    #unloading mediastreamer module
    globalObj.unloadModule("tdkintegration");
else:
    print "Failed to load tdkintegration module";
    globalObj.setLoadModuleStatus("FAILURE");
