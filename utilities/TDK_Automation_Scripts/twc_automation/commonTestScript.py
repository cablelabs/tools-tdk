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
import sys
sys.path.insert(0, "../python-lib/")
from time import gmtime, strftime;
import tdklib;
import time;
import datalib;
import numpy as np;


def configureTest():
        obj = tdklib.TDKScriptingLibrary(str(sys.argv[7]),str(sys.argv[13]))#argument 7 will be the shared object name to be tested int he STB.
        ip = sys.argv[1];
        port = int(sys.argv[2]);
        path = sys.argv[3]+"/";
        url = sys.argv[4];
        execName = sys.argv[5];
        total = len(sys.argv)
        cmdargs = str(sys.argv)
        logTransferPort = 69
        statusPort = 8088
        testcaseID = 153
        deviceId = 2279
        print ("\nThe total numbers of commandline args passed: %d " % total)
        print ("\nArgs list: %s " % cmdargs)
        print ("\nScript Name: %s" % str(sys.argv[0]))
        print ("\nFirst argument is IP Address: %s" % str(sys.argv[1]))
        print ("\nSecond argument is Port Number: %s" % str(sys.argv[2]))
        print ("\nThird argument is Path to save the logs: %s" % str(sys.argv[3]))
        print ("\nFourth argument is URL of Test Manager: %s" % str(sys.argv[4]))
        print ("\nFifth argument is Execution Name: %s" % str(sys.argv[5]))
        print "\nSTB Details : IP: %s " %ip;
        print "\nSTB Details : Port: %d" %port;
        print "\nPath: %s" %path;
        print "\nURL of Test Manager is: %s" %url;
        print "\nExecution Name: %s" %execName;
        print ("\nTest Suite Name Name: %s" % str(sys.argv[14]))

        try:
		lastExecResId = obj.fetchLastExecutionResultId();
		lastExecMethResId = obj.fetchLastExecuteMethodResultId();
		execId = int(sys.argv[11])
		execResId = int(lastExecResId) + 1;
		execMethResId = int(lastExecMethResId) + 1;
		execDevId = int(sys.argv[12])
		componentName=str(sys.argv[9])
		testType=str(sys.argv[10])
		
		print "Current EXEC_DEVID: %d" %execDevId
		print "Current EXEC_ID: %d" %execId
		print "Current EXEC_RESID: %d" %execResId
		print "Current EXEC_METHRESID: %d" %execMethResId
		infoDict={}
		infoDict['componentName']=componentName
		infoDict['testType']=testType
		infoDict['testSuiteName']=str(sys.argv[14])
		obj.enableLogging(str(sys.argv[6]),str(sys.argv[3]),infoDict)#sys.argv[6] - script Name, sys.argv[3] - log path.
		obj.configureTestCase (url, path, execId, execDevId, execResId, ip, port, logTransferPort, statusPort, testcaseID, deviceId, 'false', 'false', 'false', execName);
		print "--**--log_path--**--"+obj.logpath+"/logs/"+str(execId)+"/"+str(execDevId)+"/"+str(execResId)+"/"+"--**--log_path--**--do not chnage this format"
	except Exception,e:
		print "Error from method configureTest() in commonTestScript.py"
		print e.message
	
        return obj




try:
	sys.path.insert(0, str(sys.argv[8]))#str(sys.argv[8] is the script location path , specified in the TdkConfig.xml

	tdkobj=configureTest()

	print "going to import "+ str(sys.argv[6])
	command_module = __import__(str(sys.argv[6]), fromlist=[]) # str(sys.argv[6]) is the script name without the .py extension

	command_module.executeTests(tdkobj)
	if tdkobj.insertScriptAndFnExeDetailsInDb() == False :
		print "ERROR: Database insertion failed."
	print "From "+str(sys.argv[0]) + " : command_module.executeTests() completed"
except Exception,e:
	print "Error: Check the methods -configureTest(), __import__,executeTests,tdkobj.insertExecutionDetails   in commonTestScript.py"
	print e.message

