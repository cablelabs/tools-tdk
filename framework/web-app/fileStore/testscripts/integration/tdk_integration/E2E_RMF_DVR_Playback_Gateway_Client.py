'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_Playback_Gateway_Client</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>556</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_Rmf_LinearTv_Dvr_Play</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Tests if creating 4 recordings on XG1 and playing it on XG1 and connected client box at the same time is successful.
Testcase ID:</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import tdkintegration;
from tdklib import CreateTestThread
from mediaframework import createRecording,deleteRecording;
from random import randint

# ## START ## Function for dvr playback or live trickplay
# Input Params : kwargs={'trickplay','STREAMID'} for LinearTv
#                kwargs={'STREAMID','ID'} for DVR playback
#
# Return Value : "SUCCESS"/"FAILURE"
#
def TDKE2E_PlayUrl(IP,PORT,args=(),kwargs={}):

   retValue = "FAILURE"

   #Test component to be tested
   obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

   #IP and Port of client box.
   ip = IP
   port = PORT

   streamId = str(kwargs["STREAMID"])

   obj.configureTestCase(ip,port,'E2E_RMF_DVR_Playback_Gateway_Client');

   #Get the result of connection with test component and STB
   result = obj.getLoadModuleResult();
   print "[LIB LOAD STATUS : %s" %(result);
   obj.setLoadModuleStatus(result);

   ##Check for SUCCESS/FAILURE of TDK Integration module
   if "SUCCESS" in result.upper():
        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

        streamDetails = tdkTestObj.getStreamDetails(streamId)
        if 'trickplay' in kwargs.values():
		url = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
		if url == "NULL":
		    print "Failed to generate the Streaming URL";
		    tdkTestObj.setResultStatus("FAILURE");
                print "URL for trickplay : %s"%url
        else:
                recordId = str(kwargs["ID"])
		url = tdkintegration.E2E_getStreamingURL(obj, "DVR" , streamDetails.getGatewayIp() , recordId);
		if url == "NULL":
			print "Failed to generate the Streaming URL";
			tdkTestObj.setResultStatus("FAILURE");
                print "URL for DVR playback : %s"%url

        tdkTestObj.addParameter("playUrl",url);

        expectedresult="SUCCESS";

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Result: [%s], Details: [%s]"%(actualresult,details);

        #Set the result status of execution
        if "SUCCESS" in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");

        #unloading tdkintegration module
        obj.unloadModule("tdkintegration");

   return retValue

# ## END TDKE2E_PlayUrl ##

#IP and Port of DVR box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

# Call tdklib interface to get port number of the client devices under test
clientlist = <clientlist>
ClientListObj = tdklib.ClientList(clientlist)
#Find total number of available clients
clientsCount = ClientListObj.getNumberOfClientDevices()
print "Detected %d client(s) connected to Gateway box"%clientsCount

if (clientsCount < 1):
        print "Pre-Condition not met. Connect atleast one XI3 to XG1 in MoCA network"
else:
        # Load Modules in X1
        mfX1Obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
        mfX1Obj.configureTestCase(ip,port,'E2E_RMF_DVR_Playback_Gateway_Client');

        # tdkintegration library is loaded in X1 to get result from Xi3 and send to test manager
        tdkIntX1Obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
        tdkIntX1Obj.configureTestCase(ip,port,'E2E_RMF_DVR_Playback_Gateway_Client');

        # Check module load status in X1
        mfX1LoadStatus = mfX1Obj.getLoadModuleResult();
        print "[mediaframework LIB LOAD STATUS in X1] : %s"%mfX1LoadStatus;
        mfX1Obj.setLoadModuleStatus(mfX1LoadStatus);

	mfX1LoadDetails = mfX1Obj.getLoadModuleDetails();
	if "FAILURE" in mfX1LoadStatus.upper():
        	if "RMF_STREAMER_NOT_RUNNING" in mfX1LoadDetails:
                	print "rmfStreamer is not running. Rebooting STB"
                	mfX1Obj.initiateReboot();
	                #Reload Test component to be tested
        	        mfX1Obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                	mfX1Obj.configureTestCase(ip,port,'E2E_RMF_DVR_Playback_Gateway_Client');
	                #Get the result of connection with test component and STB
			mfX1LoadStatus = mfX1Obj.getLoadModuleResult();
	                print "Re-Load Module Status :  %s" %mfX1LoadStatus;
			mfX1LoadDetails = mfX1Obj.getLoadModuleDetails();
        	        print "Re-Load Module Details : %s" %mfX1LoadDetails;

        # tdkintegration lib is loaded in XG1 only to get the result of DVR play on XI3
        tdkIntX1LoadStatus = tdkIntX1Obj.getLoadModuleResult();
        print "[tdkintegration LIB LOAD STATUS in X1] : %s"%tdkIntX1LoadStatus;
        tdkIntX1Obj.setLoadModuleStatus(tdkIntX1LoadStatus);

        if ('SUCCESS' not in mfX1LoadStatus.upper()) and ('SUCCESS' in tdkIntX1LoadStatus.upper()):
            tdkIntX1Obj.unloadModule("tdkintegration");
            exit();
        elif ('SUCCESS' in mfX1LoadStatus.upper()) and ('SUCCESS' not in tdkIntX1LoadStatus.upper()):
            mfX1Obj.unloadModule("mediaframework");
            exit();

        #Port of client box.
        xi3_port = ClientListObj.getAgentPort(1)
        print "Client IP=%s PORT=%d"%(ip,xi3_port)

        # Step1: Record stream1 on X1 and tune to same channel on XI3
        Id = randint(1000,10000)
        recordingId1 = str(Id)
        title = 'test_dvr_'+recordingId1
        duration = '1'
        streamId1 = '01'

        #Record stream1 on XG1
        result = createRecording(mfX1Obj,kwargs={"ID":recordingId1,"TITLE":title,"DURATION":duration,"STREAMID":streamId1})
        print "Recording stream %s is %s"%(streamId1,result)

        #Tune to stream1 on XI3
        playXI3Thread = CreateTestThread(ip,xi3_port,TDKE2E_PlayUrl,kwargs={'play':'trickplay',"STREAMID":streamId1})

        # Start the thread and wait for thread to finish
        playXI3Thread.start()
        playXI3Thread.join()

        try:
                print "Return status for tuning on XI3: [%s]"%(playXI3Thread.returnValue)
                threadRes = playXI3Thread.returnValue
        except AttributeError:
                print "Failed to return status for tuning on XI3"
                threadRes = "FAILURE"

        #Primitive test case which associated to this Script
        tdkIntX1TestObj = tdkIntX1Obj.createTestStep('TDKE2E_MDVR_GetResult');
        tdkIntX1TestObj.addParameter("resultList",threadRes);
        tdkIntX1TestObj.executeTestCase("SUCCESS");

        #Get the result of execution
        actualresult = tdkIntX1TestObj.getResult();

        #Set the result status of execution
        if "SUCCESS" in actualresult.upper():
            tdkIntX1TestObj.setResultStatus("SUCCESS");
            print "Execution Successful in Xi3"
        else:
            tdkIntX1TestObj.setResultStatus("FAILURE");
            print "Execution Failed in Xi3"

        if ("SUCCESS" in result.upper()) and ("SUCCESS" not in actualresult.upper()):
            deleteRecording(mfX1Obj,kwargs={"ID":recordingId1,"STREAMID":streamId1})
        elif ("SUCCESS" not in result.upper()) and ("SUCCESS" in actualresult.upper()):
            print "Failed to create first recording in X1"
        elif "SUCCESS" in actualresult.upper():
            # Step2: Record stream 2 to 4 in X1
            for idNum in range(2,5):
                Id = randint(1000,10000)
                recordingId = str(Id)
                title = 'test_dvr_'+recordingId
                duration = '1'
                streamId='0'+str(idNum)
                result = createRecording(mfX1Obj,kwargs={"ID":recordingId,"TITLE":title,"DURATION":duration,"STREAMID":streamId})
                print "Recording stream %s is %s"%(streamId,result)

            # Step3: Playback recording 1 to 4 in X1 and XI3
            # Playback recording 1 to 4 in X1
            for idNum in range(1,5):
                recordingId = 'recordingId'+str(idNum)
                streamId = 'streamId'+str(idNum)
                result = TDKE2E_PlayUrl(ip,port,kwargs={"ID":recordingId,"STREAMID":streamId})
                print "Playback %s is %s"%(recordingId,result)

            # Playback recording 1 to 4 in XI3
            threadRetVal = []
            for threadNum in range(1,5):
                recordingId = 'recordingId'+str(threadNum)
                streamId = 'streamId'+str(threadNum)
                playXI3Thread = CreateTestThread(ip,xi3_port,TDKE2E_PlayUrl,kwargs={"ID":recordingId,"STREAMID":streamId})
                # Start thread
                playXI3Thread.start()
                playXI3Thread.join()
            try:
                print "Return status of playback %s on XI3: [%s]"%(recordingId,playXI3Thread.returnValue)
                # Append thread return value to threadRetVal
                threadRetVal.append(thread.returnValue)
            except AttributeError:
                print "%s failed to return status"%(recordingId)
                threadRetVal.append("FAILURE")

            resList = ''.join(threadRetVal)
            print "Execution results for all clients: ",
            print threadRetVal

            expectedresult="SUCCESS";
            tdkIntX1TestObj.addParameter("resultList",resList);

            #Execute the test case in STB
            tdkIntX1TestObj.executeTestCase(expectedresult);

            #Get the result of execution
            actualresult = tdkIntX1TestObj.getResult();
            resDetails = tdkIntX1TestObj.getResultDetails();

            print "[Playback Result on XI3] : %s"%actualresult
            print "[Playback Details on XI3] : %s"%resDetails

            #Set the result status of execution
            if "SUCCESS" in actualresult.upper():
                tdkIntX1TestObj.setResultStatus("SUCCESS");
            else:
                tdkIntX1TestObj.setResultStatus("FAILURE");

            # Post-Condition: Delete recordings 1 to 4 on X1
            for idNum in range(1,5):
                recordingId = 'recordingId'+str(idNum)
                streamId = 'streamId'+str(idNum)
                deleteRecording(mfX1Obj,kwargs={"ID":recordingId,"STREAMID":streamId})

        #unloading modules
        mfX1Obj.unloadModule("mediaframework");
        tdkIntX1Obj.unloadModule("tdkintegration");
