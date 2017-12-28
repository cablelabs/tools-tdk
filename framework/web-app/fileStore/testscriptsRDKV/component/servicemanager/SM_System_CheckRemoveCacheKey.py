##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
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
  <version>1</version>
  <name>SM_System_CheckRemoveCacheKey</name>
  <primitive_test_id/>
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To set the cache key and value and check if the cache contains the key using cacheContains(), then remove it using removeCacheKey() and verify again if the key is present in the cache using cacheContains()</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
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
    <test_case_id>CT_Service Manager_142</test_case_id>
    <test_objective>To set the cache key and value and check if the cache contains the key using cacheContains(), then remove it using removeCacheKey() and verify again if the key is present in the cache using cacheContains()</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Generic_CallMethod(const QString&amp; servicename,const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, 
Generic_CallMethod - system service , 
setCachedValue(key,value)
cacheContains(key)
removeCacheKey(key)
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "systemService" with ServiceManager component.
3.Set the api version as 12
4.Service_Manager_Agent will invoke the api setCachedValue with parameters key and value
5.Check in the cache if the set key is present using the api cacheContains()
6.Depending upon the status of cacheContains return SUCCESS/FAILURE status.
7. Remove this key-value pair using the api removeCacheKey()
8. Check again if the key is present in the cache using cacheContains()
9.Depending upon the status of cacheContains() return SUCCESS/FAILURE status.
10. Service_Manager_Agent will deregister the given service from ServiceManager component</automation_approch>
    <except_output>Checkpoint 1.System service should register successfully
Checkpoint 2. Setting of cached value should be success
Checkpoint 3. cacheContains should return true
Checkpoint 4. removeCacheKey should be success
Checkpoint 5. cacheContains should return false</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_System_CheckRemoveCacheKey</test_script>
    <skipped>No</skipped>
    <release_version>M54</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import servicemanager;

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_System_CheckRemoveCacheKey');

def cacheContains(serviceName,methodName,setKey):
    flag = 0;
    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
    methodName="cacheContains"
    tdkTestObj.addParameter("service_name", serviceName);
    tdkTestObj.addParameter("method_name", methodName);
    tdkTestObj.addParameter("params",setKey);
    tdkTestObj.executeTestCase(expectedresult);
    print "Calling method :",methodName
    actualresult = tdkTestObj.getResult();
    methodDetail = tdkTestObj.getResultDetails();

    if expectedresult in actualresult and "true" in methodDetail:
        print "CacheContains returned true"
        print methodName, "Details :",methodDetail
	flag = 1; 
    elif expectedresult in actualresult and "false" in methodDetail:
        print "CacheContains returned false"
        print methodName, "Details :",methodDetail
	flag = 2;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print methodName, "call is NOT successful";
        print methodName, "Details :",methodDetail
    return (tdkTestObj, flag);

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper():
    serviceName = "systemService";
    register = servicemanager.registerService(smObj,serviceName)
    if "SUCCESS" in register:
        tdkTestObj = smObj.createTestStep('SM_SetAPIVersion');
        expectedresult = "SUCCESS"
        apiVersion = 12;
        tdkTestObj.addParameter("apiVersion",apiVersion);
        tdkTestObj.addParameter("service_name",serviceName);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Set the API version %s succesfully" % apiVersion

	    #Calling the method setCachedValue() to set the key-value pair
            tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
            expectedresult="SUCCESS"
            methodName="setCachedValue"
            setKey = "partnerId"
            setValue = "0"
            inputlist = [setKey,setValue]
            tdkTestObj.addParameter("service_name", serviceName);
            tdkTestObj.addParameter("method_name", methodName);
            tdkTestObj.addParameter("params",inputlist);
            tdkTestObj.addParameter("inputCount", 2);
            tdkTestObj.executeTestCase(expectedresult);
            print "Calling method :",methodName
            actualresult = tdkTestObj.getResult();
            methodDetail = tdkTestObj.getResultDetails();

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "EXPECTED VALUE : setCachedValue should return SUCCESS"
                print "ACTUAL VALUE : setCachedValue returned SUCCESS"
                print methodName, "call is successful with parameter" , inputlist;
                print methodName, ": Details :" ,methodDetail
                print "TEST EXECUTION RESULT :SUCCESS"

		#Calling the function to call cacheContains() to check if the previously set key is present or not
	  	tdkTestObj, flag = cacheContains(serviceName,methodName,setKey);
		if flag == 1:
                    tdkTestObj.setResultStatus("SUCCESS");
        	    print "EXPECTED VALUE : CacheContains should return true"
		    print "ACTUAL VALUE : CacheContains returned true"
		    print "TEST EXECUTION RESULT :SUCCESS"

		    #Remove the previously set key
                    tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                    methodName="removeCacheKey"
                    tdkTestObj.addParameter("service_name", serviceName);
                    tdkTestObj.addParameter("method_name", methodName);
                    tdkTestObj.addParameter("params",setKey);
                    tdkTestObj.executeTestCase(expectedresult);
                    print "Calling method :",methodName
                    actualresult = tdkTestObj.getResult();
                    methodDetail = tdkTestObj.getResultDetails();
		    
		    if expectedresult in actualresult:
	                tdkTestObj.setResultStatus("SUCCESS");
	                print "EXPECTED VALUE : removeCacheKey should return SUCCESS"
        	        print "ACTUAL VALUE : removeCacheKey returned SUCCESS"
                	print methodName, "call is successful with parameter" , inputlist;
	                print methodName, ": Details :" ,methodDetail
        	        print "TEST EXECUTION RESULT :SUCCESS"

			#Calling the function to call cacheContains() to check if the previously removed key is properly removed or not
			tdkTestObj, flag = cacheContains(serviceName,methodName,setKey);
			if flag == 2:
			    tdkTestObj.setResultStatus("SUCCESS");
			    print "EXPECTED VALUE : cacheContains should return false"
			    print "ACTUAL VALUE : cacheContains returned false"
	                    print methodName, ": Details :" ,methodDetail
        	            print "TEST EXECUTION RESULT :SUCCESS"
			elif flag == 1:
			    tdkTestObj.setResultStatus("FAILURE");
			    print "EXPECTED VALUE : cacheContains should return false"
			    print "ACTUAL VALUE : cacheContains returned true"
	                    print methodName, ": Details :" ,methodDetail
        	            print "TEST EXECUTION RESULT :FAILURE"
			else:
			    tdkTestObj.setResultStatus("FAILURE");
		            print methodName, "call is NOT successful";
		            print "methodDetail:",methodDetail

		    else:
	                tdkTestObj.setResultStatus("FAILURE");
	                print "EXPECTED VALUE : removeCacheKey should return SUCCESS"
        	        print "ACTUAL VALUE : removeCacheKey returned FAILURE"
                	print methodName, "call is NOT successful with parameter" , inputlist;
	                print methodName, ": Details :" ,methodDetail
        	        print "TEST EXECUTION RESULT :FAILURE"

		elif flag == 2:
                    tdkTestObj.setResultStatus("FAILURE");
        	    print "EXPECTED VALUE : CacheContains should return true"
		    print "ACTUAL VALUE : CacheContains returned false"
		    print "TEST EXECUTION RESULT :FAILURE"
		else:
        	    tdkTestObj.setResultStatus("FAILURE");
		    print methodName, "call is NOT successful";
		    print "methodDetail:",methodDetail
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "EXPECTED VALUE : setCachedValue should return SUCCESS"
                print "ACTUAL VALUE : setCachedValue returned FAILURE"
                print methodName, "call is not successful with parameter" , inputlist;
                print methodName, ": Details :" ,methodDetail
                print "TEST EXECUTION RESULT :FAILURE"
        else:
            print "Unable to set the API version"
            tdkTestObj.setResultStatus("FAILURE");

        #Unregister System service
        print "Unregistering the System Service"
        unregister = servicemanager.unRegisterService(smObj,serviceName);

    else:
        print "Unable to register the System service"
        tdkTestObj.setResultStatus("FAILURE");

    #Unloading service manager module
    smObj.unloadModule("servicemanager");
else:
    print "Failed to load service manager module\n";
    #Set the module loading status
    smObj.setLoadModuleStatus("FAILURE");

