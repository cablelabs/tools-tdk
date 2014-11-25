/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */

#include "xupnpAgent.h"


std::string g_tdkPath = getenv("TDK_PATH");
#define PRE_REQ_CHECK "xupnp_pre_req_chk.txt"
#define TDK_XUPNP_OUTPUT_JSON "xupnp_output.txt" 
#define TDK_XUPNP_XML_DIR "BasicDevice.xml" 
std::string localOutputJsonFile = g_tdkPath + "/" + TDK_XUPNP_OUTPUT_JSON;
  

/*************************************************************************
Function name : searchPattern

Arguments     : file path and search pattern

return       : true if log msg is found
               false if log msg is not found

Description   : used to check for the pattern in the file.
***************************************************************************/
bool searchPattern(const char* filepath , const char* search)
{
    string line;
    ifstream logFile;
    DEBUG_PRINT(DEBUG_LOG,"\nInside the search pattern file name is %s and pattern is %s\n",filepath, search);

    logFile.open(filepath, ios::in);
    if(logFile.is_open())
    {
        while(logFile.good())
        {
            getline(logFile,line);
            if (line.find(search, 0) != string::npos) 
            {
		logFile.close();
    		DEBUG_PRINT(DEBUG_LOG,"\nInside the search pattern true block");
             	return true;
            }
        }
        logFile.close();
    }
    else
    {
    DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open file %s\n",filepath);
    }
    return false;
}


/*************************************************************************
Function name : localOutputfile

Arguments     : NULL

Description   : used to create a local copy of output file for verifying
***************************************************************************/

bool localOutputfile(void)
{
	// Make a copy of output.json file for verifying
     	
	std::string pre_req_chk;
        std::string pre_req_chk_file;
        pre_req_chk_file= g_tdkPath + "/" + TDK_XUPNP_OUTPUT_JSON;
        pre_req_chk ="/opt/output.json";
	int flag=0;
        std::ifstream Myfile;

        Myfile.open (pre_req_chk.c_str());

	if(Myfile.is_open())
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nXupnp /opt/output.json exists and copying to TDK\n");
                flag=1;
		//return TEST_SUCCESS;
                
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nXupnp /opt/output.json File not found.\n");
		flag=0; 
                //return TEST_FAILURE;
        }
        if(flag==1)
        {
	        Myfile.close();
        	pre_req_chk ="cp /opt/output.json " + pre_req_chk_file;
       		try
        	{
                	system((char *)pre_req_chk.c_str());
        	}
        	catch(...)
	        {
        	        DEBUG_PRINT(DEBUG_ERROR,"Error copying of output.json to TDK folder for verification\n");
                	DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
	                return TEST_FAILURE;
        	}
	
		DEBUG_PRINT(DEBUG_TRACE, " copied output.json to TDK for verification\n");
        	return TEST_SUCCESS;
	}
	else{
                DEBUG_PRINT(DEBUG_ERROR,"\nXupnp /opt/output.json File not found.\n");
                return TEST_FAILURE;
	    }
}







/*************************************************************************
Function name : XUPNPAgent::XUPNPAgent

Arguments     : NULL

Description   : Constructor for XUPNPAgent class
***************************************************************************/

XUPNPAgent::XUPNPAgent()
{
        DEBUG_PRINT(DEBUG_LOG, "XUPNPAgent Initialized\n");
}

/**************************************************************************
Function name : XUPNPAgent::initialize

Arguments     : Input arguments are Version string and XUPNPAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool XUPNPAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
        DEBUG_PRINT(DEBUG_ERROR, "XUPNPAgent Initialization\n");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_checkjson, "TestMgr_XUPNPAgent_checkjson");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_checkSTRurl, "TestMgr_XUPNPAgent_checkSTRurl");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_checkSerialNo, "TestMgr_XUPNPAgent_checkSerialNo");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_checkPBurl, "TestMgr_XUPNPAgent_checkPBurl");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_recordId, "TestMgr_XUPNPAgent_recordId");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_ModBasicDevice, "TestMgr_XUPNPAgent_ModBasicDevice");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_removeXmls, "TestMgr_XUPNPAgent_removeXmls");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_evtCheck, "TestMgr_XUPNPAgent_evtCheck");
// ---TODO ---
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_evttuneready, "TestMgr_XUPNPAgent_evttuneready");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_evtChannelMap, "TestMgr_XUPNPAgent_evtChannelMap");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_evtControllerID, "TestMgr_XUPNPAgent_evtControllerID");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_evtPlantID, "TestMgr_XUPNPAgent_evtPlantID");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_evtvodID, "TestMgr_XUPNPAgent_evtvodID");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_evtTimezone, "TestMgr_XUPNPAgent_evtTimezone");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_IFDown, "TestMgr_XUPNPAgent_IFDown");
	ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_IPIFDown, "TestMgr_XUPNPAgent_IPIFDown");

        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string XUPNPAgent::testmodulepre_requisites()
{
	DEBUG_PRINT(DEBUG_TRACE, "XUPNP testmodule pre_requisites --> Entry\n");
        
	std::string pre_req_chk;
        std::string pre_req_chk_file;
        pre_req_chk_file= g_tdkPath + "/" + PRE_REQ_CHECK;
        pre_req_chk ="pidstat | grep xcal & pidstat | grep xdis >" + pre_req_chk_file;
        int offset;
        std::string line;
        std::ifstream Myfile;
        std::string  srchXcal = "xcal-device";    
        std::string  srchXdis = "xdiscovery";    
        int flag =0; 
	bool cpTXT;
         //* To handle exception for system call
        try
        {
                system((char *)pre_req_chk.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured during pidstat xupnp xcal-device verification\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return "FAILURE:Exception occured during pidstat xupnp xcal-device verification";
        }
        Myfile.open (pre_req_chk_file.c_str());

        if(Myfile.is_open())
        {
                while(!Myfile.eof())
                {
                        getline(Myfile,line);

                	DEBUG_PRINT(DEBUG_ERROR,"line n\n");
                        if ((offset = line.find(srchXcal, 0)) != std::string::npos) {
                                
				DEBUG_PRINT(DEBUG_LOG,"\nxcal-device process is running\n");
                                flag = 1;
                        }
                        if ((offset = line.find(srchXdis, 0)) != std::string::npos) {
                                
				DEBUG_PRINT(DEBUG_LOG,"\nxdiscovery process is running\n");
                                flag = 1; 
                        }
                }
                Myfile.close();
                if (flag==1)
                {
			cpTXT = localOutputfile();
			DEBUG_PRINT(DEBUG_LOG,"\n local output file is created ");
			if(cpTXT)
			return "SUCCESS:xcal-device and xdiscovery process is running";
			else
			return "FAILURE:xcal-device and xdiscovery process is running but local cp of Json failed";

                }
                else
		{

		DEBUG_PRINT(DEBUG_ERROR,"\nXupnp pre-requisites not present\n");
                return "FAILURE: Xupnp pre-requisites not present";
 		}
	}
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open preq Xupnp txt file.\n");
                return "FAILURE:Unable to open preq Xupnp txt file.";
        }


}



/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool XUPNPAgent::testmodulepost_requisites()
{
	DEBUG_PRINT(DEBUG_TRACE, "XUPNP testmodule post_requisites --> Entry\n");

	// Remove the local copy ofioutput.json
        try
        {
                system((char *)localOutputJsonFile.c_str());
        }
        catch(...)
        {
		DEBUG_PRINT(DEBUG_ERROR,"\n%s: Error deleting file /opt/TDK/output.json \n", __FUNCTION__);
		DEBUG_PRINT(DEBUG_TRACE, "XUPNP testmodule post requisites --> Exit");
		return TEST_FAILURE;
	}


	DEBUG_PRINT(DEBUG_TRACE, "file successfully deleted/opt/TDK/output.json\n");
	DEBUG_PRINT(DEBUG_TRACE, "XUPNP testmodule post requisites --> Exit");
	return TEST_SUCCESS;

}


/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_checkjson

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to check the JSON messsage is present or not.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_checkjson(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkjson --->Entry\n");


        if (true ==  localOutputfile())
	{
        	response["result"] = "SUCCESS";
        	response["details"] = "pre req is met and output.json is available for testing success";
	}
	else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed: output.json is not available for testing success\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed: output.json is not available for testing";
                DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkjson -->Exit\n");
                return TEST_FAILURE;
        }

     	DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkjson -->Exit\n");

       	return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_checkSTRurl

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to check the basestreamingurl is present in the json message.
**************************************************************************/

bool XUPNPAgent::XUPNPAgent_checkSTRurl(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkSTRurl --->Entry\n");

	char testMsg[64] = {'\0'};
        sprintf(testMsg, "%s","baseStreamingUrl" );
	DEBUG_PRINT(DEBUG_LOG, "search pattern file is %s \n and pattern is %s", localOutputJsonFile.c_str(),testMsg);
      	bool srFound; 
	srFound =  searchPattern((char *)localOutputJsonFile.c_str(),testMsg);
	DEBUG_PRINT(DEBUG_LOG,"\nsrFound output is %d\n", (int)srFound);
	if(srFound)
//	if (true == searchPattern((char *)localOutputJsonFile.c_str(),testMsg))
	{
                DEBUG_PRINT(DEBUG_TRACE, "SUCCESS: baseStreamingUrl is present in output.json\n");
        	response["result"] = "SUCCESS";
        	response["details"] = "streaming url is present in the Json file";
                return TEST_SUCCESS;
	}
	else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed: baseStreamingUrl is not present in output.json\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed: baseStreamingUrl is not present in output.json";
                DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkSTRurl -->Exit\n");
                return TEST_FAILURE;
        }
        cout<<" details at the exit of function"<<response["details"]<<endl;
	DEBUG_PRINT(DEBUG_LOG, "search pattern file is %s \n and details ", localOutputJsonFile.c_str());

}


/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_checkSerialNo

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to check the serial no is present in the json message.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_checkSerialNo(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkSerialNo --->Entry\n");
 
	int flag=0;
	std::string serialNo; 
        char testMsg[64] = {'\0'};


        sprintf(testMsg, "%s","sno" );
        if (true == searchPattern( (char*)localOutputJsonFile.c_str(),testMsg ))
        {
                response["result"] = "SUCCESS";
                response["details"] = "serial NO is present in the Json file";
		flag=1;
                //return TEST_SUCCESS;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed: Serial NO is not present in output.json\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed: serial NO is not present in output.json";
                DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkSTRurl -->Exit\n");
                return TEST_FAILURE;
        }

	if (flag==1)

        {
	    std::string line;
	    ifstream logFile;
	    logFile.open("/tmp/mpeos_vendor_info.txt", ios::in);
	    if(logFile.is_open())
		    {
		        while(logFile.good())
		        {
		            getline(logFile,line);
		            if (line.find("Serial Number", 0) != string::npos)
		            {
		                size_t pos=line.find("PAPV"); 
				serialNo=line.substr(pos); 
				cout<<"serialNO:"<<serialNo<<endl;		
                                logFile.close();
				break;
	            	    }		
	        	}
    		}
    		else
    		{
	        DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open file /tmp/mpeos_vendor_info.txt\n");
		}

	}

        sprintf(testMsg, "%s", serialNo.c_str());
	if (true == searchPattern((char*)localOutputJsonFile.c_str(),testMsg))
        {
                response["result"] = "SUCCESS";
                response["details"] = " SUCCESS:serial No is verified";
                return TEST_SUCCESS;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed: Serial No is not present\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed: Serial No is not present";
                return TEST_FAILURE;
        }

	DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkSerialNo -->Exit\n");
}

/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_checkPBurl

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to check the playbackurl is present in the json message.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_checkPBurl(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkPBurl --->Entry\n");

        char testMsg[64] = {'\0'};
        sprintf(testMsg, "%s","playbackUrl" );
        if (true == searchPattern((char *)localOutputJsonFile.c_str(),testMsg))
        {
                response["result"] = "SUCCESS";
                response["details"] = " playbackUrl is present in the Json file";
                return TEST_SUCCESS;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed:playbackUrl is not present in output.json\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed: playbackUrl is not present in output.json";
        	DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkPBurl -->Exit\n");
                return TEST_FAILURE;
        }


        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkPBurl -->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_recordId

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to check the recordId is present in the json message.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_recordId(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_recordId --->Entry\n");
        int flag=0;
        std::string serialNo;
        char testMsg[64] = {'\0'};

        if (true ==  localOutputfile())
        {
                response["result"] = "SUCCESS";
                response["details"] = "output.json is available for testing";
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed: output.json is not available for testing success\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed: output.json is not available for testing";
                return TEST_FAILURE;
        }

        sprintf(testMsg, "%s","receiverid" );
        if (true == searchPattern( (char*)localOutputJsonFile.c_str(),testMsg ))
        {
                response["result"] = "SUCCESS";
                response["details"] = "serial NO is present in the Json file";
                flag=1;
                //return TEST_SUCCESS;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed: Serial NO is not present in output.json\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed: serial NO is not present in output.json";
                DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_checkSTRurl -->Exit\n");
                return TEST_FAILURE;
        }
        if (flag==1)

        {
        system("cat /opt/www/whitebox/wbdevice.dat > /opt/TDK/recvLog.txt");
        }
            
        char filePath[64] = {'\0'};
        sprintf(filePath, "%s","/opt/TDK/recvLog.txt" );
        sprintf(testMsg, "%s", serialNo.c_str());
        if (true == searchPattern(filePath,testMsg))
        {
                response["result"] = "SUCCESS";
                response["details"] = " SUCCESS:receiverid is verified";
                return TEST_SUCCESS;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed: receiverid not  is not present\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed: receiverid is not present";
                return TEST_FAILURE;
        }

        system("rm /opt/TDK/recvLog.txt");
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_recordId -->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_ModBasicDevice

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to modify the xml file and check the behavior message.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_ModBasicDevice(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_ModBasicDevice --->Entry\n");

        std::string clear_xml_in_TDK;
        std::string cp_xml_to_TDK;
        std::string cp_xml_to_opt;
        std::string mod_xml_in_opt;
        std::string pre_req_chk_file;
        pre_req_chk_file= g_tdkPath + "/";
        cp_xml_to_TDK ="cp /opt/xupnp/BasicDevice.xml "+pre_req_chk_file;
        cp_xml_to_opt ="cp /opt/TDK/BasicDevice.xml /opt/xupnp/BasicDevice.xml";
        clear_xml_in_TDK ="rm /opt/TDK/*.xml";
        std::ifstream Myfile;
        //Clearing the xml file is it already present in the TDK
        try
        {
                system((char *)clear_xml_in_TDK.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Error clearing the xml file is it already present in the TDK \n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
        }
         //Copying the BasicDevice.xml from .opt folder to TDK for backup
        try
        {
                system((char *)cp_xml_to_TDK.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Error Copying the BasicDevice.xml from .opt folder to TDK for backup\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
        }
        //loging to corrupt the Basicdevice.xml
        
	try
        {
        	mod_xml_in_opt ="cat /opt/xupnp/BasicDevice.xml >  /opt/xupnp/BasicDevice_org.xml";
                system((char *)mod_xml_in_opt.c_str());
                mod_xml_in_opt ="sed '7,10d' /opt/xupnp/BasicDevice_org.xml >  /opt/xupnp/BasicDevice.xml";
                system((char *)mod_xml_in_opt.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Error copying of output.json to TDK folder for verification\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
        }
	
	//startupnp again
        std::string cmd_start_xupnp;
	 try
        {
          	cmd_start_xupnp= "killal xcal-device xdiscovery";
          	system((char *)cmd_start_xupnp.c_str());
		cmd_start_xupnp= "sh /lib/rdk/start_upnp.sh /var/logs/pipe_xdiscovery_log &";
		system((char *)cmd_start_xupnp.c_str());
	
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Error n restarting the xupnp.sh  \n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
        }
        usleep(4000000);
        //Verify the file
	char testMsg[64] = {'\0'};
        sprintf(testMsg, "%s","XfinityMediaGateway" );
        cmd_start_xupnp= "/opt/xupnp/BasicDevice.xml";
        if (true == searchPattern((char *)cmd_start_xupnp.c_str(),testMsg))
        {
                response["result"] = "SUCCESS";
                response["details"] = " Success: Basic device is updated";
                //return TEST_SUCCESS;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed:Basic device is not updated\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed:Basic device is not updated";
                return TEST_FAILURE;
        }
 
        //Copy back the original .xml file is not required

	DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_ModBasicDevice -->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_removeXmls

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to remove all the  xml files refered by the process xcal-device and xdiscovery and check the behavior message.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_removeXmls(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_removeXmls --->Entry\n");
	
        std::string cmd_start_xupnp;
        try
        {
                cmd_start_xupnp= "rm /opt/xupnp/*.xml";
                system((char *)cmd_start_xupnp.c_str());
          	cmd_start_xupnp= "killal xcal-device xdiscovery";
          	system((char *)cmd_start_xupnp.c_str());
		cmd_start_xupnp= "sh /lib/rdk/start_upnp.sh /var/logs/pipe_xdiscovery_log &";
		system((char *)cmd_start_xupnp.c_str());

        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Error n restarting the xupnp.sh  \n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
        }
        usleep(4000000);
        //Verifcation the file
        char testMsg[64] = {'\0'};
        sprintf(testMsg, "%s","XfinityMediaGateway" );
        cmd_start_xupnp= "/opt/xupnp/BasicDevice.xml";
        if (true == searchPattern((char *)cmd_start_xupnp.c_str(),testMsg))
        {
                response["result"] = "SUCCESS";
                response["details"] = " Success: All xml are copied back to /opt/xupnp/from /etc ";
                //return TEST_SUCCESS;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed: All xmls are not copied back to /opt/xupnp/from /etc\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed: All xml are not copied back to /opt/xupnp/from /etc";
                return TEST_FAILURE;
        }

        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_removeXmls -->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_evtCheck

Arguments     : Input argument : 2 , evtName and evtValue 
		Output argument : "SUCCESS"  is TRUE
			  	  "FAILURE"  is FALSE

Description   : Common function to receive the request from Test Manager to check the sysmgrs events triggered from iarmbus is received or not. 
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_evtCheck(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_eventCheck --->Entry\n");
	std::string cmd_start_xupnp;
        try
        {
                cmd_start_xupnp= "tail -12 /opt/logs/xdevice.log > /opt/TDK/tdkXupnpEvtChkLog";
                system((char *)cmd_start_xupnp.c_str());

        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Error in restarting the xupnp.sh  \n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
        }

        std::string discovery_log_path;
        discovery_log_path = "/opt/TDK/tdkXupnpEvtChkLog";
        char testMsg[64] = {'\0'};
        string evtName = req["evtName"].asString();
        string evtValue = req["evtValue"].asString();
        if(evtName.compare("serialNo")==0){
	//sprintf(testMsg, "%s","IARM_BUS_SYSMGR_SYSSTATE_CABLE_CARD_SERIAL_NO" );
	sprintf(testMsg, "%s",evtValue.c_str());
	}
        else if(evtName.compare("tuneReady")==0){
        sprintf(testMsg, "%s","Tune Ready Update Received:" );
	}
        else if(evtName.compare("channelMap")==0){
        sprintf(testMsg, "%s","Received channel map update" );
	}
        else if(evtName.compare("controllerID")==0){
        sprintf(testMsg, "%s","Received controller id update" );
	}
        else if(evtName.compare("plantID")==0){
        sprintf(testMsg, "%s","Received plant id update" );
	}
        else if(evtName.compare("vodID")==0){
        sprintf(testMsg, "%s","Received vod server id update" );
	}
        else if(evtName.compare("timeZone")==0){
        sprintf(testMsg, "%s","Received timezone update" );
	}
	bool srchXdeviceLog = searchPattern((char *)discovery_log_path.c_str(),testMsg); 
	
         if(srchXdeviceLog)
        //if (true == searchPattern((char *)discovery_log_path.c_str(),testMsg))
        {
                DEBUG_PRINT(DEBUG_TRACE, " SUCCESS: IARM_BUS_SYSMGR_SYSSTATE_EVT is recieved by xdevice process\n");
                response["result"] = "SUCCESS";
                response["details"] = " SUCCESS: IARM_BUS_SYSMGR_SYSSTATE_EVT is recieved by xdevice process";
                //return TEST_SUCCESS;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed:IARM_BUS_SYSMGR_SYSSTATE_EVT is not recieved by xdevice process\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed:IARM_BUS_SYSMGR_SYSSTATE_EVT is not recieved by xdevice process\n ";
                return TEST_FAILURE;
        }
//verification in output.json
/*
        sprintf(testMsg, "%s", evtValue.c_str());
// Sleep is required to update the output json 
	usleep(550000);

        char outputJsonpath[64]= {'\0'};

        sprintf(outputJsonpath, "%s", "/opt/output.json");
        if (true == searchPattern( outputJsonpath,testMsg))
        {
                response["result"] = "SUCCESS";
                response["details"] = " Success: IARM_BUS_SYSMGR_EVT  is updated in the output.json";
                //return TEST_SUCCESS;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed:IARM_BUS_SYSMGR_SYSSTATE_EVT is received but not updated in the output.json\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed:IARM_BUS_SYSMGR_SYSSTATE__EVT is received but not updated in the output.json\n ";
                return TEST_FAILURE;
        }
*/
	system("rm /opt/TDK/tdkXupnpEvtChkLog");
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evtCheck --> Exit\n");
        return TEST_SUCCESS;
	
}
/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_evttuneready

Arguments     : Input argument : 2 , evtName and evtValue 
		Output argument : "SUCCESS"  is TRUE
			  	  "FAILURE"  is FALSE

Description   : Common function to receive the request from Test Manager to check the sysmgrs events triggered from iarmbus is received or not. 
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_evttuneready(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evttuneready --->Entry\n");

     	response["details"] = "dummy success";
    	DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evttuneready -->Exit\n");
     	return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_evtChannelMap

Arguments     : Input argument : 2 , evtName and evtValue 
		Output argument : "SUCCESS"  is TRUE
			  	  "FAILURE"  is FALSE

Description   : Common function to receive the request from Test Manager to check the sysmgrs events triggered from iarmbus is received or not. 
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_evtChannelMap(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evtChannelMap --->Entry\n");

        response["details"] = "dummy success";
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evtChannelMap -->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_evtControllerID
Arguments     : Input argument : 2 , evtName and evtValue
                Output argument : "SUCCESS"  is TRUE
                                  "FAILURE"  is FALSE

Description   : Common function to receive the request from Test Manager to check the sysmgrs events triggered from iarmbus is received or not.
**************************************************************************/

bool XUPNPAgent::XUPNPAgent_evtControllerID(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evtControllerID --->Entry\n");

        response["details"] = "dummy success";
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evtControllerID -->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_evtPlantID
Arguments     : Input argument : 2 , evtName and evtValue
                Output argument : "SUCCESS"  is TRUE
                                  "FAILURE"  is FALSE

Description   : Common function to receive the request from Test Manager to check the sysmgrs events triggered from iarmbus is received or not.
**************************************************************************/

bool XUPNPAgent::XUPNPAgent_evtPlantID(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evtPlantID --->Entry\n");

        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evtPlantID -->Exit\n");
        response["details"] = "dummy success";
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent::XUPNPAgent_evtvodID
Arguments     : Input argument : 2 , evtName and evtValue
                Output argument : "SUCCESS"  is TRUE
                                  "FAILURE"  is FALSE

Description   : Common function to receive the request from Test Manager to check the sysmgrs events triggered from iarmbus is received or not.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_evtvodID(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evtvodID --->Entry\n");

	DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_evtvodID -->Exit\n");
	response["details"] = "dummy success";
        return TEST_SUCCESS;
	
}

bool XUPNPAgent::XUPNPAgent_evtTimezone(IN const Json::Value& req, OUT Json::Value& response)
{
        response["details"] = "dummy success";
        return TEST_SUCCESS;

}

bool XUPNPAgent::XUPNPAgent_IFDown(IN const Json::Value& req, OUT Json::Value& response)
{
        response["details"] = "dummy success";
        return TEST_SUCCESS;
}


bool XUPNPAgent::XUPNPAgent_IPIFDown(IN const Json::Value& req, OUT Json::Value& response)
{
        response["details"] = "dummy success";
        return TEST_SUCCESS;
}

/****ee********************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "XUPNPAgent".
**************************************************************************/

extern "C" XUPNPAgent* CreateObject()
{
        return new XUPNPAgent();
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
**************************************************************************/

bool XUPNPAgent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
        DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
        if(NULL == ptrAgentObj)
        {
                return TEST_FAILURE;
        }
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_checkjson");
 	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_checkSTRurl");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_checkSerialNo");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_checkPBurl");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_recordId");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_ModBasicDevice");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_removeXmls");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_evtCheck");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_evttuneready");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_evtChannelMap");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_evtControllerID");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_evtPlantID");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_evtvodID");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_evtTimezone");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_IFDown");
	ptrAgentObj->UnregisterMethod("TestMgr_XUPNPAgent_IPIFDown");

        return TEST_SUCCESS;
}
/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is XUPNPAgent Object

Description   : This function will be used to destory the XUPNPAgent object.
**************************************************************************/
extern "C" void DestroyObject(XUPNPAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying RDKLogger Agent object\n");
        delete stubobj;
}
