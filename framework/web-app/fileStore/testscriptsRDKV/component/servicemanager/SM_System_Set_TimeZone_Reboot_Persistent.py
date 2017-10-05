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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>2</version>
  <name>SM_System_Set_TimeZone_Reboot_Persistent</name>
  <primitive_test_id/>
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <primitive_test_version>7</primitive_test_version>
  <status>FREE</status>
  <synopsis>To set the time zone and check its persistence after reboot</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_88</test_case_id>
    <test_objective>To check whether available time zones are set and get successfully and whether it persists even after rebooting the device</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xg1V3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Generic_CallMethod(const QString&amp; servicename,const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, 
Generic_CallMethod - system service , 
getTimeZoneDST
setTimeZoneDST
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>
1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "systemService" with ServiceManager component.
3.Set the api version as 11
4.Service_Manager_Agent will invoke the api setTimeZoneDST 
5.Reboot the device
6.and getTimeZoneDST
7.Set one of the available timezone and check
8.TM will check the values and return SUCCESS/FAILURE status.
9. Service_Manager_Agent will deregister the given service from ServiceManager component
</automation_approch>
    <except_output>Checkpoint 1.System service should register successfully
Checkpoint 2.Check the timezones are set properly.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_System_Set_TimeZone_Reboot_Persistent</test_script>
    <skipped>No</skipped>
    <release_version>M50</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import servicemanager;
import iarmbus;

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");


#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_System_Set_TimeZone_Reboot_Persistent');
iarmObj.configureTestCase(ip,port,'SM_System_Set_TimeZone_Reboot_Persistent');

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus.upper());

iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[iarmbus LIB LOAD STATUS]  :  %s" %iarmLoadStatus;
iarmObj.setLoadModuleStatus(iarmLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper() and "SUCCESS" in iarmLoadStatus.upper():
    #Calling IARM Bus Init
    init=iarmbus.IARMBUS_Init(iarmObj,'SUCCESS')
    if "SUCCESS" in init:
        connect=iarmbus.IARMBUS_Connect(iarmObj,'SUCCESS')
        if "SUCCESS" in connect:
	    serviceName = "systemService";
	    register = servicemanager.registerService(smObj,serviceName)
	    if "SUCCESS" in register:
        	tdkTestObj = smObj.createTestStep('SM_SetAPIVersion');
	        expectedresult = "SUCCESS"
        	apiVersion = 11;
	        tdkTestObj.addParameter("apiVersion",apiVersion);
        	tdkTestObj.addParameter("service_name",serviceName);
	        tdkTestObj.executeTestCase(expectedresult);
        	actualresult = tdkTestObj.getResult();
	        if expectedresult in actualresult:
        	    tdkTestObj.setResultStatus("SUCCESS");
	            print "Set the API version %s succesfully" % apiVersion
        	    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
	            expectedresult="SUCCESS"
        	    methodName="setTimeZoneDST"
		    #Giving the input in the format "std offset dst [offset],start[/time],end[/time]" as per GNU specification
        	    settimeZone="EST+5EDT,M9.3.3/11,M9.3.3/56"
	            tdkTestObj.addParameter("service_name", serviceName);
        	    tdkTestObj.addParameter("method_name", methodName);
	            tdkTestObj.addParameter("params",settimeZone);
        	    tdkTestObj.addParameter("inputCount", 1);
	            tdkTestObj.executeTestCase(expectedresult);
        	    print "Calling method :",methodName
	            actualresult = tdkTestObj.getResult();

        	    if expectedresult in actualresult:
                	tdkTestObj.setResultStatus("SUCCESS");
	                print methodName, "call is successful with parameter" , settimeZone;
        	        methodDetail = tdkTestObj.getResultDetails();
                	print methodName, ": Details :" ,methodDetail
	
                        #Calling IARM_Bus_DisConnect API
                        disconnect=iarmbus.IARMBUS_DisConnect(iarmObj,'SUCCESS')
                        term=iarmbus.IARMBUS_Term(iarmObj,'SUCCESS')

        	        #Reboot the STB
                	smObj.initiateReboot();
                        #Reset the connection after reboot
                        iarmObj.resetConnectionAfterReboot();

                        #Calling IARM Bus Init
                        init=iarmbus.IARMBUS_Init(iarmObj,'SUCCESS')
                        if "SUCCESS" in init:
                            connect=iarmbus.IARMBUS_Connect(iarmObj,'SUCCESS')
                            if "SUCCESS" in connect:
                                print "Registering the System Service after reboot"
        	        	serviceName = "systemService";
	                 	register = servicemanager.registerService(smObj,serviceName)
	 	                if "SUCCESS" in register:
                                    tdkTestObj = smObj.createTestStep('SM_SetAPIVersion');
                                    expectedresult = "SUCCESS"
                                    apiVersion =11;
                                    tdkTestObj.addParameter("apiVersion",apiVersion);
                                    tdkTestObj.addParameter("service_name",serviceName);
                                    tdkTestObj.executeTestCase(expectedresult);
                                    actualresult = tdkTestObj.getResult();
                                    if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Set the API version %s succesfully" % apiVersion
                      		        tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod'); 
		                        methodName="getTimeZoneDST"
        		                tdkTestObj.addParameter("service_name", serviceName);
                		        tdkTestObj.addParameter("method_name", methodName);
	                	        tdkTestObj.executeTestCase(expectedresult);
	        	                print "Calling method after reboot:",methodName
        	        	        actualresult = tdkTestObj.getResult();

	        	                if expectedresult in actualresult:
        	        	            tdkTestObj.setResultStatus("SUCCESS");
                	        	    print methodName, "call is successful";
	                        	    methodDetail = tdkTestObj.getResultDetails();
		                            print methodName, ": Get Details :" ,methodDetail
        		                    gettimeZone = methodDetail.replace("\\","");
                		            if gettimeZone == settimeZone:
                        		        tdkTestObj.setResultStatus("SUCCESS");
		                                print "Successfully gets the time zone as " ,settimeZone , "after reboot"
        		                    else:
                		                print "Unable to get time zone as " , settimeZone, "after reboot"
                        		        tdkTestObj.setResultStatus("FAILURE");
		                        else:
        		                    print methodName, "call is NOT successful";
                		            tdkTestObj.setResultStatus("FAILURE");
				    else:
					print "Unable to set the API Version " , apiVersion
					tdkTestObj.setResultStatus("FAILURE");
	        	        else:
        	        	    print "Unable to register the System service"
		                    tdkTestObj.setResultStatus("FAILURE");
            	    else:
 	                print methodName, "call is NOT successful with parameter" , settimeZone;
          	        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print "Unable to set the API version"
                    tdkTestObj.setResultStatus("FAILURE");

                #Unregister System service
                print "Unregistering the System Service"
                unregister = servicemanager.unRegisterService(smObj,serviceName);

                #Calling IARM_Bus_DisConnect API
                disconnect=iarmbus.IARMBUS_DisConnect(iarmObj,'SUCCESS')
                term=iarmbus.IARMBUS_Term(iarmObj,'SUCCESS')

            else:
                print "Unable to register the System service"
        	tdkTestObj.setResultStatus("FAILURE");

	    #Unloading service manager module
	    smObj.unloadModule("servicemanager");
            #Unloading iarmbus module^M
            iarmObj.unloadModule("iarmbus");

else:
    print "Failed to load service manager module\n";
    #Set the module loading status
    smObj.setLoadModuleStatus("FAILURE");
    iarmObj.setLoadModuleStatus("FAILURE");




