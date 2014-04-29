/*
* ============================================================================
* COMCAST CONFIDENTIAL AND PROPRIETARY
* ============================================================================
* This file and its contents are the intellectual property of Comcast.  It may
* not be used, copied, distributed or otherwise  disclosed in whole or in part
* without the express written permission of Comcast.
* ============================================================================
* Copyright (c) 2013 Comcast. All rights reserved.
* ============================================================================
*/
 
#ifndef __rmfAppTEST_STUB_H__
#define __rmfAppTEST_STUB_H__

#include <iostream>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/stat.h>   
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>

#include <json/json.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

using namespace std;

#define IN
#define OUT

typedef void (*sighandler_t)(int);

//Return value or result of sendCommand () operation.
typedef enum
{
	COMMAND_SENT = 0, //Success.
	COMMUNICATION_FAILURE, //Unknown error.
	CHILD_APP_EXITED //Error.
} sendCommandResult;

#define RMFAPP_EXEC "rmfApp" //name of child executable.
#define RMFAPP_DIR "/mnt/nfs/env"//Location of rmfApp
#define RMFAPP_LOG_FILE "/opt/logs/rmfapp.log" //Path of log file
#define RMFAPP_KILL_COMMAND "kill 1" //Command that causes the child to kill the process it is running.
#define RMFAPP_QUIT_COMMAND "quit" //Command that causes the child to exit.
#define RMFAPP_COMMAND_TERMINATOR "\n" //To be appended to every command.
#define RMFAPP_TIME_TO_READY 3 //Time taken for the child application to drop to CLI prompt.
#define PIPE_READ_END 0
#define PIPE_WRITE_END 1
#define RMFAPP_MAX_COMMAND_LENGTH 400 //Maximum length of commands sent to child application.
#define RMFAPP_RPC_COMMAND_STRING "TestMgr_rmfapp_Test_Execute" //Name of RPC method registered with the agent.

	

class rmfAppTestStub : public RDKTestStubInterface
{	
	public:
	
        rmfAppTestStub ();
        bool initialize (IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);
        bool cleanup (IN const char* szVersion,IN RDKTestAgent	*ptrAgentObj);
     	bool rmfAppTestStub_Execute (IN const Json::Value& req, OUT Json::Value& response);
		
	private:
	
	sighandler_t old_signal_handler; //Holds the original signal handler to be reinstated at the end of test.
	int child_pid; //Pid of the child that is spawned.
	int	tunnel[2]; //This is the pipe that communicates between stub and rmfApp
	
	sendCommandResult sendCommand (const char * command);
};

#endif //__rmfAppTEST_STUB_H_

// End of file rmfAppteststub.h
