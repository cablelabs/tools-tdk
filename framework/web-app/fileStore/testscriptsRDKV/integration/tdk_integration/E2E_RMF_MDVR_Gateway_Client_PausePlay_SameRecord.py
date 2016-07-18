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
  <id>1542</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_MDVR_Gateway_Client_PausePlay_SameRecord</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>583</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_MDVR_GetResult</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify that when XG1 playback pause on the recorded content  try to playback the same recorded content in 2 client boxes from XG1. CT_MDVR_13</synopsis>
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
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
from tdklib import CreateTestThread
import tdkintegration;
globalObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

def TDKE2E_mDVR_Pause(IP,PORT,args=(),kwargs={}):

    print " TDKE2E_mDVR_LivePause called"
    retValue = "FAILURE"

    #Test component to be tested
    obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

    #IP and Port of client box.
    ip = IP
    port = PORT
    url = str(kwargs["URL"])
    macAdd = str(kwargs["MAC"])

    print "Box with IP: %s PORT: %d MAC Address: %s"%(ip,port,macAdd)

    obj.configureTestCase(ip,port,'E2E_RMF_MDVR_Gateway_Client_PausePlay_SameRecord');

    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[LIB LOAD STATUS in Client [%s]]  :  %s" %(macAdd,result);

    ##Check for SUCCESS/FAILURE of TDK Integration module
    if "SUCCESS" in result.upper():        
        
        obj.setLoadModuleStatus("SUCCESS");
        print "tdkintegration module load successful in client [%s]"%(macAdd);

        expectedresult="SUCCESS";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_Pause');

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

    obj.configureTestCase(ip,port,'E2E_RMF_MDVR_Gateway_Client_PausePlay_SameRecord');

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

globalObj.configureTestCase(ip,port,'E2E_RMF_MDVR_Gateway_Client_PausePlay_SameRecord');

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

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");
    # Fetch recording of duration 1 min
    duration = 4	
    #recInfoAsList = [index,recordingId,recordingTitle,duration,segmentName]
    recInfoAsList = tdkTestObj.getRecordingDetails(duration);
    if not recInfoAsList:
	        print "Recording details list is empty";
		tdkTestObj.setResultStatus("FAILURE");
    recordID = recInfoAsList[1]
    URL = tdkintegration.E2E_getStreamingURL(globalObj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1]);
    if URL == "NULL":
        print "Failed to generate the Streaming URL";
        tdkTestObj.setResultStatus("FAILURE");
                                      
    thread1 = CreateTestThread(ip,port,TDKE2E_mDVR_Pause,kwargs={"URL":URL,"MAC":ip})
   
    
    if (clientsCount >= 2):
        
        clientIP = ip
                                        
        # Request for live trick playing on client 1
        clientPORT1 = ClientListObj.getAgentPort(1)
        clientMAC1 = ClientListObj.getClientMACAddress(1)
      
        thread2 = CreateTestThread(clientIP,clientPORT1,TDKE2E_mDVR_PlayUrl,kwargs={"URL":URL,"MAC":clientMAC1})

        # Request for playing recorded content on client 2
        clientPORT2 = ClientListObj.getAgentPort(2)
        clientMAC2 = ClientListObj.getClientMACAddress(2)
 
      
        thread3 = CreateTestThread(clientIP,clientPORT2,TDKE2E_mDVR_PlayUrl,kwargs={"URL":URL,"MAC":clientMAC2})

        # Start the threads and wait for all threads to finish
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()
        

        try:
            print "Return status for gateway %s"%(thread1.returnValue)
            threadRetVal.append(thread1.returnValue)
        except AttributeError:
                                        
            print "Gateway failed to return status"
            threadRetVal.append("FAILURE")

        try:
            print "Return status for client [%s] = %s"%(clientMAC1,thread2.returnValue)
            threadRetVal.append(thread2.returnValue)
        except AttributeError:
            print "Client [%s] failed to return status"%(clientMAC1)
            threadRetVal.append("FAILURE")
        try:
            print "Return status for client [%s] = %s"%(clientMAC2,thread3.returnValue)
            threadRetVal.append(thread3.returnValue)
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
