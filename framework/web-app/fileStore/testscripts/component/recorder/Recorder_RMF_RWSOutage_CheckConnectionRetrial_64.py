'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_RWSOutage_CheckConnectionRetrial_64</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check that after RWS Get and Post server outage recorder attempts no more than 1 concurrent connection with randomized  exponentially-longer retry intervals each time, to avoid overwhelming the server after a systemwide outage.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
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
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

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
                print "Waiting to get connection retrial attempts from recorder"
                sleep(550)

                #Checkpoint-1: Get the time between each re-trials
                print "Checking status of disabled servers"
                status = recorderlib.callServerHandlerWithType('retrieveDisabledStatus','RWSStatus',ip)
                print "RWSStatus server Status: ",status
                status2 = recorderlib.callServerHandlerWithType('retrieveDisabledStatus','RWSServer',ip)
                print "RWSserver Status: ",status2
                #Check if status is not empty
                if ( [] == status ):
                        print "ERROR: No status available for RWSStatus"
                        tdkTestObj.setResultStatus("FAILURE")
		elif ( [] == status2 ):
			print "ERROR: No status available for RWSServer"
			tdkTestObj.setResultStatus("FAILURE")
                else:
                        intervalPrev = 0
                        ret = recorderlib.getTimeListFromStatus(status)
                        print "RWS status server timelist = ",ret
                        for x in range(len(ret)-1):
                                intervalCurr = int( (ret[x+1] - ret[x])/1000 )
                                print "Retry interval for RWS status server: ",intervalCurr,"sec"
                                if intervalCurr <= intervalPrev:
                                        print "Retry interval for RWS status server not incrementing from ",intervalPrev,"sec to ",intervalCurr,"sec"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                        print "Retry interval for RWS status server incrementing from ",intervalPrev,"sec to ",intervalCurr,"sec"
                                intervalPrev = intervalCurr

                        intervalPrev = 0
                        ret = recorderlib.getTimeListFromStatus(status2)
                        print "RWS server timelist = ",ret
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
