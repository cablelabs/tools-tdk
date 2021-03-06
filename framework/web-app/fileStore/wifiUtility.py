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
        print "TEST STEP : Execute callmethod for %s" %methodname
        print "EXPECTED RESULT : Should successfully execute callmethod"
        print "ACTUAL RESULT : %s " %details
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
        print "TEST STEP : Execute callmethod for %s" %methodname
        print "EXPECTED RESULT : Should successfully execute callmethod"
        print "ACTUAL RESULT 1: %s " %details
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";

    return (tdkTestObj, actualresult, details);


