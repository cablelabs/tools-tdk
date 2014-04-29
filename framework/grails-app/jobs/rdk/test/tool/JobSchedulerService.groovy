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
package rdk.test.tool

import java.text.DateFormat
import java.text.SimpleDateFormat
import java.util.regex.Matcher
import org.quartz.Job
import org.quartz.JobExecutionContext;
import com.comcast.rdk.*

import javax.servlet.http.HttpServletRequest;
import static com.comcast.rdk.Constants.*;
import java.util.regex.Pattern;
import org.codehaus.groovy.grails.commons.ConfigurationHolder
import rdk.test.tool.DeviceStatusJob

/**
 * Schedular class to schedule script execution for a future date
 * Quartz Schedula
 * @author sreejasuma
 *
 */
class JobSchedulerService implements Job{

    def grailsApplication
    boolean transactional = false
//	def executionService
	
    static triggers ={}
    
    /**
     * Method which is invoked based on the schedule time
     * @param context
     */
    public void execute (JobExecutionContext context) {
        def jobName = context.jobDetail.key.name
        def triggerName = context.trigger.key.name

        JobDetails jobDetails

        JobDetails.withTransaction {
            jobDetails = JobDetails.findByJobNameAndTriggerName(jobName,triggerName)
        }

        if(jobDetails){
            DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
            Calendar cal = Calendar.getInstance()
            String date = dateFormat.format(cal.getTime()).toString()
            String executionName = KEY_JOB+UNDERSCORE+jobDetails.device+UNDERSCORE+date
            startExecutions(executionName,jobDetails.id)
        }
    }
	
    /**
     * Method to execute the script
     * @param executionName
     * @param jobId
     * @return
     */
    def startExecutions(final String executionName, final def jobId){

        def filePath
        def scripts = null
        def scriptGrpId = null
		def devices = null
        def realpath
        def url
        JobDetails jobDetails
		ExecutionDevice executionDevice
		StringBuilder output = new StringBuilder();
        JobDetails.withTransaction{
            jobDetails = JobDetails.findById(jobId, [lock: true])
           // log.info jobDetails.script
            filePath = jobDetails?.filePath
            scripts = jobDetails?.script
            scriptGrpId = jobDetails?.scriptGroup
            realpath = jobDetails?.realPath
            url = jobDetails?.appUrl
			devices = jobDetails?.device
        }
		
        def scriptInstance
        def scriptGroupInstance
		def deviceName
        def deviceInstance //= Device.findById(jobDetails?.device, [lock: true])
        String htmlData = ""
       
            def scriptObject
            def scriptName

            DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT);
            Calendar cal = Calendar.getInstance();

			def deviceList = []
			
			if(devices instanceof String){
				deviceList << devices
				deviceInstance = Device.findById(devices, [lock: true])
				deviceName = deviceInstance?.stbName
			}
			else{
				(devices).each{ deviceid ->
					deviceList << deviceid
				}
				deviceName = MULTIPLE
			}
			
			def repeatCount = jobDetails?.repeatCount
			def deviceId
			def execName
			def executionNameForCheck
			for(int i = 0; i < repeatCount; i++ ){
				executionNameForCheck = null
				deviceList.each{ device ->
					deviceInstance = Device.findById(device)
					def executionSaveStatus = true
					def execution = null
					
					deviceId = deviceInstance?.id
					def scriptStatus = true
					def scriptId
					if(scripts){
						if(scripts.size() > 1){
							scriptName = MULTIPLESCRIPT
						}
						else{
							scriptInstance = Script.findById(scripts[0],[lock: true])
							scriptStatus = validateScriptBoxType(scriptInstance,deviceInstance)
							scriptName = scriptInstance?.name
						}
					}else if(scriptGrpId){
						scriptGroupInstance = ScriptGroup.findById(scriptGrpId,[lock: true])
					}

					if(scriptStatus){
						if(!executionNameForCheck){
							if(i > 0){
								execName = executionName + UNDERSCORE +i
							}
							else{
								execName = executionName
							}
							
							Execution.withTransaction { status ->
								try {
									execution = new Execution()
									execution.name = execName
									execution.script = scriptName
									execution.device = deviceName
									execution.scriptGroup = scriptGroupInstance?.name
									execution.result = UNDEFINED_STATUS
									execution.dateOfExecution = new Date()//dateFormat.format(cal.getTime())
									execution.groups = jobDetails?.groups
									if(! execution.save(flush:true)) {
										log.error "Error saving Execution instance : ${execution.errors}"
										executionSaveStatus = false
									}
									status.flush()
								}
								catch(Throwable th) {
									status.setRollbackOnly()
								}
							}

							if(deviceList.size() > 0 ){
								executionNameForCheck = execName
							}
						}
						else{
							execution = Execution.findByName(executionNameForCheck)
							execName = executionNameForCheck
						}
						if(executionSaveStatus){
							ExecutionDevice.withTransaction { status ->
							try{
								executionDevice = new ExecutionDevice()
								executionDevice.execution = Execution.findByName(execName)
								executionDevice.dateOfExecution = new Date()
								executionDevice.device = deviceInstance?.stbName
								executionDevice.deviceIp = deviceInstance?.stbIp
								executionDevice.status = UNDEFINED_STATUS
								executionDevice.save(flush:true)
								if(! executionDevice.save(flush:true)) {
									log.error "Error saving Execution instance : ${execution.errors}"
								}
								status.flush()
							}
							catch(Throwable th) {
									status.setRollbackOnly()
							}
							
							}
							executeVersionTransferScript(realpath, filePath, executionName, executionDevice?.id, deviceInstance.stbIp, deviceInstance?.logTransferPort)
							
							int scriptGrpSize = 0
							int scriptCounter = 0
							def isMultiple = "true"
							if(jobDetails?.scriptGroup){
								scriptGroupInstance = ScriptGroup.findById(jobDetails?.scriptGroup,[lock: true])
								scriptCounter = 0
								List<Script> validScriptList = new ArrayList<Script>()
								scriptGroupInstance.scripts.each { script ->
									if(validateScriptBoxType(script,deviceInstance)){
										validScriptList << script
									}
								}
								scriptGrpSize = validScriptList?.size()
								validScriptList.each{ scriptObj ->
									scriptCounter++
									if(scriptCounter == scriptGrpSize){
										isMultiple = "false"
									}
									htmlData = executeScript(execName, executionDevice, scriptObj , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,executionName,isMultiple)
									
								
									output.append(htmlData)
									Thread.sleep(6000)
								}
							}
							else if(scripts){
								if(scripts instanceof String){
									scriptInstance = Script.findById(scripts,[lock: true])
									scriptId = scriptInstance?.id
									isMultiple = "false"
									htmlData = executeScript(execName, executionDevice, scriptInstance , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,executionName,isMultiple)
									output.append(htmlData)
								}
								else{
									scriptCounter = 0
									List<Script> validScripts = new ArrayList<Script>()
									scripts.each { script ->
										scriptInstance = Script.findById(script,[lock: true])
										if(validateScriptBoxType(scriptInstance,deviceInstance)){
											validScripts << scriptInstance
										}
									}
									scriptGrpSize = validScripts?.size()
									validScripts.each{ script ->
										scriptCounter++
										if(scriptCounter == scriptGrpSize){
											isMultiple = "false"
										}
										
										htmlData = executeScript(execName, executionDevice, script , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics, executionName,isMultiple)
										
										output.append(htmlData)
										Thread.sleep(6000)
									}
								}
							}
						}
					}
					else{
						
						output.append(htmlData)
					}
					htmlData = ""
				}
				
				/**
				 * Re run on failure
				 */
				def executionObj = Execution.findByName(execName)
				def executionDeviceObj = ExecutionDevice.findAllByExecutionAndStatusNotEqual(executionObj, SUCCESS_STATUS)

				if((executionDeviceObj.size() > 0 ) && (jobDetails?.rerun)){
					htmlData = reRunOnFailure(realpath,filePath,url,execName,executionName,jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,jobDetails?.groups)
					output.append(htmlData)
				}
				
			}

   }


	
	def reRunOnFailure(final String realPath, final String filePath, String url, final String execName,final String uniqueExecutionName,
				final String isBenchMark, final String isSystemDiagnostics, final def groups){
		Thread.sleep(10000)
		Execution executionInstance = Execution.findByName(execName)
		def resultArray = Execution.executeQuery("select a.result from Execution a where a.name = :exName",[exName: execName])
		def result = resultArray[0]
		def newExecName
		def execution
		Execution rerunExecutionInstance
		def executionSaveStatus = true
		if(result != SUCCESS_STATUS){
			def scriptName
			def scriptGroupInstance = ScriptGroup.findByName(executionInstance?.scriptGroup)
			/**
			 * Get all devices for execution
			 */
			def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
			int cnt = 0
			executionDeviceList.each{ execDeviceInstance ->
				if(execDeviceInstance.status != SUCCESS_STATUS){
					Device deviceInstance = Device.findByStbName(execDeviceInstance?.device)
					if(cnt == 0){
						newExecName = execName + RERUN
						scriptName = executionInstance?.script
						def deviceName = deviceInstance?.stbName
						if(executionDeviceList.size() > 1){
							deviceName = MULTIPLE
						}
						
						Execution.withTransaction { status ->
							try {
								execution = new Execution()
								execution.name = newExecName
								execution.script = scriptName
								execution.device = deviceName
								execution.scriptGroup = scriptGroupInstance?.name
								execution.result = UNDEFINED_STATUS
								execution.dateOfExecution = new Date()//dateFormat.format(cal.getTime())
								execution.groups = groups
								if(! execution.save(flush:true)) {
									log.error "Error saving Execution instance : ${execution.errors}"
									executionSaveStatus = false
								}
								status.flush()
							}
							catch(Throwable th) {
								status.setRollbackOnly()
							}
						}
						
						cnt++
						rerunExecutionInstance = Execution.findByName(newExecName)
					}
					if(executionSaveStatus){
						ExecutionDevice executionDevice
						Execution.withTransaction {
							executionDevice = new ExecutionDevice()
							executionDevice.execution = rerunExecutionInstance
							executionDevice.device = deviceInstance?.stbName
							executionDevice.deviceIp = deviceInstance?.stbIp
							executionDevice.dateOfExecution = new Date()
							executionDevice.status = UNDEFINED_STATUS
							executionDevice.save(flush:true)
						}
						executeVersionTransferScript(realPath, filePath, newExecName, executionDevice?.id, deviceInstance.stbIp, deviceInstance?.logTransferPort)
						def executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(executionInstance,execDeviceInstance,SUCCESS_STATUS)
						def scriptInstance
						def htmlData
						
						def resultSize = executionResultList.size()
						int counter = 0
						def isMultiple = "true"
						executionResultList.each{ executionResult ->
							scriptInstance = Script.findByName(executionResult?.script,[lock: true])
							
							if(counter == resultSize){
								isMultiple = "false"
							}
							
							if(validateScriptBoxType(scriptInstance,deviceInstance)){
								htmlData = executeScript(newExecName, executionDevice, scriptInstance, deviceInstance, url, filePath, realPath,isBenchMark,isSystemDiagnostics,uniqueExecutionName,isMultiple)
							}
							counter++
						}
					}
						
				}
			}
		}
	}
	
	
	def executeVersionTransferScript(final String realPath, final String filePath, final String executionName, def exectionDeviceId, final String stbIp, final String logTransferPort){
		try{
			def executionInstance = Execution.findByName(executionName)
			String fileContents = new File(filePath+DOUBLE_FWD_SLASH+VERSIONTRANSFER_FILE).text
			
			fileContents = fileContents.replace(IP_ADDRESS, STRING_QUOTES+stbIp+STRING_QUOTES)
			
			fileContents = fileContents.replace(PORT, logTransferPort)
			
			String versionFilePath = "${realPath}//logs//version//${executionInstance?.id}//${exectionDeviceId?.toString()}//${exectionDeviceId?.toString()}_version.txt"
			fileContents = fileContents.replace(LOCALFILE, STRING_QUOTES+versionFilePath+STRING_QUOTES)
			
			String versionFile = TEMP_VERSIONFILE_NAME
			new File("${realPath}//logs//version//${executionInstance?.id}//${exectionDeviceId?.toString()}").mkdirs()
			File versnFile = new File(filePath, versionFile)
			boolean isVersionFileCreated = versnFile.createNewFile()
			if(isVersionFileCreated) {
				versnFile.setExecutable(true, false )
			}
			PrintWriter versnNewPrintWriter = versnFile.newPrintWriter()
			versnNewPrintWriter.print( fileContents )
			versnNewPrintWriter.flush()
			versnNewPrintWriter.close()
			executeScript( versnFile.getPath() )
			versnFile.delete()
		}
		catch(Exception ex){
			
		}
	}

	/**
	 * Method to execute the script
	 * @param scriptGroupInstance
	 * @param scriptInstance
	 * @param deviceInstance
	 * @param url
	 * @return
	 */

	def String executeScript(final String executionName, final ExecutionDevice executionDevice, final Script scriptInstance,
			final Device deviceInstance, final String url, final String filePath, final String realPath, final String isBenchMark, final String isSystemDiagnostics,final String uniqueExecutionName,final String isMultiple) {

		String htmlData = ""

		String scriptData = convertScriptFromHTMLToPython(scriptInstance.scriptContent)

		String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES

		Script scriptInstance1 = Script.findById(scriptInstance.id,[lock: true])
		scriptInstance1.status = Status.ALLOCATED
		scriptInstance1.save(flush:true)

		Device deviceInstance1 = Device.findById(deviceInstance.id,[lock: true])
	 
		def executionInstance = Execution.findByName(executionName,[lock: true])
		def executionId = executionInstance?.id
		Date executionDate = executionInstance?.dateOfExecution
		
		def execStartTime = executionDate?.getTime()
		
		def executionResult
		
		ExecutionResult.withTransaction { resultstatus ->
			try {
				executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance1.name
				executionResult.device = deviceInstance1.stbName
				if(! executionResult.save(flush:true)) {
					log.error "Error saving executionResult instance : ${executionResult.errors}"
				}
				resultstatus.flush()
			}
			catch(Throwable th) {
				resultstatus.setRollbackOnly()
			}
		}
		def executionResultId = executionResult?.id
		scriptData = scriptData.replace( IP_ADDRESS , stbIp )
		scriptData = scriptData.replace( PORT , deviceInstance?.stbPort )

		String gatewayIp = deviceInstance1?.gatewayIp
		
		scriptData = scriptData.replace( REPLACE_TOKEN, LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath +SINGLE_QUOTES + COMMA_SEPERATOR +
			  executionId  + COMMA_SEPERATOR + executionDevice?.id + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.logTransferPort + COMMA_SEPERATOR + deviceInstance1?.statusPort + COMMA_SEPERATOR +
			  scriptInstance?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR + SINGLE_QUOTES + isBenchMark + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + isSystemDiagnostics + SINGLE_QUOTES + COMMA_SEPERATOR +
			  SINGLE_QUOTES + isMultiple + SINGLE_QUOTES + COMMA_SEPERATOR)// + gatewayIp + COMMA_SEPERATOR)
		
		scriptData	 = scriptData + "\nprint \"SCRIPTEND#!@~\";"
		
		Date date = new Date()
		String newFile = FILE_STARTS_WITH+date.getTime().toString()+PYTHON_EXTENSION
		
		File file = new File(filePath, newFile)
		boolean isFileCreated = file.createNewFile()
		if(isFileCreated) {
			file.setExecutable(true, false )
		}
		PrintWriter fileNewPrintWriter = file.newPrintWriter();
		fileNewPrintWriter.print( scriptData )
		fileNewPrintWriter.flush()
		fileNewPrintWriter.close()
		String outData = executeScripts( file.getPath() , scriptInstance.executionTime)
				
		file.delete()
		outData?.eachLine { line ->
			htmlData += (line + HTML_BR )
		}
		Date execEndDate = new Date()
		def execEndTime =  execEndDate.getTime()
		def timeDifference = ( execEndTime - execStartTime  ) / 60000;
		String timeDiff =  String.valueOf(timeDifference)
		if(htmlData.contains(TDK_ERROR)){
			htmlData = htmlData.replaceAll(TDK_ERROR,"")
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
			}
			updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff)
			Thread.sleep(4000)
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				"false"
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd)
			Thread.sleep(4000)
		}
		else{
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
				String outputData = htmlData
				updateExecutionResults(outputData,executionResultId,executionId,executionDevice?.id,timeDiff)
			}
			else{
				if((timeDifference >= scriptInstance.executionTime) && (scriptInstance.executionTime != 0))	{
					File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
					def absolutePath = layoutFolder.absolutePath
						String[] cmd = [
							PYTHON_COMMAND,
							absolutePath,
							deviceInstance?.stbIp,
							deviceInstance?.agentMonitorPort,
							"true"
						]
						ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
						def resetExecutionData = scriptExecutor.executeScript(cmd)
						htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
						updateExecutionResults(htmlData,executionResultId,executionId,executionDevice?.id)
						Thread.sleep(4000)
				}
			}
		}
				
		String performanceFilePath
		if(isBenchMark.equals("true") || isSystemDiagnostics.equals("true")){
			new File("${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
			performanceFilePath = "${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}//"
		}
			
		if(isBenchMark.equals("true")){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath
			
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				deviceInstance?.logTransferPort,
				"PerformanceBenchMarking",
				performanceFilePath
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
			htmlData += scriptExecutor.executeScript(cmd)
		}
		if(isSystemDiagnostics.equals("true")){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				deviceInstance?.logTransferPort,
				"PerformanceSystemDiagnostics",
				performanceFilePath
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
			htmlData += scriptExecutor.executeScript(cmd)
		}
		return htmlData
	}
	
	
			/**
			 * Method to call the script executor to execute the script
			 * @param executionData
			 * @return
			 */
			public String executeScripts(final String executionData, int execTime) {
				
				def output = new ScriptExecutor().execute( getCommand( executionData ), execTime)
				return output
			}
	
	
 
    /**
     * Method to execute the script
     * @param scriptGroupInstance
     * @param scriptInstance
     * @param deviceInstance
     * @param url
     * @return
     */
/*    def String executeScript(final String executionName,final def scriptGroupInstance, final Script scriptInstance,
            final Device deviceInstance, final String url, final String filePath, final String realPath ) {

        String htmlData = ""

        String scriptData = convertScriptFromHTMLToPython(scriptInstance.scriptContent)

        String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES

        Script scriptInstance1
        Script.withTransaction {
            scriptInstance1 = Script.findById(scriptInstance.id,[lock: true])
            scriptInstance1.status = Status.ALLOCATED
            scriptInstance1.save(flush:true)
        }


        Device deviceInstance1
        Device.withTransaction {
            deviceInstance1 = Device.findById(deviceInstance.id,[lock: true])
            deviceInstance1.deviceStatus = Status.ALLOCATED
            deviceInstance1.save(flush:true)
        }


        def executionInstance = Execution.findByName(executionName,[lock: true])
        def executionId = executionInstance?.id
        Date executionDate = executionInstance?.dateOfExecution

        def execStartTime = executionDate?.getTime()

        def executionResult
        ExecutionResult.withTransaction { resultstatus ->
            try {
                executionResult = new ExecutionResult()
                executionResult.execution = executionInstance
                executionResult.script = scriptInstance1.name
                executionResult.device = deviceInstance1.stbName
                if(! executionResult.save(flush:true)) {
                    log.error "Error saving executionResult instance : ${executionResult.errors}"
                }
                resultstatus.flush()
            }
            catch(Throwable th) {
                resultstatus.setRollbackOnly()
            }
        }
        def executionResultId = executionResult?.id
        scriptData = scriptData.replace( IP_ADDRESS , stbIp )
        scriptData = scriptData.replace( PORT , deviceInstance?.stbPort )
        scriptData = scriptData.replace( REPLACE_TOKEN, LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath +SINGLE_QUOTES + COMMA_SEPERATOR +
                executionId  + COMMA_SEPERATOR + executionResultId + REPLACE_BY_TOKEN + deviceInstance?.logTransferPort + COMMA_SEPERATOR )

        Date date = new Date()
        String newFile = FILE_STARTS_WITH+date.getTime().toString()+PYTHON_EXTENSION


        File file = new File(filePath, newFile)
        boolean isFileCreated = file.createNewFile()
        if(isFileCreated) {
            file.setExecutable(true, false )
        }
        PrintWriter fileNewPrintWriter = file.newPrintWriter();
        fileNewPrintWriter.print( scriptData )
        fileNewPrintWriter.flush()

        String outData = executeScriptData( file.getPath() )

        outData?.eachLine { line ->
            htmlData += (line + HTML_BR )
        }

        file.delete()
		String outputData = htmlData
		Date execEndDate = new Date()
		def execEndTime =  execEndDate.getTime()
		def timeDifference = ( execEndTime - execStartTime  ) / 60000;
		String timeDiff =  String.valueOf(timeDifference)

		if(outputData) {
			executionResult = ExecutionResult.findById(executionResultId)
			ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput  where c.id = :execId",
					[newOutput: outputData, execId: executionResultId])
			Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime where c.id = :execId",
					[newStatus: outputData, newTime: timeDiff, execId: executionId.toLong()])

		}

		return htmlData
    }*/


    /**
     * Execute the script
     * @param executionData
     * @return
     */
    public String executeScriptData(final String executionData) {
        new ScriptExecutor().execute( getCommand( executionData ))
    }


    /**
     * Method to get the python script execution command.
     * @param command
     * @return
     */
    public String getCommand(String command) {
        String actualCommand = ConfigurationHolder.config.python.execution.path +" "+ command
        return actualCommand
    }

    /**
     * Converts the script that is given in textarea to
     * python format
     * @param script
     * @return
     */
    def convertScriptFromHTMLToPython(final String script){
        def afterspan =removeAllSpan(script)
        def afterBr = afterspan.replaceAll(HTML_REPLACEBR, KEY_ENTERNEW_LINE);
        afterBr = afterBr.replaceAll(HTML_LESSTHAN,LESSTHAN);
        afterBr = afterBr.replaceAll(HTML_GREATERTHAN, GREATERTHAN);
        return afterBr;
    }
    
    /**
     * Removes all span from the script 
     * @param script
     * @return
     */
    def removeAllSpan(String script) {
        Matcher m = Pattern.compile(HTML_PATTERN).matcher(script);
        while(m.find()){
            String match = m.group(1);
            script =script.replace(match, "");
        }
        String afterspan =script.replaceAll(HTML_PATTERN_AFTERSPAN, "");
        return afterspan
    }
	
	public boolean validateScriptBoxType(final Script scriptInstance, final Device deviceInstance){
		boolean scriptStatus = true
		if(!(scriptInstance.boxTypes.find { it.id == deviceInstance.boxType.id })){
			scriptStatus = false
		}
		return scriptStatus
	}

	public void updateExecutionResults(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId, final String timeDiff){
		
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput  where c.id = :execId",
				[newOutput: outputData, execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime where c.id = :execId",
				[newStatus: outputData, newTime: timeDiff, execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.executionTime = :newTime where c.id = :execDevId",
				[newTime: timeDiff, execDevId: executionDeviceId.toLong()])
	}
	
	/**
	 * Method to update the execution report for each test script execution.
	 * This method will update the ExecutionResult and Execution tables with new execution output.
	 *
	 * @param outputData
	 * @param executionResultId
	 * @param executionId
	 * @param timeDiff
	 */
	public void updateExecutionResults(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId){
		
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput , c.status = :newStatus  where c.id = :execId",
				[newOutput: outputData, newStatus: "SCRIPT TIME OUT", execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.result = :newStatus where c.id = :execId",
				[newStatus: outputData, newStatus: "FAILURE", execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat where c.id = :execDevId",
				[newStat: "FAILURE", execDevId: executionDeviceId.toLong()])
		
	}
	
	/**
	 * Method to update the execution report for each test script execution.
	 * This method will update the ExecutionResult and Execution tables with new execution output.
	 *
	 * @param outputData
	 * @param executionResultId
	 * @param executionId
	 * @param timeDiff
	 */
	public void updateExecutionResultsError(final String resultData,final long executionResultId, final long executionId, final long executionDeviceId,final String timeDiff){

		
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput , c.status = :newStatus  where c.id = :execId",
				[newOutput: resultData, newStatus: "FAILURE", execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime, c.result = :newStatus where c.id = :execId",
				[newStatus: resultData, newTime: timeDiff, newStatus: "FAILURE", execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat where c.id = :execDevId",
				[newStat: "FAILURE", execDevId: executionDeviceId.toLong()])
		
	}
}

