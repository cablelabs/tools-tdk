'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1369</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKLogger_CheckMPELogEnabled</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>590</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RDKLogger_CheckMPELogEnabled</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if EnableMPELog is enabled in debug.ini file
Test Case ID: CT_RDKLogger_30
Test Type: Positive</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

def Create_ExecuteTestcase(obj,primitivetest,expectedresult,verifyList, **kwargs):
    print kwargs
    details = "NULL";
 
    #calling primitive test case    
    tdkTestObj = obj.createTestStep(primitivetest);
    for name, value in kwargs.iteritems():
      
        print "Name: %s"%str(name);
        tdkTestObj.addParameter(str(name),value);                                   
       
    Expectedresult=expectedresult;
    tdkTestObj.executeTestCase(Expectedresult); 
    actualresult = tdkTestObj.getResult();
    print "Actual Result: %s"%actualresult;
    
    try: 
        details = tdkTestObj.getResultDetails();
        print "Details:%s"%details;
    except:                
        pass;
    
    #Check for SUCCESS/FAILURE return value 
    if Expectedresult in actualresult:
        count = 0;
        if verifyList:
            print "Verify List not empty"
            for name,value in verifyList.items():	
                print "Name:%s,Value:%s to be verified in the details"%(name,value);
                if value in details:
            	    print details;	    
                    print "SUCCESS : %s sucess"%primitivetest;
                    count+=1;
                    if count > 0:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS:%s"%(primitivetest);
                else:                    
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE:Value not in details %s" %details;
        else:          
            tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");            
    
    return (actualresult,tdkTestObj,details);


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdklogger","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKLogger_CheckMPELogEnabled');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

print "rdklogger module loading status :%s" %result;

#Check for SUCCESS/FAILURE of rdklogger module
if "SUCCESS" in result.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");
        
    actualresult,tdkTestObj_cc,details = Create_ExecuteTestcase(obj,'RDKLogger_CheckMPELogEnabled', 'SUCCESS',verifyList ={} );

    #unloading rdklogger module
    obj.unloadModule("rdklogger");
    
else:
    print "Failed to load rdklogger module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
