# !/usr/bin/python
#Use tdklib library,which provides a wrapper for tdk testcase script
import sys;
import tdklib; 
from time import gmtime, strftime;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("opensourcetestsuite","2.0")

#This will be replaced with correspoing Box Ip and port while executing script
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

lastExecId = obj.fetchLastExecutionId();
lastExecResId = obj.fetchLastExecutionResultId();
lastExecMethResId = obj.fetchLastExecuteMethodResultId();

execId = lastExecId + 1;
execResId = lastExecResId + 1;
execMethResId = lastExecMethResId + 1;
lastExecDevId = obj.fetchLastExecutionDeviceId();
execDevId = lastExecDevId + 1;
print "Current EXEC_DEVID: %d" %execDevId

print "Current EXEC_ID: %d" %execId
print "Current EXEC_RESID: %d" %execResId
print "Current EXEC_METHRESID: %d" %execMethResId


#obj.configureTestCase(ip,port,'Gst-plugin-base_execution');
#obj.configureTestCase(url, path, exec_id, 2222, ip, port,exec_name);
#OBJ.configureTestCase(url, path, execId, execDeviceId, execResId, deviceIp, devicePort, logTransferPort, statusPort, testcaseID, deviceId,		     performanceBenchMarkingEnabled, performanceSystemDiagnosisEnabled, executionName)

obj.configureTestCase (url, path, execId, execDevId, execResId, ip, port, logTransferPort, statusPort, testcaseID, deviceId, 'false', 'false', 'false',execName);

#obj.configureTestCase ('http://192.168.161.32:8080/rdk-test-tool','/opt/apache-tomcat-6.0.41/webapps/rdk-test-tool/',25, 3333, 29, ip, port, 69, 8088, 55, 66, 'false', 'false', 'false', 'CT_IARMBUS_3');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
if "Success" in result:
  data1= "Opensource test module successfully loaded\n";
  print "Opensource test module successfully loaded\n";
  
  #Prmitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('OpenSource_Comp_Test');

  # Configuring the test object for gst-plugin-base test suites execution
  tdkTestObj.addParameter("Opensource_component_type","gst-plugin-base");

  #Execute the test case in STB
  expectedresult="Test Suite Executed"
  executionTime = tdkTestObj.executeTestCase(expectedresult);

  #Get the result of execution
  actualresult = tdkTestObj.getResult();
  data2 = actualresult;
  print "\nGstreamer Base Plugin Test Results : %s" %actualresult; 
 
  #To Validate the Execution of Test Suites 
  details = tdkTestObj.getResultDetails();
  if "TotalSuite" in details:
    data3 = details;
    print "Gst plugin base status details : %s" %details;
    details=dict(item.split(":") for item in details.split(" "))
    Resultvalue=details.values();
    if int(Resultvalue[0])==(int(Resultvalue[1])+int(Resultvalue[2])) and int(Resultvalue[2])==0 and expectedresult in actualresult :
       tdkTestObj.setResultStatus("SUCCESS");print "Result Status: SUCCESS\n";
    else:
       tdkTestObj.setResultStatus("FAILURE");print "Result Status: FAILURE\n";
     
    #Get the log path of the Gst plugin base Testsuite
    logpath =tdkTestObj.getLogPath();
    if "TestSummary.log" in logpath:
       data4 = logpath; 
       print "Log Path :%s"%logpath;
       #Transferring the Gst plugin base Testsuite Logs
       tdkTestObj.transferLogs( logpath, "true" );
    else:
       print "Log path is not available and transfer of logs will not be initialised";
  else :
     print "Gst plugin base status details:%s" %details;
     print "Proper Execution details are not received due to error in execution";
     tdkTestObj.setResultStatus("FAILURE");
     print "Result Status: FAILURE\n";
  outData = data1 + "<br/>" + data2 + "<br/>" + data3 + "<br/>" + data4;
  print "OutData value in GstreamerBasePluginTestNew: " +outData;
  devName = execName.split("-")
  obj.insertExecutionDetails(executionTime, "GstreamerTest", tdkTestObj, outData, devName[0], execMethResId);
  print "After calling insertExecutionDetails function";
	 
  #Unloading the opensource test suite module
  obj.unloadModule("opensourcetestsuite");#print "Result Status: "+result;

else:
  print "Failed to load Opensource test module";#print "Result Status: "+result;
sys.exit(execId)
