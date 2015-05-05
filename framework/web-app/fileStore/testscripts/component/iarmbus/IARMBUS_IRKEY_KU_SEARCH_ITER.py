'''
<?xml version="1.0" encoding="iso-8859-1" ?><xml>
	<id>1552</id>
	<!--Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty-->
	<version>49</version>
	<!--Do not edit version. This will be auto incremented while exporting. If you are adding a new script you can keep the vresion as 1-->
	<name>IARMBUS_IRKEY_KU_SEARCH_ITER</name>
	<!-- If you are adding a new script you can specify the script name.-->
	<primitive_test_id>604</primitive_test_id>
	<!--Do not change primitive_test_id if you are editing an existing script.-->
	<primitive_test_name>IARMBUSPERF_RegisterEventHandler</primitive_test_name>
	<!---->
	<primitive_test_version>1</primitive_test_version>
	<!---->
	<status>FREE</status>
	<!---->
	<synopsis>				Iterate on SEARCH key KEYUP events, time and average.</synopsis>
	<!---->
	<groups_id>None</groups_id>
	<!--If groups_id = None , it will be defaulted to 2 -->
	<execution_time>0</execution_time>
	<!--execution_time is the time out time for test execution-->
	<remarks>				</remarks>
	<!---->
	<skip>False</skip>
	<!---->
	<box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
		<box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
		<!--  -->
	</box_types>
	<rdk_versions>
		<rdk_version>RDK1.2</rdk_version>
		<!--  -->
		<rdk_version>RDK1.3</rdk_version>
		<!--  -->
		<rdk_version>RDK2.0</rdk_version>
		<!--  -->
	</rdk_versions>
</xml>
'''

import datalib;
import numpy as np;
import tdklib;
import time;

# Refer to header generic/iarmmgrs/generic/ir/include/twcIrKeyCodes.h
# KET_KEYDOWN 0x8000
# KET_KEYUP 0x8100
# KET_KEYREPEAT 0x8200
# KET_KEYUNDEFINEDKEY 0x8300
# Codes start at 250, go through 300
# Note: range(51) goes through 0 including 50
# KED_ONDEMAND/KED_BROWSE is 294
# KED_FP_POWER/KED_POWER is 297
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'IARMBUS_IRKEY_KU_SEARCH_ITER');
loadmodulestatus =obj.getLoadModuleResult();

print ("[LIB LOAD STATUS]  :  %s" %loadmodulestatus );

if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus('SUCCESS');
        timeval = 0.0;
        keytype = 33024;
        keycode = 299; 
        # Iterate on this action for 20 times
        itercount = 10;
        dataReadings = np.zeros(itercount);
        for i in range(itercount):
                print '******** Iteration %d **********\n' % i ;
                #calling IARMBUS API "IARM_Bus_Init"
                tdkTestObj = obj.createTestStep('IARMBUSPERF_Init');
                expectedresult="SUCCESS/FAILURE"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUSPERF_Init
                if ("SUCCESS" in actualresult or ("FAILURE" in actualresult and "INVALID_PARAM" in details)):
                        tdkTestObj.setResultStatus("SUCCESS");
                        print ("SUCCESS: Application successfully initialized with IARMBUSPERF library");
                        #calling IARMBUS API "IARM_Bus_Connect"
                        tdkTestObj = obj.createTestStep('IARMBUSPERF_Connect');
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUSPERF_Connect
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print ("SUCCESS: Application successfully connected with IARM-Bus Daemon");
                                #Run another application to receive broadcasted events
                                #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                                tdkTestObj = obj.createTestStep('IARMBUSPERF_RegisterEventHandler');
                                #registering event handler for IR Key events
                                tdkTestObj.addParameter("owner_name","IRMgr");
                                tdkTestObj.addParameter("event_id",0);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of IARMBUSPERF_RegisterEventHandler
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print ("SUCCESS: Event Handler registered for IR key events");
                                        #sleep for 3 sec to receive IR key event that is broadcasted from second app.
                                        time.sleep(3);
                                        tdkTestObj = obj.createTestStep('IARMBUSPERF_InvokeEventTransmitterApp');
                                        expectedresult="SUCCESS";
                                        #Specify the appname as "gen_single_event"
                                        #This app will run once and generate an IR event on the
                                        #bus with keyType and keyCode.
                                        tdkTestObj.addParameter("owner_name","IRMgr");
                                        tdkTestObj.addParameter("event_id",0);
                                        tdkTestObj.addParameter("evttxappname","gen_single_event");
                                        tdkTestObj.addParameter("keyType",keytype);
                                        tdkTestObj.addParameter("keyCode",keycode);
                                        tdkTestObj.executeTestCase(expectedresult);
                                        time.sleep(3);
                                        actualresult = tdkTestObj.getResult();
                                        #details=tdkTestObj.getResultDetails();
                                        #Check for SUCCESS/FAILURE return value of IARMBUSPERF_InvokeEventTransmitterApp
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print ("SUCCESS: Second application Invoked successfully");
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print ("FAILURE: Second application failed to execute");
                                        time.sleep(2);
                                        tdkTestObj = obj.createTestStep('IARMBUSPERF_GetLastReceivedEventDetails');
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        print details;
                                        details = details.split(":");
                                        length = len(details);
                                        timestr = details[length-1];
                                        try:
                                                timeval = float(timestr);
                                                print "Reading: %f" % timeval;
                                                dataReadings[i] = timeval
                                        except:
                                                 timeval=0.0;
                                                 pass
                                        print "Data: %d" % keycode;
                                        print "Units: s";
        
                                        #Check for SUCCESS/FAILURE return value of IARMBUSPERF_GetLastReceivedEventDetails
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print ("SUCCESS: GetLastReceivedEventDetails executed successfully");
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print ("FAILURE: GetLastReceivedEventDetails failed");
                                        tdkTestObj = obj.createTestStep('IARMBUSPERF_UnRegisterEventHandler');
                                        #deregistering IR event handler
                                        tdkTestObj.addParameter("owner_name","IRMgr");
                                        tdkTestObj.addParameter("event_id",0);
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        #Check for SUCCESS/FAILURE return value of IARMBUSPERF_UnRegisterEventHandler
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print ("SUCCESS: UnRegister Event Handler for IR key events");
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print ("FAILURE : IARMBUSPERF_UnRegisterEventHandler failed with %s " %details);
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print ("FAILURE : IARMBUSPERF_RegisterEventHandler failed with %s " %details);
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print ("FAILURE: IARMBUSPERF_Connect failed with %s" %details);
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print ("FAILURE: IARMBUSPERF_Init failed with %s " %details);
        
                #calling IARMBUS API "IARM_Bus_DisConnect"
                tdkTestObj = obj.createTestStep('IARMBUSPERF_DisConnect');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUSPERF_DisConnect
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print ("SUCCESS: Application successfully disconnected from IARMBus");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print ("FAILURE: IARMBUSPERF_Disconnect failed with %s " %details);
                #pause between each iteration
                #time.sleep(5);
        sizeOfData = itercount; 
        unitOfData = 2;
        dv = datalib.datavalidator(sizeOfData, unitOfData, sizeOfData, 5, dataReadings);
        dv.printAllData();
 
        print '\nIQR=%f\n' % dv.getInterQuartileRange();
        dv.flushOutOutliersByIQR();
        print '\nNormalized Mean = %f\n' % dv.getMean();
        print ("[TEST EXECUTION RESULT] : %s" %actualresult);
        #Unload the iarmbus module
        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        obj.setLoadModuleStatus("FAILURE");
