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

# Description  : To initialize DSManager
#
# Parameters   : obj: Instance of devicesettings component library
#
# Return Value : "SUCCESS"/"FAILURE"
#
def dsManagerInitialize(obj):

        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');

        expectedresult = "SUCCESS"

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Result: [%s] Details: [%s]"%(result,details)

        #Set the result status of execution
        if expectedresult in result:
        	tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
		retValue = "FAILURE"

        return retValue

########## End of dsManagerInitialize Function ##########

# Description  : To de-Initialize DSManager
#
# Parameters   : obj: Instance of devicesettings component library
#
# Return Value : "SUCCESS"/"FAILURE"
#
def dsManagerDeInitialize(obj):

        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');

        expectedresult = "SUCCESS"

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Result: [%s] Details: [%s]"%(result,details)

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue

########## End of dsManagerDeInitialize Function ##########

# Description  : To check if display device is connected to STB
#
# Parameters   : obj: Instance of devicesettings component library
#
# Return Value : "TRUE"/"FALSE"
#
# Pre-condition: DSMgr should be initialized
# 
def dsIsDisplayConnected(obj):

        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('DS_IsDisplayConnectedStatus');

        expectedresult = "SUCCESS"

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Result: [%s] Details: [%s]"%(result,details)

        #Set the result status of execution
	if (expectedresult in result) and ("TRUE" in details):
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "TRUE"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FALSE"

        return retValue

########## End of dsIsDisplayConnected Function ##########
