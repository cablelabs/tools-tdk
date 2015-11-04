#!/usr/bin/python

#============================================================================
#COMCAST CONFIDENTIAL AND PROPRIETARY
#============================================================================
#This file and its contents are the intellectual property of Comcast.  It may
#not be used, copied, distributed or otherwise  disclosed in whole or in part
#without the express written permission of Comcast.
#============================================================================
#Copyright (c) 2013 Comcast. All rights reserved.
#============================================================================

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import tdklib;

def registerService(obj,service_name):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('SM_RegisterService')

    expectedresult = "SUCCESS"

    #Execute the test case in STB
    tdkTestObj.addParameter("service_name",service_name)
    tdkTestObj.executeTestCase(expectedresult)

    #Get the result of execution
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print "Details: ", details

    #Set the result status of execution
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        retValue = "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        retValue = "FAILURE"

    return retValue


def unRegisterService(obj,service_name):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('SM_UnRegisterService')

    expectedresult = "SUCCESS"

    #Execute the test case in STB
    tdkTestObj.addParameter("service_name",service_name)
    tdkTestObj.executeTestCase(expectedresult)

    #Get the result of execution
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print "Details: ", details

    #Set the result status of execution
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        retValue = "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        retValue = "FAILURE"

    return retValue


def doesServiceExists(obj,service_name):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('SM_DoesServiceExist')

    expectedresult = "SUCCESS"

    #Execute the test case in STB
    tdkTestObj.addParameter("service_name",service_name)
    tdkTestObj.executeTestCase(expectedresult)

    #Get the result of execution
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print "Details: ", details

    #Set the result status of execution
    if expectedresult in actualresult:
        if "PRESENT" in details:
		tdkTestObj.setResultStatus("SUCCESS")
		retValue = "SUCCESS"
	else:
		tdkTestObj.setResultStatus("FAILURE")
        	retValue = "FAILURE"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        retValue = "FAILURE"

    return retValue
