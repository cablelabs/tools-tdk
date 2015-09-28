'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TWC_IRKEY_NUMERICKEYS_ITER</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>4</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_Init</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test case Id -
IRKEY_NUMERICKEYS_ITER_TC_01
IRKEY_NUMERICKEYS_ITER_TC_02
IRKEY_NUMERICKEYS_ITER_TC_03
IRKEY_NUMERICKEYS_ITER_TC_04
IRKEY_NUMERICKEYS_ITER_TC_05
IRKEY_NUMERICKEYS_ITER_TC_06
IRKEY_NUMERICKEYS_ITER_TC_07
IRKEY_NUMERICKEYS_ITER_TC_08
IRKEY_NUMERICKEYS_ITER_TC_09
IRKEY_NUMERICKEYS_ITER_TC_10
IRKEY_NUMERICKEYS_ITER_TC_11
IRKEY_NUMERICKEYS_ITER_TC_12
IRKEY_NUMERICKEYS_ITER_TC_13
IRKEY_NUMERICKEYS_ITER_TC_14
IRKEY_NUMERICKEYS_ITER_TC_15
IRKEY_NUMERICKEYS_ITER_TC_16
IRKEY_NUMERICKEYS_ITER_TC_17
IRKEY_NUMERICKEYS_ITER_TC_18
IRKEY_NUMERICKEYS_ITER_TC_19
IRKEY_NUMERICKEYS_ITER_TC_20
IRKEY_NUMERICKEYS_ITER_TC_21
IRKEY_NUMERICKEYS_ITER_TC_22
IRKEY_NUMERICKEYS_ITER_TC_23
IRKEY_NUMERICKEYS_ITER_TC_24
IRKEY_NUMERICKEYS_ITER_TC_25
IRKEY_NUMERICKEYS_ITER_TC_26
IRKEY_NUMERICKEYS_ITER_TC_27
IRKEY_NUMERICKEYS_ITER_TC_28
IRKEY_NUMERICKEYS_ITER_TC_29
IRKEY_NUMERICKEYS_ITER_TC_30</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
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
#This python script is autogenerated by parsing the original scripts imported from the Database
#This script is supposed to be called from the genericscript.py 
#TODO:replace this caling script name with correct one
from time import sleep;
from tdklib import TDKScriptingLibrary;
import datalib;
import numpy as np;

#Test component to be tested
obj = TDKScriptingLibrary("iarmbus","1.3");

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TWC_IRKEY_NUMERICKEYS_ITER');
loadmodulestatus =obj.getLoadModuleResult();
print ("[LIB LOAD STATUS]  :  %s" %loadmodulestatus );
if "SUCCESS" in loadmodulestatus.upper():
	obj.setLoadModuleStatus('SUCCESS');
	timeval = 0.0;
	with open(obj.realpath + '/fileStore/testscripts/component/iarmbus/IRkey_Numerickeys_Iter.txt', 'r') as f:
		#print obj.realpath;
		data = f.readlines();
		#expectedresult="SUCCESS/FAILURE"
		print data
		for line in data:
			print line
			print "got line"
			Eline = line.split("\n");
			print Eline[0]
			Estring=Eline[0].split(":")
	       		print Estring, "=",Estring[0]," + ",Estring[1]," + ",Estring[2]
			keytype = int(Estring[1]);
	        	keycode = int(Estring[2]); 
	        	# Iterate on this action for 6 times
	        	itercount = 6;
        		dataReadings = np.zeros(itercount);
			for i in range(itercount):
				print '******** Iteration %d **********\n' % i ;
            			#calling IARMBUS API "IARM_Bus_Init"
		            	tdkTestObj = obj.createTestStep('IARMBUS_Init',0);
				expectedresult="SUCCESS/FAILURE"
				tdkTestObj.executeTestCase(expectedresult);
				actualresult = tdkTestObj.getResult();
        		        details=tdkTestObj.getResultDetails();
		                #Check for SUCCESS/FAILURE return value of IARMBUSPERF_Init
				if ("SUCCESS" in actualresult or ("FAILURE" in actualresult and "INVALID_PARAM" in details)):
					tdkTestObj.setResultStatus("SUCCESS");
        			        print ("SUCCESS: Application successfully initialized with IARMBUS library");
					#calling IARMBUS API "IARM_Bus_Connect"
			                tdkTestObj = obj.createTestStep('IARMBUS_Connect',0);
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
                        			tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler',0);
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
							#time.sleep(3);
							tdkTestObj = obj.createTestStep('IARMBUS_InvokeEventTransmitterApp',0);
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
							#time.sleep(3);
							actualresult = tdkTestObj.getResult();
							#details=tdkTestObj.getResultDetails();
							#Check for SUCCESS/FAILURE return value of IARMBUSPERF_InvokeEventTransmitterApp
							if expectedresult in actualresult:
								tdkTestObj.setResultStatus("SUCCESS");
								print ("SUCCESS: Second application Invoked successfully");
							else:
								tdkTestObj.setResultStatus("FAILURE");
								print ("FAILURE: Second application failed to execute");
							#sleep for 2 sec to receive IR key event that is broadcasted from second app
							sleep(2);
							tdkTestObj = obj.createTestStep('IARMBUS_GetLastReceivedEventPerformanceDetails',4);
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
							print "Data: %d" % int(keycode);
							print "Units: s";
							#Check for SUCCESS/FAILURE return value of IARMBUSPERF_GetLastReceivedEventDetails
							if expectedresult in actualresult:
								tdkTestObj.setResultStatus("SUCCESS");
								print ("SUCCESS: GetLastReceivedEventDetails executed successfully");
							else:
								tdkTestObj.setResultStatus("FAILURE");
								print ("FAILURE: GetLastReceivedEventDetails failed");
							perfData=tdkTestObj.logPerformanceData();
							tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler',0);
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
								print ("FAILURE : IARMBUS_UnRegisterEventHandler failed with %s " %details);
						else:
							tdkTestObj.setResultStatus("FAILURE");
							print ("FAILURE : IARMBUS_RegisterEventHandler failed with %s " %details);
					else:
						tdkTestObj.setResultStatus("FAILURE");
						print ("FAILURE: IARMBUS_Connect failed with %s" %details);
				else:
					tdkTestObj.setResultStatus("FAILURE");
					print ("FAILURE: IARMBUS_Init failed with %s " %details);
        
				#calling IARMBUS API "IARM_Bus_DisConnect"
				tdkTestObj = obj.createTestStep('IARMBUS_DisConnect',0);
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
					print ("FAILURE: IARMBUS_Disconnect failed with %s " %details);
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
			tdkTestObj = obj.createTestStep('IARMBUS_IRKeyEventTime',5,"Test for checking: "+'keyname: '+Estring[0]+'keytype: '+str(keytype)+'keycode: '+str(keycode));
			perfData=tdkTestObj.logPerformanceData('IRKeyEventPropagation_AveragedTime','ms',str(dv.getMean()),'keytype:'+str(keytype)+' keycode:'+str(keycode) );
			sleep(1);
	obj.unloadModule("iarmbus");
else:
	print"Load module failed";
	obj.setLoadModuleStatus("FAILURE");
