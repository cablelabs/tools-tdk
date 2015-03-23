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
	if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
        else:
                tdkTestObj.setResultStatus("FAILURE");

        if "FALSE" in details:
                retValue = "FALSE"
        else:
                retValue = "TRUE"

        return retValue

########## End of dsIsDisplayConnected Function ##########
## Get Resolution ##
def dsGetResolution(obj,expectedresult,kwargs={}):

        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('DS_SetResolution');

        #Add parameters to test object
        portName=str(kwargs["portName"])
        tdkTestObj.addParameter("port_name",portName);
        tdkTestObj.addParameter("get_only",1);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        print "[Get Resolution RESULT] : %s" %actualresult;
        resolution = tdkTestObj.getResultDetails();
        print "[Get Resolution VALUE] : %s" %resolution;

        #Set the result status of execution
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
        else:
                tdkTestObj.setResultStatus("FAILURE");

        return resolution

## End of Get Resolution ##

## Set Resolution ##
def dsSetResolution(obj,expectedresult,kwargs={}):

        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('DS_SetResolution');

        #Add parameters to test object
        portName=str(kwargs["portName"])
        resolution=str(kwargs["resolution"])
        print "Setting resolution value to %s" %resolution;
        tdkTestObj.addParameter("resolution",resolution);
        tdkTestObj.addParameter("port_name",portName);
        tdkTestObj.addParameter("get_only",0);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        print "[Set Resolution RESULT] : %s" %actualresult;
        getResolution = tdkTestObj.getResultDetails();
        print "[Get Resolution VALUE] : %s" %getResolution;

        #Set the result status of execution
        if expectedresult in actualresult:
                #Comparing the resolution before and after setting
                if resolution in getResolution:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Get resolution value same as Set resolution value";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Get resolution value not same as Set resolution value";
        else:
                tdkTestObj.setResultStatus("FAILURE");

        return getResolution

## End of Set Resolution ##

## Get CPU Temperture ##
def dsGetCPUTemp(obj,expectedresult):

        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('DS_GetCPUTemperature');

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Result : [%s] "%actualresult,

        #Set the result status of execution
        if expectedresult in actualresult:
		print "Details : [+%sC]" %details;
		if ((float(details) <= float(0)) or (float(details) > float(125))):
			print "Temperature out of range";
			retValue = "FAILURE"
		else:
			retValue = "SUCCESS"
        else:
		print "Details : [%s]" %details;
		retValue = "FAILURE"

        tdkTestObj.setResultStatus(retValue);
        return (retValue,details)

## End of Get CPU Temperture ##
