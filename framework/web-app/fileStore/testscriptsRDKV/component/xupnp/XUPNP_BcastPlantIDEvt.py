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
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>XUPNP_BcastPlantIDEvt</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>XUPNP_BroadcastEvent</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To broadcast Plant ID event and check if xcal-device process receives it.
Testcase ID: CT_XUPNP_37</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
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
from iarmbus import IARMBUS_Init,IARMBUS_Connect,IARMBUS_DisConnect,IARMBUS_Term;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");
iarmObj.configureTestCase(ip,port,'XUPNP_BcastPlantIDEvt');
#Get the result of connection with test component and STB
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "Iarmbus module loading status : %s" %iarmLoadStatus ;
#Set the module loading status
iarmObj.setLoadModuleStatus(iarmLoadStatus);

if "SUCCESS" in iarmLoadStatus.upper():
        #Calling IARMBUS API "IARM_Bus_Init"
        result = IARMBUS_Init(iarmObj,"SUCCESS")
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if "SUCCESS" in result:
                #Calling IARMBUS API "IARM_Bus_Connect"
                result = IARMBUS_Connect(iarmObj,"SUCCESS")
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
                if "SUCCESS" in result:
                        xUpnpObj = tdklib.TDKScriptingLibrary("xupnp","2.0");
                        xUpnpObj.configureTestCase(ip,port,'XUPNP_BcastPlantIDEvt');
                        #Get the result of connection with test component and STB
                        xupnpLoadStatus = xUpnpObj.getLoadModuleResult();
                        print "XUPNP module loading status : %s" %xupnpLoadStatus;
                        #Set the module loading status
                        xUpnpObj.setLoadModuleStatus(xupnpLoadStatus);

                        if "SUCCESS" in xupnpLoadStatus.upper():
                                tdkTestObj = xUpnpObj.createTestStep('XUPNP_BroadcastEvent');
                                expectedresult="SUCCESS";
                                #Configuring the test object for starting test execution
                                tdkTestObj.addParameter("stateId",32);
                                tdkTestObj.addParameter("eventLog","Received plant id update");
                                tdkTestObj.addParameter("payload","0000");
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                #Check for SUCCESS return value of Testcase
                                if "SUCCESS" in actualresult.upper():
                                        tdkTestObj.setResultStatus("SUCCESS");
                                	print "Broadcasting PlantID Event Result : %s"%actualresult;
	                                print "Details : %s"%details;
                                else:
	                                tdkTestObj.addParameter("stateId",32);
	                                tdkTestObj.addParameter("eventLog","plant id available");
	                                tdkTestObj.addParameter("payload","0000");
	                                tdkTestObj.executeTestCase(expectedresult);
	                                actualresult = tdkTestObj.getResult();
	                                details = tdkTestObj.getResultDetails();
	                                print "Broadcasting PlantID Event Result : %s"%actualresult;
        	                        print "Details : %s"%details;
					if "SUCCESS" in actualresult.upper():
						tdkTestObj.setResultStatus("SUCCESS");
					else:
						tdkTestObj.setResultStatus("FAILURE");
                                #Unload xupnp module
                                xUpnpObj.unloadModule("xupnp");

                        #Calling IARM_Bus_DisConnect API
                        result = IARMBUS_DisConnect(iarmObj,"SUCCESS")
                #calling IARMBUS API "IARM_Bus_Term"
                result = IARMBUS_Term(iarmObj,"SUCCESS")
        #Unload iarmbus module
        iarmObj.unloadModule("iarmbus");
