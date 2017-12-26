#!/usr/bin/python
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

# A utility function to invoke WiFi hal apis based on the method name received
#
# Syntax       : ExecuteWIFIHalCallMethod(obj, primitive, radioIndex, param, methodname)
#
# Parameters   : obj, primitive, radioIndex, param, methodname 
#
# Return Value : Execution status of the hal api

def ExecuteWIFIHalCallMethod(obj, primitive, radioIndex, param, methodname):

    tdkTestObj = obj.createTestStep(primitive);
    tdkTestObj.addParameter("radioIndex", radioIndex);
    #'param' is valid for only set operations. It isdummy attribute for get functions
    tdkTestObj.addParameter("param", param);
    tdkTestObj.addParameter("methodName", methodname);
    expectedresult="SUCCESS";

    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if expectedresult in actualresult :
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP : Execute callmethod for %s" %methodname
        print "EXPECTED RESULT : Should successfully execute callmethod"
        print "ACTUAL RESULT : %s " %details
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP : Execute callmethod for %s" %methodname
        print "EXPECTED RESULT : Should successfully execute callmethod"
        print "ACTUAL RESULT 1: %s " %details
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";

    return (tdkTestObj, actualresult, details);


##########################################################################

# A utility function to invoke WiFi hal api wifi_applyRadioSettings based on the radioIndex received
#
# Syntax       : ExecuteWIFIApplySettings(obj, radioIndex)
#
# Parameters   : obj, radioIndex
#
# Return Value : Execution status of the hal api

def ExecuteWIFIApplySettings(obj,radioIndex):
    #Script to load the configuration file of the component
    tdkTestObj = obj.createTestStep("WIFIHAL_ApplySettings");
    #Giving the method name to invoke the api to set the radio settings
    #Radio index is 0 for 2.4GHz and 1 for 5GHz
    tdkTestObj.addParameter("radioIndex",radioIndex);
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if expectedresult in actualresult :
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP: Executing wifi_applyRadioSettings to set the previous changes"
        print "EXPECTED RESULT: Execution returns SUCCESS"
        print "ACTUAL RESULT: %s"%details;
        print "TEST EXECUTION RESULT :SUCCESS"
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP: Executing wifi_applyRadioSettings to set the previous changes"
        print "EXPECTED RESULT: Execution returns SUCCESS"
        print "ACTUAL RESULT: %s"%details;
        print "TEST EXECUTION RESULT :FAILURE"

    return (tdkTestObj, actualresult, details);


