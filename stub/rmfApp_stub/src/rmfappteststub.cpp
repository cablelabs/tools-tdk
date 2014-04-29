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

#include "rmfAppteststub.h"


/**************************************************************************
* Function name: rmfAppTestStub::rmfAppTestStub()
* Descrption: Constructor for rmfAppTestStub class. Initializes the class 
* variables and configures it to ignore SIGPIPE signal.
* 
* @param [in]: none
* @param [out]: none
***************************************************************************/	
rmfAppTestStub::rmfAppTestStub ()
{
	/* Ignore any sigpipe errors while this test is running. This could be caused by the child
	application crashing or prematurely exiting. This condition can be detected by the EPIPE
	error thrown when the parent attempts to write to the pipe. Not ignoring this signal will
	cause the stub to quit upon receiving the signal. */
	old_signal_handler = signal (SIGPIPE, SIG_IGN);
	tunnel[PIPE_READ_END] = 0; tunnel[PIPE_WRITE_END]= 0;
	child_pid = 0; 
	DEBUG_PRINT(DEBUG_LOG, "Creating new stub object.\n");
}

/**************************************************************************
* Function name: initialize ()
* Descrption: Registers the RPC methods of the stub with the server and forks
* the actual rmfApp application. Sets up a 'pipe' to communicate with the child
* application. Anything the parent (stub) writes to the pipe appears on the STDIN
* of the child application.
*
* @param [in]: ptrAgentObj has a reference to the agent object whose RPC server
*	shall be used.
* @param [out]: none.
* 
* return value: true or false depending on the success of operation.
***************************************************************************/	
bool rmfAppTestStub::initialize (IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	int log_fd = 0;
	DEBUG_PRINT(DEBUG_LOG, "rmfAppTestStub Initialize");
	
	/*Register stub function for callback*/
	if (true != 
		ptrAgentObj->RegisterMethod (*this,&rmfAppTestStub::rmfAppTestStub_Execute, RMFAPP_RPC_COMMAND_STRING))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error! Registration of RPC method %s failed.\n", RMFAPP_RPC_COMMAND_STRING);
		return false;
	}
	
	/* Set up the pipe for IPC*/
	if (pipe (tunnel))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error! Unable to create pipe!\n");
		return false;
	}
	
	/* Attempt to fork and check for errors */
	DEBUG_PRINT(DEBUG_LOG, "Launching child application. Please check %s for logs.\n", RMFAPP_LOG_FILE);
	child_pid = fork ();
	if (0 > child_pid)
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error! Unable to fork child process.\n");
		return false;        
	}

	if (child_pid)
	{
		/* This is the parent process */
		DEBUG_PRINT(DEBUG_TRACE, "The child process was created with PID %d \n.", child_pid);		
		/* Close unused side of pipe ("read" end) */
		close (tunnel[PIPE_READ_END]);		
		
		/* Wait for the launched rmfApp application to perform initializations and drop to 
		prompt*/
		sleep (RMFAPP_TIME_TO_READY);

	}
	else
	{	/* This is the child process */
		/* Replace stdin with the "read" end of the pipe */
		dup2 (tunnel[PIPE_READ_END],STDIN_FILENO);
		/* Close unused side of pipe (write end) */
		close (tunnel[PIPE_WRITE_END]);
		
		/* Open log file to use for output redirection. */
		log_fd = open (RMFAPP_LOG_FILE, O_WRONLY | O_CREAT | O_APPEND, S_IRUSR | S_IWUSR);
		if (-1 != log_fd)
		{
				/* stdout may now be redirected to a file */
				dup2 (log_fd, STDOUT_FILENO);		
				//Redirect error logs (stderr) as well.
				dup2 (log_fd, STDERR_FILENO);
				close (log_fd);
		}
		else
		{
			DEBUG_PRINT(DEBUG_ERROR, "Warning! Unable to open log file. Won't redirect stdout of %s.\n", RMFAPP_EXEC);
		}
		/* Change directory to the actual location of rmfApp. It doesn't like it when called
		from elsewhere. */
		if (chdir (RMFAPP_DIR))
		{
			DEBUG_PRINT(DEBUG_ERROR, "Unable to switch to %s to run child application!\n",
				RMFAPP_DIR);
			exit(-1);
		}
		
		/* Replace the child process with the actual rmfApp process */
		if (-1 == execl (RMFAPP_EXEC, RMFAPP_EXEC, NULL))
		{
			DEBUG_PRINT(DEBUG_ERROR, "Error! execl failed! Are you sure the application %s is present?\n", RMFAPP_EXEC);
			exit (-1);
		}
	}
	return true;
}




/**************************************************************************
* Function name: rmfAppTestStub_Execute ()
* Descrption: Sends the command received from the framework to the rmfApp child
* application.
* 
* @param [in]: command string 
* @param [out]: result of the operation.
* @param [out]: details of any errors encountered. 
* @param [out]: path of log file.
*
* return value: true or false depending on the success of operation. This does
* not indicate the success or failure of the command executed in rmfApp, but 
* merely that the command has been sent to the application. Result of the actual 
* application has to be deduced from the logs.
***************************************************************************/	
bool rmfAppTestStub::rmfAppTestStub_Execute (IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "Entering rmfApp TestStub_Execute\n");
	char *rmfapp_command = (char*)req["rmfapp_command"].asCString ();

	switch (sendCommand (rmfapp_command))
	{
	case COMMAND_SENT:
		response["result"]="Test Suite Executed";
		break;
		
	case CHILD_APP_EXITED:
		response["details"]="The application(rmfApp) under test has exited prematurely or crashed!";
		response["result"]="FAILURE";
		break;
		
	default:
		/* Unknown error. Mark this test as a failure */
		response["result"]="FAILURE";
		response["details"]="Unable to communicate with rmfApp.";
	}

	string logger_path;
	
	/* Filling the response and log path of testsuite logs */	
	logger_path = RMFAPP_LOG_FILE;
	response["log-path"]=logger_path;	
	return true;
}


/**************************************************************************
* Function name: CreateObject ()
* Descrption: Handle provided to C libraries to create an object of this class.
* 
* @param [in]: none
* @param [out]: none
*
* return value: pointer to the newly created object.
***************************************************************************/	
extern "C" rmfAppTestStub* CreateObject ()
{
	return new rmfAppTestStub ();
}


/**************************************************************************
* Function name: cleanup ()
* Descrption: Unregisters the RPC methods of the stub, sends "quit" command to
* the child application and waits for it to exit. Also reinstates the original 
* SIGPIPE handler. This function can get blocked (hang) if the child application
*  doesn't quit.
* 
* @param [in]: reference to the agent object to unregister RPC methods from.
* @param [out]: none
* 
* return value: always returns true.
 ***************************************************************************/	
bool rmfAppTestStub::cleanup (IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	int returnval;
	DEBUG_PRINT(DEBUG_LOG, "rmfAppTestStub shutting down\n");
	
	/* Unregister RPC methods. */
	if (true != ptrAgentObj->UnregisterMethod (RMFAPP_RPC_COMMAND_STRING))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Warning! Unable to unregister method %s "\
			"from RPC server.\n", RMFAPP_RPC_COMMAND_STRING);
	}
	
	/* Kill the process running in a child process */	
	if (COMMAND_SENT != sendCommand (RMFAPP_KILL_COMMAND))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error while trying to quit. Unable to communicate with child.\n");	
	}

	/* Send shut-down command to rmfApp */
	if (COMMAND_SENT != sendCommand (RMFAPP_QUIT_COMMAND))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error while trying to quit. Unable to communicate with child.\n");	
	}

	/* Wait for child process to end */
	DEBUG_PRINT(DEBUG_LOG, "waitpid () indicates a %s exit.\n", 
		(child_pid == waitpid (child_pid, &returnval, 0)? \
		"CLEAN" : "PREMATURE/PENDING"));	
	
	/* Close the pipe to the child process */
	close (tunnel[PIPE_WRITE_END]);

	/* Restore the original signal handler. */
	signal (SIGPIPE, old_signal_handler);

	DEBUG_PRINT(DEBUG_LOG, "Done. %s exited with a value 0x%x\n", RMFAPP_EXEC, returnval);
	return true;
}	

/**************************************************************************
* Function name: sendCommand ()
* Descrption: Actual function that sends the command to child application 
* through the pipe. It also appends "\n" to the string to terminate the 
* command.
* 
* @param [in]: command string.
* @param [out]: none
*
* return value: COMMAND_SENT - Success.
				CHILD_APP_EXITED - Child app is no longer running.
				COMMUNICATION_FAILURE - Failed to send command to child app.
***************************************************************************/	
sendCommandResult rmfAppTestStub::sendCommand (const char * command)
{
	char command_buffer[RMFAPP_MAX_COMMAND_LENGTH];
	
	if (RMFAPP_MAX_COMMAND_LENGTH < (strlen (command) + 2)) /* Size of command + "/n" + "/0" */
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error! Command is too big for the buffer.\n");
		return COMMUNICATION_FAILURE;
	}
	
	/* Copy command to internal buffer and append terminator. */
	strncpy (command_buffer, command, RMFAPP_MAX_COMMAND_LENGTH);
	command_buffer[strlen (command)] = '\n';
	
	/* Write to pipe. */
	DEBUG_PRINT(DEBUG_TRACE, "Sending command %s to fd %d.\n", command_buffer, tunnel[PIPE_WRITE_END]);
	if (0 >= write (tunnel[PIPE_WRITE_END], command_buffer, strlen (command_buffer)))
	{
		/* There was an error. A crashed rmfApp could be one of the reasons*/
		perror ("Error");
		if (errno == EPIPE)
		{
			DEBUG_PRINT(DEBUG_ERROR, "The application %s appears to have exited/crashed prematurely.\n", RMFAPP_EXEC);
			DEBUG_PRINT(DEBUG_ERROR, "Unable to send command %s.\n", command_buffer);
			return CHILD_APP_EXITED;
		}
		else
		{
			DEBUG_PRINT(DEBUG_ERROR, "Communication with rmfApp failed. errno is %d.\n", errno);
			DEBUG_PRINT(DEBUG_ERROR, "Unable to send command %s.\n", command_buffer);
			return COMMUNICATION_FAILURE;
		}
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG, "Command issued: %s.\n", command_buffer);
		return COMMAND_SENT;
	}
}

/**************************************************************************
* Function name: DestroyObject ()
* Descrption: Handle to destroy the stub object from a C library.
* 
* @param [in]: reference to the stub object created.
* @param [out]: none
*
* return value: none
***************************************************************************/	
extern "C" void DestroyObject (rmfAppTestStub *stubobj)
{
	DEBUG_PRINT(DEBUG_LOG, "Destroying rmfAppTest stub object\n");
	delete stubobj;

}


// End of file rmfappteststub.cpp.
