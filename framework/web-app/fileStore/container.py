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

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import tdklib;

def CheckProcessTree(obj, expectedState):
	status = False;
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        expectedResult="SUCCESS";
	
	cmd = "pstree | grep -o -e dbusDaemonInit -e rmfStreamerInit -e systemd | tr \'\n\' \' \'";
	
	#configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
	print "Exceution result: ", actualResult;
	
	if expectedResult in actualResult:
		details = tdkTestObj.getResultDetails();
		print "Output: ", details;
		if "dbusDaemonInit" in details and "rmfStreamerInit" in details and "systemd" in details:
			if expectedState:
                                tdkTestObj.setResultStatus("SUCCESS");
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
			print "Containerization is enabled";
			status = True;
		else:
			if expectedState:
                                tdkTestObj.setResultStatus("FAILURE");
                        else:
                                tdkTestObj.setResultStatus("SUCCESS");
			print "Containerization is not enabled";
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Command execution failed";
	return status;


def CheckContainerState(obj, containerName, expectedState):
	status = False;
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        expectedResult="SUCCESS";
	
	cmd = "lxc-info -n " + containerName + " | grep State";
	
	#configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
	print "Exceution result: ", actualResult;
	
	if expectedResult in actualResult:
		details = tdkTestObj.getResultDetails();
		print "Output: ", details;
		if "RUNNING" in details:
			if expectedState:
				tdkTestObj.setResultStatus("SUCCESS");
			else:
				tdkTestObj.setResultStatus("FAILURE");
			print "%s Container is running" %containerName;
			status = True;
		else:
			if expectedState:
				tdkTestObj.setResultStatus("FAILURE");
			else:
				tdkTestObj.setResultStatus("SUCCESS");
			print "%s Container is not running" %containerName;
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Command execution failed";
	return status;


def FindPatternFromFile(obj, fileName, field, pattern):
	status = False;
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        expectedResult="SUCCESS";
	
	cmd = "cat " + fileName + " | grep " + field;
	
	#configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
	print "Exceution result: ", actualResult;
	
	if expectedResult in actualResult:
		details = tdkTestObj.getResultDetails();
		print "Output: ", details;
		if pattern in details:
			tdkTestObj.setResultStatus("SUCCESS");
			status = True;
		else:
			tdkTestObj.setResultStatus("FAILURE");
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Command execution failed";
	return status;

def GetFilePermission(obj, fileName):
        status = False;
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        expectedResult="SUCCESS";

        cmd = "stat -c \"%a %n\" "  + fileName + "| cut -d \" \" -f 1";
	print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
		permissionValue = details.strip('\\n');
                if  permissionValue == "770":
                        tdkTestObj.setResultStatus("SUCCESS");
			print "Permission satisfied for ", fileName;
                        status = True;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
			print "Permission not satisfied for ", fileName;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;

def GetOwnership(obj, fileName, owner, field):
        status = False;
	result = True;
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        expectedResult="SUCCESS";

        cmd = "ls -al "  + fileName + " |  tr -s \" \" | cut -d \" \" -f " +field + " | tr \'\\n\' \',\'";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
		output = details.split(',');
		for item in output:
			if owner not in item:
				print "Expected user owner for files in %s is %s, but recieved %s" %(fileName, owner, item); 
				result = False;	
		
                if result:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "User ownership as expected for ", fileName;
                        status = True;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "User ownership not as expected for ", fileName;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;

def StopContainer(obj, containerName):
        status = False;
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        expectedResult="SUCCESS";

        cmd = "lxc-stop -n " + containerName + "&";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
        	tdkTestObj.setResultStatus("SUCCESS");
                print "Container %s stopped" %containerName;
                status = True;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;

def StartContainer(obj):
        status = False;
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        expectedResult="SUCCESS";

        cmd = "/usr/bin/start_containers.sh &"
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Containers started";
                status = True;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;



def GetIdFromFile(obj, fileName, pattern):
        status = False;
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        expectedResult="SUCCESS";

        cmd = "cat " + fileName + " | grep " + pattern + " | cut -d \" \" -f 5";
	print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
                if pattern in details:
                        tdkTestObj.setResultStatus("SUCCESS");
                        status = True;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;


def AccessContainerShell(obj, containerName):
        status = False;
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        expectedResult="SUCCESS";

        #cmd = "lxc-attach -n " + containerName;
        cmd = "lxc-attach -n dbus";
	print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;

		print "*****************";
		tdkTestObj.addParameter("command", "ps | grep dbusDaemonInit");
	        tdkTestObj.executeTestCase(expectedResult);

        	actualResult = tdkTestObj.getResult();
	        print "Exceution result: ", actualResult;
		details = tdkTestObj.getResultDetails();
                print "Output: ", details;
		print "*****************";

		expectedOutput = "root@" + containerName + ":/#";
                if expectedOutput in details:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Accessed %s Container shell" %containerName;
                        status = True;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "%s Container shell not accessible" %containerName;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;

