'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_RWSServerOutage_CheckConnectionRetrial_62</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check that after RWS Get server outage recorder attempts no more than 1 concurrent connection with randomized  exponentially-longer retry intervals each time, to avoid overwhelming the server after a systemwide outage.</synopsis>
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
  <script_tags />
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
recObj.configureTestCase(ip,port,'Recorder_RMF_RWSServerOutage_CheckConnectionRetrial_62');
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
	recorderlib.callServerHandlerWithType('clearDisabledStatus','RWSServer',ip)
        recorderlib.callServerHandler('clearStatus',ip)

        #Disable RWSServer
        recorderlib.callServerHandlerWithType('disableServer','RWSServer',ip)
        status = recorderlib.callServerHandlerWithType('isEnabledServer','RWSServer',ip)
        print "RWS server status: ",status
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',"{\"noUpdate\":{}}",ip);
        if "FALSE" in status.upper():
                print "Waiting for 550s to get connection retrial attempts from recorder"
                sleep(550)

                #Checkpoint-1: Get the time between each re-trials
                print "Checking status of disabled servers"
                rwsstatus = recorderlib.callServerHandlerWithType('retrieveDisabledStatus','RWSServer',ip)
                print "RWSServer Status: ",rwsstatus
                #Check if status is not empty
                if ( "[]" in rwsstatus ):
                        print "ERROR: No connection retry from recorder"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                        intervalPrev = 0
                        ret = recorderlib.getTimeListFromStatus(rwsstatus)
                        print "RWSServer timelist = ",ret
                        if (0 == len(ret)):
                            tdkTestObj.setResultStatus("FAILURE")
                            print "ERROR: No connection retry from recorder"
                        elif (1 == len(ret)):
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

                #Checkpoint-2: Check no status from RWSServer
                response = recorderlib.callServerHandler('retrieveStatus',ip);
                print "response = ",response
                if 'RWSServer' in response:
                        print "Recorder communicated with RWSServer in disabled state"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                        print "Recorder did not communicate with RWSServer in disabled state as expected"

                #post-req: Enable RWSServer
                recorderlib.callServerHandlerWithType('enableServer','RWSServer',ip)
                status = recorderlib.callServerHandlerWithType('isEnabledServer','RWSServer',ip)
                print "RWS server status: ",status
                if "FALSE" in status.upper():
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to enable RWS Server"
                else:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Enabled RWS Server"
        else:
                print "Failed to disable RWS Server. Exiting.."
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        recObj.unloadModule("Recorder");
