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
  <id>1289</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_MDVR_Max_ScheduleRecording</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>583</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_MDVR_GetResult</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify that upto 3 client boxes  [XI3] can schedule recordings of 3 different channels on a single XG1 box simultaneously without any issues.
Test Case Id: CT_MDVR_07</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This test causes the RMFStreamer to crash and reboot the box. This is a bug in RDK</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
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
import tdklib
import tdkintegration;
from tdklib import CreateTestThread

globalObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

def TDKE2E_Schedule_Recording(IP,PORT,args=(),kwargs={}):

   print "TDKE2E_Schedule_Recording called"
   retValue = "FAILURE"

   #Test component to be tested
   obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

   #IP and Port of client box.
   ip = IP
   port = PORT
   url = str(kwargs["URL"])
   macAdd = str(kwargs["MAC"])

   print "Box with IP: %s PORT: %d MAC Address: %s"%(ip,port,macAdd)

   obj.configureTestCase(ip,port,'E2E_RMF_MDVR_Max_ScheduleRecording');

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

globalObj.configureTestCase(ip,port,'E2E_RMF_MDVR_Max_ScheduleRecording');

#Get the result of connection with test component and STB
result =globalObj.getLoadModuleResult();
print "[LIB LOAD STATUS in Gateway]  :  %s" %result;

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
                thread = CreateTestThread(clientIP,clientPORT,TDKE2E_Schedule_Recording,kwargs={"URL":URL,"MAC":clientMAC})
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
