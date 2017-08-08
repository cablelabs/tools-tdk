# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id>1283</id>
  <version>1</version>
  <name>E2E_RMF_MDVR_Max_LivePlay</name>
  <primitive_test_id>583</primitive_test_id>
  <primitive_test_name>TDKE2E_MDVR_GetResult</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To verify that 3 client boxes [XI3] can perform live trickplay of same channel on a single XG1 box simultaneously without any issues.
Test Case ID : CT_MDVR_06</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_MDVR_06</test_case_id>
    <test_objective>To verify that 3 client boxes [XI3] can perform live trickplay of same channel on a single XG1 box simultaneously without any issues.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1, XI3-3</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. XG1 is connected to XI3 client boxes.    
2. XG1 &amp; all XI3 boxes should be up &amp; running.</input_parameters>
    <automation_approch>1) Connect 3 client boxes (XI3) through XG1.
2) Agent will be running in all the XI3 and XG1 box.
3) TM frames a request url with ocapId of the channel to be tuned for live trickplay and passes it to XI3 agents simultaneously to play through mplayer.
4) TM reads Success or Failure message from each connected client and sends final result.</automation_approch>
    <except_output>Checkpoint 1.Check the return values of API's from each XI3 for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtdkintegrationstub.so</test_stub_interface>
    <test_script>E2E_RMF_MDVR_Max_LivePlay</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import tdkintegration;
from tdklib import CreateTestThread

globalObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

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

   obj.configureTestCase(ip,port,'E2E_RMF_MDVR_Max_LivePlay');

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


#IP and Port of DVR box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

globalObj.configureTestCase(ip,port,'E2E_RMF_MDVR_Max_LivePlay');

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
                globalObj.configureTestCase(ip,port,'E2E_RMF_MDVR_Max_LivePlay');
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

    if (clientsCount < 3):
        details = "Pre-Condition not met. Connect three client boxes"
        threadRetVal.append("FAILURE")
    else:
        threads = []
        for threadNum in range(clientsCount):
                # Get Client port number and mac address
                clientIP = ip
                clientPORT = ClientListObj.getAgentPort(threadNum+1)
                clientMAC = ClientListObj.getClientMACAddress(threadNum+1)

                # Frame different request URL for each client box
                streamId='0'+str(threadNum+1)
                streamDetails = tdkTestObj.getStreamDetails(streamId);
		URL = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
		if URL == "NULL":
		    print "Failed to generate the Streaming URL";
		    tdkTestObj.setResultStatus("FAILURE");

                # Create a new thread for each client
                thread = CreateTestThread(clientIP,clientPORT,TDKE2E_mDVR_PlayUrl,kwargs={"URL":URL,"MAC":clientMAC})
                # Append thread to threads
                threads.append(thread)
                # Start thread
                thread.start()

        for t in threads:
                # Wait for all threads to finish
                t.join()
                try:
                        print "Return status for client [%s] = %s"%(clientMAC,thread.returnValue)
                        # Append thread return value to threadRetVal
                        threadRetVal.append(thread.returnValue)
                except AttributeError:
                        print "Client [%s] failed to return status"%(clientMAC)
                        threadRetVal.append("FAILURE")

        print "Execution results for all clients: ",
        print threadRetVal

        #Get the result of execution
        if "FAILURE" in threadRetVal:
                details = "One or more clients failed to execute successfully"
        else:
                details = "All Clients executed successfully"

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
