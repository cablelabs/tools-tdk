'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1575</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_LinearTV_Stress_LivePlay_SwitchingChannel_LongDuration</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Live play back and continuous switching of channels for long duration(10hrs).
E2E_LinearTV_45</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>630</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from tdkintegration import getURL_PlayURL;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
                                        
obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_Stress_Live_SwitchingChannel_LongDuration');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "TDKIntegration module loading status : %s" %result;

if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";
    
    for i in range(1,600):
                                        
        #Calling the getURL_PlayURL function for the requested StreamID
        result1 = getURL_PlayURL(obj,'01');

        #Calling the getURL_PlayURL function for the requested StreamID
        result2 = getURL_PlayURL(obj,'02');
        
        if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                        
            print "Execution Success at iteration %d"%i;
        else:            
            print "Execution failure at iteration %d"%i;
            break;                                        
         
    obj.unloadModule("tdkintegration");
else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");
