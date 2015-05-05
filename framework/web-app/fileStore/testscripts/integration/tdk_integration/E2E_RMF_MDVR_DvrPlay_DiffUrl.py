'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1288</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>18</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_MDVR_DvrPlay_DiffUrl</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>583</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_MDVR_GetResult</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify that 2 client boxes [XI3] can playback 2 different recorded content on an XG1 box simultaneously without any issues.
Test Case ID : CT_MDVR_01</synopsis>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
import tdklib
import tdkintegration;
from tdklib import CreateTestThread

globalObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

# ## START ## Function to create recording for dvr playback
def createRecording(IP,PORT,args=(),kwargs={}):

   retValue = "FAILURE"

   #Test component to be tested
   obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

   #IP and Port of client box.
   ip = IP
   port = PORT
   obj.configureTestCase(ip,port,'TdkRmfApp_CreateRecord');

   #Get the result of connection with test component and STB
   result = obj.getLoadModuleResult();
   print "[LIB LOAD STATUS]  :  %s" %result;

   ##Check for SUCCESS/FAILURE of TDK Integration module
   if "SUCCESS" in result.upper():
       obj.setLoadModuleStatus("SUCCESS");
       print "rmfapp module load successful"

       recordId = str(kwargs["ID"])
       title = str(kwargs["TITLE"])
       duration = str(kwargs["DURATION"])
       ocapId = str(kwargs["OCAPID"])

       #Primitive test case which associated to this Script
       tdkTestObj = obj.createTestStep('TdkRmfApp_CreateRecording');

       tdkTestObj.addParameter("recordId",recordId);
       tdkTestObj.addParameter("recordDuration",duration);
       tdkTestObj.addParameter("recordTitle",title);
       tdkTestObj.addParameter("ocapId",ocapId);

       expectedresult="SUCCESS";

       #Execute the test case in STB
       tdkTestObj.executeTestCase(expectedresult);

       #Get the result and details of execution
       result = tdkTestObj.getResult();
       details = tdkTestObj.getResultDetails();
       print "Result: [%s] Details: [%s]"%(result,details)

       #Set the result status of execution
       if expectedresult in result.upper():
           tdkTestObj.setResultStatus("SUCCESS");
           retValue = "SUCCESS"
       else:
           tdkTestObj.setResultStatus("FAILURE");

       #unloading rmfapp module
       obj.unloadModule("rmfapp");
   else:
       obj.setLoadModuleStatus("FAILURE");
       print "Failed to load rmfapp module"

   return retValue

# ## END createRecording ##

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

   obj.configureTestCase(ip,port,'E2E_RMF_MDVR_DvrPlay_DiffUrl');

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

globalObj.configureTestCase(ip,port,'E2E_RMF_MDVR_DvrPlay_DiffUrl');

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
    if (clientsCount >= 2):

        clientIP = ip
        streamDetails = tdkTestObj.getStreamDetails('01');

        # Request for playing recorded content on client 1
        # Fetch recording of duration 1 min
        duration = 1
        recInfoAsList1 = tdkTestObj.getRecordingDetails(duration);
        recordID1 = recInfoAsList1[1]
        clientPORT1 = ClientListObj.getAgentPort(1)
        clientMAC1 = ClientListObj.getClientMACAddress(1)

        streamDetails1 = tdkTestObj.getStreamDetails('01');
	URL1 = tdkintegration.E2E_getStreamingURL(globalObj, "DVR" , streamDetails1.getGatewayIp() , recordID1[:-1]);
	if URL1 == "NULL":
		print "Failed to generate the Streaming URL";
		tdkTestObj.setResultStatus("FAILURE");
        thread1 = CreateTestThread(clientIP,clientPORT1,TDKE2E_mDVR_PlayUrl,kwargs={"URL":URL1,"MAC":clientMAC1})

        # Request for playing recorded content on client 2
        # Fetch recording of duration 2 mins
        streamDetails2 = tdkTestObj.getStreamDetails('02')
        duration = 2
        recInfoAsList2 = tdkTestObj.getRecordingDetails(duration);
        recordID2 = recInfoAsList2[1]
        clientPORT2 = ClientListObj.getAgentPort(2)
        clientMAC2 = ClientListObj.getClientMACAddress(2)

        URL2 = tdkintegration.E2E_getStreamingURL(globalObj, "DVR" , streamDetails2.getGatewayIp() , recordID2[:-1]);
        if URL2== "NULL":
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
