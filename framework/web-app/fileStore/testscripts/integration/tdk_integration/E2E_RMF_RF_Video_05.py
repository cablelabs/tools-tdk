'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1108</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_RF_Video_05</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>557</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMF_Linear_simultuning</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>E2E_RMF_RF_Video_05: To verify 4 SD service &amp; 2 HD services are playing from six XI3 boxes simultaneously.
Note: Tested only with 2 XI3 client Boxes</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>7</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This script is tested on the ipnetwork with two ipclient boxes connected, Not tested on Moca network</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
import tdklib;
import time;
from tdklib import CreateTestThread

#Add ip and portnumbers of the client boxes to be tested.
xi3_1 = "192.168.30.120"
xi3_1_port = 8087
URL1 = 'http://192.168.30.80:8080/vldms/tuner?ocap_locator=ocap://0xa3'

xi3_2 = "192.168.30.122"
xi3_2_port = 8087
URL2 = 'http://192.168.30.80:8080/vldms/tuner?ocap_locator=ocap://0xa1'

SUCCESS = 0
FAILURE = 1

def TDKE2E_Linear_simultuning(IP,portnumber,args=(),kwargs={}):

   print "URL = " + str(kwargs["URL"])
   URL = str(kwargs["URL"])

   #Test component to be tested
   obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

   #IP and Port of box, No need to change,
   #This will be replaced with corresponding Box Ip and port while executing script
   ip = IP
   port = portnumber

   print "E2e rmf scirpt called"
   obj.configureTestCase(ip,port,'TDKE2E_RMF_RF_Video_05');

   #Get the result of connection with test component and STB
   result =obj.getLoadModuleResult();
   print "e2e_rmf module [LIB LOAD STATUS]  :  %s" %result;

   if "SUCCESS" in result.upper():
       obj.setLoadModuleStatus("SUCCESS");
       print "e2e rmf module load successful";

       #Prmitive test case which associated to this Script
       tdkTestObj = obj.createTestStep('TDKE2E_RMF_Linear_simultuning');

       #set the dvr play url
       url = URL
       print "The Play Url Requested: %s"%url
       tdkTestObj.addParameter("playUrl",url);

       #Execute the test case in STB
       expectedresult="SUCCESS";
       tdkTestObj.executeTestCase(expectedresult);
       #Get the result of execution
       actualresult = tdkTestObj.getResult();
       details =  tdkTestObj.getResultDetails();
       print "Simultaneus tuning from client box [TEST EXECUTION RESULT] : %s" %actualresult;
       print "Box with IP: %s"%ip
       print "Channel tuning " + actualresult
       tdkTestObj.setResultStatus(actualresult);
       print "Simultaneous tuning: " + actualresult + " [%s]"%details;
       print " "
       time.sleep(40);
       obj.unloadModule("tdkintegration");
   else:
       print "Failed to load e2e_rmf module";
       obj.setLoadModuleStatus("FAILURE");

   return SUCCESS

# Create new threads
test1 = CreateTestThread(xi3_1,xi3_1_port,TDKE2E_Linear_simultuning,kwargs={"URL":URL1})
test2 = CreateTestThread(xi3_2,xi3_2_port,TDKE2E_Linear_simultuning,kwargs={"URL":URL2})



# Start new Threads
test1.start()
test2.start()
test1.join()
test2.join()
try:
    print "test1 return value = %s" %(test1.returnValue)
except AttributeError:
    print "No return value for test 1"
try:
    print "test2 return value = %s" %(test2.returnValue)
except AttributeError:
    print "No return value for test 2"