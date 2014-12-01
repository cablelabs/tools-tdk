/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file (and its contents) are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */

#include "opensrcteststub.h"

/*************************************************************************************************
 *Function name	: OpensourceTestStub 
 *Descrption	: This is a constructor function for OpensourceTestStub class. 
 ************************************************************************************************/ 
OpensourceTestStub::OpensourceTestStub()
{
	DEBUG_PRINT(DEBUG_LOG,"OpensourceTestStub Initialized");
}

/***************************************************************************************************
 *Function name	: initialize
 *Descrption	: Initialize Function will be used for registering the wrapper method 
 * 	 	  with the agent so that wrapper functions will be used in the 
 *  		  script
 ***************************************************************************************************/ 
bool OpensourceTestStub::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nOpensourceTestStub Initialize");
	/*Register stub function for callback*/
	ptrAgentObj->RegisterMethod(*this,&OpensourceTestStub::OpensourceTestStub_Execute, "TestMgr_Opensource_Test_Execute");
	return true;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string OpensourceTestStub::testmodulepre_requisites()
{
        return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool OpensourceTestStub::testmodulepost_requisites()
{
        return true;
}

/*******************************************************************************************************
 *Function name	: OpensourceTestStub_Execute
 *Descrption	: OpensourceTestStub_Execute wrapper function will be used to execute opensource test suites
 *******************************************************************************************************/ 
bool OpensourceTestStub::OpensourceTestStub_Execute(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nEntering OpensourceTestStub_Execute function");
	if (getenv ("OPENSOURCETEST_PATH")!=NULL)
	{
		/* Declaring the variables */
		string testenvPath,executerPath, logger_path,get_status;
		int iTestAppStatus;

		testenvPath = getenv ("OPENSOURCETEST_PATH");
		if (testenvPath.empty()==0)
		{
			executerPath.append(testenvPath);
			executerPath.append("/");
			executerPath.append(MASTERSUITE_NAME);
			
			/*Creating the process for Suite execution*/
			char *component_option=(char*)req["Opensource_component_type"].asCString();
			DEBUG_PRINT(DEBUG_LOG,"\nopensource component option %s",component_option);

			pid_t idChild = vfork();
			if(idChild == 0)
			{
				/*getting the display options from the test framework*/
				char *display_selection=(char*)req["Display_option"].asCString();
				if (strcmp(component_option,"qt_gfx") == 0) 
				{
					/*Executing the suite executer script to invoke all qt graphical test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the QT Graphics tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","qt_gfx","-o",display_selection,NULL);
				}
				else if(strcmp(component_option,"qt_non_gfx") == 0)
				{
					/*Executing the suite executer script to invoke all qt non graphical test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the QT non graphics tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","qt_non_gfx",NULL);
				}
				else if(strcmp(component_option,"webkit") == 0)
				{
					/*Executing the suite executer script to invoke all webkit test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the Webkit tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","webkit","-o",display_selection,NULL);       
				}
				else if(strcmp(component_option,"gstreamer") == 0)
				{
					/*Executing the suite executer script to invoke all Gstreamer test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the Gstreamer tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","gstreamer",NULL);       
				}
				else if(strcmp(component_option,"gst-plugin-base") == 0)
				{
					/*Executing the suite executer script to invoke all Gst-Plugin-base test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the Gst-plugin-base tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","gst_plugin_base",NULL);       
				}
				else if(strcmp(component_option,"gst-plugin-custom") == 0)
				{
					/*Executing the suite executer script to invoke all Gst-Plugin-base test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the Gst-plugin-custom tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","gst_plugin_custom",NULL);       
				}
				else if(strcmp(component_option,"gst-plugin-good") == 0)
				{
					/*Executing the suite executer script to invoke all Gst-Plugin-good test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the Gst-plugin-good tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","gst_plugin_good",NULL);       
				}
				else if(strcmp(component_option,"glib") == 0)
				{
					/*Executing the suite executer script to invoke all Glib test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the Glib tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","glib",NULL);       
				}
				else if(strcmp(component_option,"openssl") == 0)
				{
					/*Executing the suite executer script to invoke all Openssl suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the Openssl tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","openssl",NULL);       
				}
				else if(strcmp(component_option,"libsoup") == 0)
				{
					/*Executing the suite executer script to invoke all Libsoup suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the Libsoup tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","libsoup",NULL);       
				}
				else if(strcmp(component_option,"jansson") == 0)
				{
					/*Executing the suite executer script to invoke all Jansson suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the Jansson tests");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","jansson",NULL);       
				}
				else if(strcmp(component_option,"qt5") == 0)
				{
					/*Executing the suite executer script to invoke all qt5 test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the qt5 tests suites");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","qt5",NULL);       
				}
				else if(strcmp(component_option,"qt5webkit") == 0)
				{
					/*Executing the suite executer script to invoke all qt5webkit test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the qt5webkit tests suites");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","qt5webkit",NULL);       
				}
				else if(strcmp(component_option,"yajl") == 0)
				{
					/*Executing the suite executer script to invoke all yajl test suites*/
					DEBUG_PRINT(DEBUG_TRACE,"\n Invoke SuiteExecuter script to execute the yajl tests suites");
					execlp(executerPath.c_str(),"SuiteExecuter.sh","-c","yajl",NULL);       
				}
				else 
				{
					DEBUG_PRINT(DEBUG_ERROR,"\n Not an Valid Test suite option");
					response["result"]="Not a valid test suite option for execution ";
				}
			}
			else if(idChild <0)
			{
				/* Filling the response back with error message in case of fork failure*/
				DEBUG_PRINT(DEBUG_ERROR,"\nfailed fork");
				response["result"]="Test Suite Execution failed";
			}
			else
			{
				/* Wait for the Suite execution to get over */  
				waitpid(idChild,&iTestAppStatus,0);

				/* Filling the response and log path of testsuite logs */
				if(strcmp(component_option,"openssl") == 0)
				{
					DEBUG_PRINT(DEBUG_LOG,"\n Filling the openssl Test apps response details \n");
					response["details"]= "See the individual log files for Execution status";
					response["result"]="Test Suite Executed";
				}
				else
				{
					/* Get the execution status */
					get_status = getstatus(testenvPath);
					DEBUG_PRINT(DEBUG_LOG,"\n Getting the Execution status : %s\n",get_status.c_str());
					if(get_status.empty() == 0)
					{
						response["details"]= get_status;
						response["result"]="Test Suite Executed";
					}
					else
					{
						response["result"]="Test Suite Execution Failed";
						response["details"]= "NO SUITE_STATUS file available to get the information about exectution status ";
					}
				}

				/* Get the Summary file path */
				logger_path = getsummarylogpath(testenvPath);
				DEBUG_PRINT(DEBUG_LOG,"\n Getting the Test Summary Log path \n");
				DEBUG_PRINT(DEBUG_LOG,"\n Test Summary Log path :%s\n",logger_path.c_str());
				if (logger_path.empty() == 0)
				{
					response["log-path"]=logger_path;
				}
				else
				{
					response["details"]= "NO LOGPATH_INFO file available to get the information about log path";
				} 
			}

		} 
		else
		{
			DEBUG_PRINT(DEBUG_ERROR,"\n Not able to read the environment path\n");
			response["details"]= "\n  Not able to read the environment path \n";
			response["result"]="Test Suite Execution Failed";
		}
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n OPENSOURCETEST_PATH export is not set. Kindly set the RDKTDK_PATH path\n");
		response["details"]= "\n OPENSOURCETEST_PATH export is not set. Kindly set the RDKTDK_PATH path\n";
		response["result"]="Test Suite Execution Failed";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nExiting OpensourceTestStub_Execute function");

	return true;
}
/******************************************************************************************************************************
 *Function name	: getsummarylogpath
 *Descrption	: This function will help in reading the LOGPATH_INFO file and give the details of the executed test suite log
 *       returns a string value
 *****************************************************************************************************************************/ 
string OpensourceTestStub:: getsummarylogpath(string envPath)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n Entering getsummarylogpath function \n");
	string logpathobj,logPath;
	printf ("%s",envPath.c_str());
	logPath.append(envPath);
	logPath.append("/");
	logPath.append(LOGGERFILE_NAME);

	ifstream input(logPath.c_str());
	if(input.is_open())
	{
		while(!input.eof())
		{
			DEBUG_PRINT(DEBUG_LOG,"\n Reading the status details from LOGPATH_INFO \n");
			getline(input,logpathobj);
			input.close();
			return logpathobj;
		}
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Not able to open LOGPATH_INFO file\n");
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n Exiting getsummarylogpath function \n");
	return NULL;
}

/******************************************************************************************************************************
 *Function name	: getstatus
 *Descrption	: This function will help in reading the SUITESTATUS file and give the details of the executed test suite log
 *       returns a string value
 *****************************************************************************************************************************/ 
string OpensourceTestStub:: getstatus(string envPath1)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n Entering getstatus function \n");

	string logstatusobj,statusPath;
	printf ("%s",envPath1.c_str());
	statusPath.append(envPath1);
	statusPath.append("/");
	statusPath.append(SUITESTATUSFILE_NAME);
	ifstream input(statusPath.c_str());
	if(input.is_open())
	{
		while(!input.eof())
		{
			DEBUG_PRINT(DEBUG_LOG,"\n Reading the status details from LOGPATH_INFO \n");
			getline(input,logstatusobj);
			input.close();
			return logstatusobj;
		}	
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Not able to open SUITE_STATUS file\n");
	}

	DEBUG_PRINT(DEBUG_TRACE,"\n Exiting getstatus function \n");
	return NULL;
}

/**************************************************************************
 * Function Name : CreateObject
 * Description   : this function will be used to create a new object
 *      for the class OpensourceTestStub
 **************************************************************************/
extern "C" OpensourceTestStub* CreateObject()
{
	DEBUG_PRINT(DEBUG_LOG,"\n Creating the Open source test stub object \n");
	return new OpensourceTestStub();
}

/**************************************************************************
 * Function Name : cleanup
 * Description   : This function will do the clean up.
 *
 **************************************************************************/
bool OpensourceTestStub::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_LOG,"\n OpensourceTestStub shutting down ");
	ptrAgentObj->UnregisterMethod("TestMgr_Opensource_Test_Execute");
	return true;
}

/**************************************************************************
 * Function Name : DestroyObject
 * Description   : This function will be used to destory the object. 
 *
 **************************************************************************/
extern "C" void DestroyObject(OpensourceTestStub *stubobj)
{
	DEBUG_PRINT(DEBUG_LOG,"\n Destroying Opensourcetest stub object");
	delete stubobj;


}

