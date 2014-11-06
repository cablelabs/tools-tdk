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

def change_powermode(obj,mode):

    #Setting the POWER state
    tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
    tdkTestObj.addParameter("method_name","SetPowerState");
    tdkTestObj.addParameter("owner_name","PWRMgr");               
    tdkTestObj.addParameter("newState",mode);        
    expectedresult="SUCCESS"
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details=tdkTestObj.getResultDetails();
    print "set power state: %s" %details;
    #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
    before_set_powerstate = details;
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        retValue = "SUCCESS";
        print "SUCCESS: Setting STB power state -RPC method invoked successfully";
        #Querying the STB power state
        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
        tdkTestObj.addParameter("method_name","GetPowerState");
        tdkTestObj.addParameter("owner_name","PWRMgr");
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        print "current power state: %s" %details;
        #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
        after_set_powerset=details;
        if expectedresult in actualresult:                      
            print "SUCCESS: Querying STB power state -RPC method invoked successfully";
            if before_set_powerstate == after_set_powerset :
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS";
                print "SUCCESS: Both the Power states are equal";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"
                print "FAILURE: Both power states are different";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            retValue = "FAILURE"
            print "FAILURE: Querying STB power state - IARM_Bus_Call failed. %s " %details;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        retValue = "FAILURE"
        print "FAILURE: Set STB power state - IARM_Bus_Call failed. %s " %details;
            
    return retValue;
