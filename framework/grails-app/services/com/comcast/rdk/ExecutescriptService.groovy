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
package com.comcast.rdk

import static com.comcast.rdk.Constants.*
import groovy.sql.Sql

import java.util.List
import java.util.concurrent.Callable
import java.util.concurrent.ExecutorService
import java.util.concurrent.Future
import java.util.concurrent.Executors


/**
 * 
 * Service class of ExecutionController
 *
 */

class ExecutescriptService {
	/**
	 * Injecting executor service.
	 */
	static ExecutorService executorService = Executors.newCachedThreadPool()

	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication

	/**
	 * Injects the executionService.
	 */
	def executionService
	
	def scriptService

	/**
	 * Injects the deviceStatusService.
	 */
	def deviceStatusService

	/**
	 * Injects the scriptexecutionService.
	 */
	def scriptexecutionService

	/**
	 * Injects dataSource.
	 */
	def dataSource
	
	/**
	 * Sets the transactional to false as it is causing many issues
	 * in database operations that invokes from different threads.
	 */
	static transactional = false

	/**
	 * Method to execute the script
	 * @param scriptGroupInstance
	 * @param scriptInstance
	 * @param deviceInstance
	 * @param url
	 * @return
	 */
	
	def String executeScript(final String executionName, final ExecutionDevice executionDevice, final def scriptInstance,
			final Device deviceInstance, final String url, final String filePath, final String realPath, final String isBenchMark, final String isSystemDiagnostics,final String uniqueExecutionName,final String isMultiple, def executionResult) {
		String htmlData = ""
		String scriptData = executionService.convertScriptFromHTMLToPython(scriptInstance.scriptContent)
		String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES
		def executionInstance = Execution.findByName(executionName)
		def executionId = executionInstance?.id
		Date executionDate = executionInstance?.dateOfExecution
		def resultArray = Execution.executeQuery("select a.executionTime from Execution a where a.name = :exName",[exName: executionName])
				
		def executionResultId
		if(executionResult == null){			
		    try {
			   def sql = new Sql(dataSource)
			   sql.execute("insert into execution_result(version,execution_id,execution_device_id,script,device,date_of_execution,status) values(?,?,?,?,?,?,?)", [1,executionInstance?.id, executionDevice?.id, scriptInstance.name, deviceInstance.stbName, new Date(), UNDEFINED_STATUS])
			} catch (Exception e) {
				e.printStackTrace()
			}

			def resultArray1 = ExecutionResult.executeQuery("select a.id from ExecutionResult a where a.execution = :exId and a.script = :scriptname and device = :devName ",[exId: executionInstance, scriptname: scriptInstance.name, devName: deviceInstance?.stbName.toString()])
			if(resultArray1[0]){
				executionResultId = resultArray1[0]
			}
		}else{
			executionResultId = executionResult?.id
		}
		def mocaDeviceList = Device.findAllByStbIpAndMacIdIsNotNull(deviceInstance?.stbIp)
		
		int counter = 1
		def mocaString = CURLY_BRACKET_OPEN
		
		int mocaListSize = mocaDeviceList?.size()
		mocaDeviceList.each{ mocaDevice ->
			
			mocaString = mocaString + counter.toString() + COLON + SQUARE_BRACKET_OPEN + STRING_QUOTES + mocaDevice?.macId + STRING_QUOTES +
			COMMA_SEPERATOR + mocaDevice?.stbPort + SQUARE_BRACKET_CLOSE
			
			if(mocaListSize != counter){
				mocaString = mocaString + COMMA_SEPERATOR
			}
			counter++
		}
		mocaString = mocaString + CURLY_BRACKET_CLOSE
		
		scriptData = scriptData.replace( IP_ADDRESS , stbIp )
		scriptData = scriptData.replace( PORT , deviceInstance?.stbPort )		
		scriptData = scriptData.replace( CLIENTLIST , mocaString )
		
		String gatewayIp = deviceInstance?.gatewayIp
		
		def sFile = ScriptFile.findByScriptNameAndModuleName(scriptInstance?.name,scriptInstance?.primitiveTest?.module?.name)

		scriptData = scriptData.replace( REPLACE_TOKEN, METHOD_TOKEN + LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath +SINGLE_QUOTES + COMMA_SEPERATOR +
				executionId  + COMMA_SEPERATOR + executionDevice?.id + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.logTransferPort + COMMA_SEPERATOR + deviceInstance?.statusPort + COMMA_SEPERATOR +
				sFile?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR + SINGLE_QUOTES + isBenchMark + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + isSystemDiagnostics + SINGLE_QUOTES + COMMA_SEPERATOR +
				SINGLE_QUOTES + isMultiple + SINGLE_QUOTES + COMMA_SEPERATOR)

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
		
		Date executionStartDt = new Date()
		def executionStartTime =  executionStartDt.getTime()
		
		int execTime = 0
		try {
			if(scriptInstance?.executionTime instanceof String){
				execTime = Integer.parseInt(scriptInstance?.executionTime)
			}else if(scriptInstance?.executionTime instanceof Integer){
				execTime = scriptInstance?.executionTime?.intValue()
			}else {
				execTime = scriptInstance?.executionTime
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		
		
		String outData = executionService.executeScript( file.getPath() , execTime, uniqueExecutionName , scriptInstance.name)
		file.delete()
		outData?.eachLine { line ->
			htmlData += (line + HTML_BR )
		}
		Date execEndDate = new Date()
		def execEndTime =  execEndDate.getTime()
		def timeDifference = ( execEndTime - executionStartTime  ) / 60000;

		String timeDiff =  String.valueOf(timeDifference)
		String singleScriptExecTime = String.valueOf(timeDifference)
		
		BigDecimal myVal1
		if(resultArray[0]){
			myVal1= new BigDecimal (resultArray[0]) + new BigDecimal (timeDiff)
		}
		else{
			myVal1 =  new BigDecimal (timeDiff)
		}
						
		timeDiff =  String.valueOf(myVal1)

		if(htmlData.contains(TDK_ERROR)){
			htmlData = htmlData.replaceAll(TDK_ERROR,"")
			if(htmlData.contains(KEY_SCRIPTEND)){
				htmlData = htmlData.replaceAll(KEY_SCRIPTEND,"")
			}
			executionService.updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
			Thread.sleep(4000)
			hardResetAgent(deviceInstance)
		}
		else{
			if(htmlData.contains(KEY_SCRIPTEND)){
				htmlData = htmlData.replaceAll(KEY_SCRIPTEND,"")
//				if(!checkExecutionCompletionStatus(executionResultId)){
//					executionService.updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
//				}else{
					String outputData = htmlData
					executionService.updateExecutionResults(outputData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
//				}
			}
			else{
				
				
				if((timeDifference >= execTime) && (execTime != 0))	{
					
					File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
					def absolutePath = layoutFolder.absolutePath
					String[] cmd = [
						PYTHON_COMMAND,
						absolutePath,
						deviceInstance?.stbIp,
						deviceInstance?.agentMonitorPort,
						TRUE
					]
					ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
					def resetExecutionData = ""
					
					try {
						resetExecutionData = scriptExecutor.executeScript(cmd,1)
					} catch (Exception e) {
						e.printStackTrace()
					}
					executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
					htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
					executionService.updateExecutionResultsTimeOut(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
					Thread.sleep(10000)
				}else{
					executionService.updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
					Thread.sleep(4000)
					resetAgent(deviceInstance)
				}
			}
		}
		String performanceFilePath
		if(isBenchMark.equals(TRUE) || isSystemDiagnostics.equals(TRUE)){
			new File("${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
			performanceFilePath = "${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}//"
		}

		if(isBenchMark.equals(TRUE)){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath

			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				deviceInstance?.logTransferPort,
				KEY_PERFORMANCE_BM,
				performanceFilePath
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
			htmlData += scriptExecutor.executeScript(cmd,1)
		}
		if(isSystemDiagnostics.equals(TRUE)){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				deviceInstance?.logTransferPort,
				KEY_PERFORMANCE_SD,
				performanceFilePath
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
			htmlData += scriptExecutor.executeScript(cmd,1)
		}
		
		def logTransferFileName = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDevice?.id.toString()}"
		def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"

		new File("${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
		logTransfer(deviceInstance,logTransferFilePath,logTransferFileName)
		
		return htmlData
	}
		
	/** 
	 *  Method to check whether the execution result is having any result update or not.
	 *  Check If execution result  got any update or it is initial status.
	 * @param executionResultId
	 * @return
	 */
	def checkExecutionCompletionStatus(def executionResultId){
		boolean status = true
		ExecutionResult.withTransaction {
			def resultArray = ExecutionResult.executeQuery("select a.status from ExecutionResult a where a.id = :exId",[exId: executionResultId])
			if(resultArray?.size() > 0){
//				if(resultArray[0] == Constants.UNDEFINED_STATUS || resultArray[0] == Constants.PENDING){
//					status = false
//				}
			}
		}
		return status
	}

	/**
	 * Create file to append execution log
	 * @param executionName
	 * @param scriptName
	 * @return
	 */
	private String prepareOutputfile(final String executionName, final String scriptName){
		try {
			def folderName = Constants.SCRIPT_OUTPUT_FILE_PATH
			File folder = grailsApplication.parentContext.getResource(folderName).file
			folder.mkdirs();

			def fileName = folderName+executionName+Constants.SCRIPT_OUTPUT_FILE_EXTN

			File opFile = grailsApplication.parentContext.getResource(fileName).file


			boolean append = true
			FileWriter fileWriter = new FileWriter(opFile, append)
			BufferedWriter buffWriter = new BufferedWriter(fileWriter)
			buffWriter.write("<br/>Executing script : "+scriptName+"<br/>"+NEW_LINE);
			buffWriter.write("======================================<br/>"+NEW_LINE);
			buffWriter.flush()
			buffWriter.close()
			return opFile.getAbsolutePath();
		} catch(Exception ex) {
		}

		return null
	}
	
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def logTransfer(def deviceInstance, def logTransferFilePath, def logTransferFileName){
		Thread.sleep(4000)
		try{			
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callConsoleLogTransfer.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				deviceInstance?.logTransferPort,
				"AgentConsole.log",
				logTransferFilePath			
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)		
			Thread.sleep(4000)
		}
		catch(Exception e){			
		}
	}

	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def resetAgent(def deviceInstance,String hardReset){
		try {
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				hardReset
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			Thread.sleep(4000)
			executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def resetAgent(def deviceInstance){
		try {
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				FALSE
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			Thread.sleep(4000)
			executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def hardResetAgent(def deviceInstance){
		try {
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				TRUE
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			Thread.sleep(4000)
			executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}


	/**
	 * Re run the tests if the status of script execution is not failure
	 * @param realPath
	 * @param filePath
	 * @param execName
	 * @return
	 */
	def reRunOnFailure(final String realPath, final String filePath, final String execName, final String uniqueExecutionName, final String appUrl){
		try {
				def aborted=false
		Execution executionInstance = Execution.findByName(execName)
		def exeId = executionInstance?.id
		def resultArray = Execution.executeQuery("select a.result from Execution a where a.name = :exName",[exName: execName])
		def result = resultArray[0]
		def newExecName
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
						executionSaveStatus = executionService.saveExecutionDetails(newExecName, scriptName, deviceName, scriptGroupInstance,appUrl,"false","false","false")
						cnt++
						Execution.withTransaction{
							rerunExecutionInstance = Execution.findByName(newExecName)
						}
					}
					if(executionSaveStatus){
						ExecutionDevice executionDevice
						ExecutionDevice.withTransaction {
							executionDevice = new ExecutionDevice()
							executionDevice.execution = rerunExecutionInstance
							executionDevice.device = deviceInstance?.stbName
							executionDevice.deviceIp = deviceInstance?.stbIp
							executionDevice.dateOfExecution = new Date()
							executionDevice.status = UNDEFINED_STATUS
							executionDevice.save(flush:true)
						}
						executionService.executeVersionTransferScript(realPath, filePath, newExecName, executionDevice?.id, deviceInstance.stbIp, deviceInstance?.logTransferPort)
						def executionResultList
						ExecutionResult.withTransaction {
							executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(executionInstance,execDeviceInstance,SUCCESS_STATUS)
						}
						def scriptInstance
						def htmlData

						def resultSize = executionResultList.size()
						int counter = 0
						def isMultiple = TRUE
						executionResultList.each{ executionResult ->
							if(!executionResult.status.equals(SKIPPED)){
//								scriptInstance = Script.findByName(executionResult?.script)
								def scriptFile = ScriptFile.findByScriptName(executionResult?.script)
								scriptInstance = scriptService.getScript(realPath,scriptFile?.moduleName,scriptFile?.scriptName)
								counter ++
								if(counter == resultSize){
									isMultiple = FALSE
								}
								if(scriptInstance){
								if(executionService.validateScriptBoxTypes(scriptInstance,deviceInstance)){
									aborted = executionService.abortList.contains(exeId?.toString())
									if(!aborted){
										htmlData = executeScript(newExecName, executionDevice, scriptInstance, deviceInstance, appUrl, filePath, realPath,"false","false",uniqueExecutionName,isMultiple,null)
										
									}
								}
								}
							}
						}
					}
				}
			}
			
			Execution execution = Execution.findByName(newExecName)
			if(aborted && executionService.abortList.contains(exeId?.toString())){
				executionService.abortList.remove(exeId?.toString())
			}
			
			Execution.withTransaction {
				Execution executionInstance1 = Execution.findByName(newExecName)
				executionService.saveExecutionStatus(aborted, executionInstance1?.id)
			}
		}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}


	/**
	 * Called from REST API : To save the result details
	 * @param executionId
	 * @param resultData
	 * @return
	 */

	def saveExecutionResultStatus(final String execId, final String resultData, final String execResult,
			final String expectedResult, final String resultStatus, final String testCaseName, final String execDevice)
	{
		try{
			if(resultData){
				String actualResult = resultData
				if(actualResult){
					ExecutionResult.withTransaction {
						ExecutionResult executionResult = ExecutionResult.findById(execResult)

						ExecuteMethodResult executionMethodResult = new ExecuteMethodResult()
						if(resultStatus.equals( STATUS_NONE ) || resultStatus == null ){
							executionMethodResult.status = actualResult
						}
						else{
							executionMethodResult.executionResult = executionResult
							executionMethodResult.expectedResult = expectedResult
							executionMethodResult.actualResult = actualResult
							executionMethodResult.status = resultStatus
						}
						executionMethodResult.functionName = testCaseName
						executionMethodResult.save(flush:true)

						executionResult.addToExecutemethodresults(executionMethodResult)
						executionResult.save(flush:true)

						Execution execution = Execution.findById(execId)
						ExecutionDevice execDeviceInstance = ExecutionDevice.findById(execDevice)
						if(!executionResult.status.equals( FAILURE_STATUS )){
							executionResult.status = resultStatus
							executionResult.save(flush:true)
							if(!execution.result.equals( FAILURE_STATUS )){
								execution.result = resultStatus
								execution.save(flush:true)
							}
							if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
								execDeviceInstance.addToExecutionresults(executionResult)
								execDeviceInstance.status = resultStatus
								execDeviceInstance.save(flush:true)
							}
						}
					}
				}
			}
			else{
				Execution.withTransaction {
					Execution execution = Execution.findById(execId)
					execution.result = FAILURE_STATUS
					execution.save(flush:true)
				}
			}
		}catch(Exception ex){
			ex.printStackTrace()
		}

	}

	/**
	 *  Called from REST API : To save the load module status
	 * @param executionId
	 * @param resultData
	 * @return
	 */
	def saveLoadModuleStatus(final String execId, final String statusData, final String execDevice, final String execResult){

		Execution.withTransaction{
			Execution execution = Execution.findById(execId)
			if(execution && !(execution?.result?.equals( FAILURE_STATUS ))){
				execution?.result = statusData?.toUpperCase().trim()
				execution?.save(flush:true)
			}

			ExecutionDevice execDeviceInstance = ExecutionDevice.findByExecutionAndId(execution,execDevice)
			if(execDeviceInstance && !(execDeviceInstance?.status.equals( FAILURE_STATUS ))){
				execDeviceInstance?.status = statusData?.toUpperCase().trim()
				execDeviceInstance?.save(flush:true)
			}

			ExecutionResult executionResult = ExecutionResult.findById(execResult)
			if(executionResult && !(executionResult?.status.equals( FAILURE_STATUS ))){
				executionResult?.status = statusData?.toUpperCase().trim()
				executionResult?.save(flush:true)
			}
		}
	}

	/**
	 * Execute scripts on Device
	 * @param execName
	 * @param device
	 * @param executionDevice
	 * @param scripts
	 * @param scriptGrp
	 * @param executionName
	 * @param filePath
	 * @param realPath
	 * @param groupType
	 * @param url
	 * @param isBenchMark
	 * @param isSystemDiagnostics
	 * @param rerun
	 * @return
	 */
	def executescriptsOnDevice(String execName, String device, ExecutionDevice executionDevice, def scripts, def scriptGrp,
			def executionName, def filePath, def realPath, def groupType, def url, def isBenchMark, def isSystemDiagnostics, def rerun)
	{
		
		boolean aborted = false
		boolean pause = false
		def scriptInstance
		Device deviceInstance 
		Device.withTransaction {
			deviceInstance= Device.findById(device)
		}
		ScriptGroup scriptGroupInstance
		StringBuilder output = new StringBuilder();
		def htmlData = ""
		int scriptGrpSize = 0
		int scriptCounter = 0
		def isMultiple = TRUE
		
		try{
		
		if(groupType == TEST_SUITE){
			scriptCounter = 0
			boolean skipStatus = false
			boolean notApplicable = false
			List validScriptList = new ArrayList()
			String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);

			ScriptGroup.withTransaction { trans ->
				scriptGroupInstance = ScriptGroup.findById(scriptGrp)
				scriptGroupInstance?.scriptList?.each { script ->
				def scriptInstance1 = scriptService.getScript(realPath,script?.moduleName, script?.scriptName)
				if(scriptInstance1){
					if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
						if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
						if(scriptInstance1?.skip?.toString().equals("true")){
							skipStatus = true
							executionService.saveSkipStatus(Execution.findByName(execName), executionDevice, scriptInstance1, deviceInstance)
							}else{
								validScriptList << scriptInstance1
							}
						}else{
							notApplicable = true
							String rdkVersionData = ""

//							Script.withTransaction {
//								def scriptInstance2 = Script.findById(script?.id)
								rdkVersionData = scriptInstance1?.rdkVersions
//							}

							String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData
							executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance1, deviceInstance,reason)
						}
					}else{
					
						notApplicable = true
						String boxTypeData = ""

						String deviceBoxType = ""

						Device.withTransaction {
							Device dev = Device.findById(deviceInstance?.id)
							deviceBoxType = dev?.boxType
						}

//						Script.withTransaction {
//							def scriptInstance1 = Script.findById(script?.id)
							boxTypeData = scriptInstance1?.boxTypes
//						}

						String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
						executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance1, deviceInstance,reason)
					}
				}else{
				
				String reason = "No script is available with name :"+script?.scriptName+" in module :"+script?.moduleName
				executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script?.scriptName, deviceInstance,reason)
				
				}
				}
			}

			scriptGrpSize = validScriptList?.size()
			Execution ex = Execution.findByName(execName)
			def exeId = ex?.id
			
			if((skipStatus || notApplicable)&& scriptGrpSize == 0){
				executionService.updateExecutionSkipStatusWithTransaction(FAILURE_STATUS, exeId)
				executionService.updateExecutionDeviceSkipStatusWithTransaction(FAILURE_STATUS, executionDevice?.id)
			}
			
			
			boolean executionStarted = false
			List pendingScripts = []
			validScriptList.each{ scriptObj ->
				
				
				scriptCounter++
				if(scriptCounter == scriptGrpSize){
					isMultiple = FALSE
				}
				aborted = executionService.abortList.contains(exeId?.toString())
				
				String devStatus = ""
				if(!pause && !aborted){
					try {
						devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						/*Thread.start{
							deviceStatusService.updateDeviceStatus(deviceInstance, devStatus)
						}*/
						if(devStatus.equals(Status.HANG.toString())){
							resetAgent(deviceInstance, TRUE)
							Thread.sleep(6000)
							devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						}
					}
					catch(Exception eX){
					}
				}
				if(!aborted && !(devStatus.equals(Status.NOT_FOUND.toString()) || devStatus.equals(Status.HANG.toString())) && !pause){
					executionStarted = true
					try {
						htmlData = executeScript(execName, executionDevice, scriptObj, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics, executionName, isMultiple,null)

					} catch (Exception e) {
					
						e.printStackTrace()
					}
					output.append(htmlData)
					Thread.sleep(6000)
				}else{
				
					if(!aborted && (devStatus.equals(Status.NOT_FOUND.toString()) ||  devStatus.equals(Status.HANG.toString()))){
						pause = true
					}

					if(!aborted && pause) {
						try {
							pendingScripts.add(scriptObj)
							def execInstance
							Execution.withTransaction {
								def execInstance1 = Execution.findByName(execName)
								execInstance = execInstance1
							}
							def scriptInstanceObj
//							Script.withTransaction {
//							Script scriptInstance1 = Script.findById(scriptObj.id)
							scriptInstanceObj = scriptObj
//							}
							Device deviceInstanceObj
							def devId = deviceInstance?.id
							Device.withTransaction {
								Device deviceInstance1 = Device.findById(devId)
								deviceInstanceObj = deviceInstance1
							}
							ExecutionDevice executionDevice1
							ExecutionDevice.withTransaction {
								def exDev = ExecutionDevice.findById(executionDevice?.id)
								executionDevice1 = exDev
							}
							
							ExecutionResult.withTransaction { resultstatus ->
							try {
								def executionResult = new ExecutionResult()
								executionResult.execution = execInstance
								executionResult.executionDevice = executionDevice1
								executionResult.script = scriptInstanceObj?.name
								executionResult.device = deviceInstanceObj?.stbName
								executionResult.execDevice = null
								executionResult.deviceIdString = deviceInstanceObj?.id?.toString()
								executionResult.status = PENDING
								executionResult.dateOfExecution = new Date()
								if(! executionResult.save(flush:true)) {
								}
								resultstatus.flush()
							}
							catch(Throwable th) {
								resultstatus.setRollbackOnly()
							}
							}
						} catch (Exception e) {
						}

					}
				}
			}
			if(aborted && executionService.abortList.contains(exeId?.toString())){
				executionService.abortList.remove(exeId?.toString())
			}

			if(!aborted && pause && pendingScripts.size() > 0 ){
				def exeInstance = Execution.findByName(execName)
				executionService.savePausedExecutionStatus(exeInstance?.id)
				executionService.saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
//				ExecutionDevice.withTransaction {
//					ExecutionDevice exDevice = ExecutionDevice.findById(idd)
//					exDevice.status = PAUSED
//					exDevice.save();
//				}
			}
		}
		else if(groupType == SINGLE_SCRIPT){

			if(scripts instanceof String){
				def moduleName= scriptService.scriptMapping.get(scripts)
				def script1 = scriptService.getScript(realPath,moduleName, scripts)
				isMultiple = FALSE
				try {
					htmlData = executeScript(execName, executionDevice, script1, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics,executionName,isMultiple,null)

				} catch (Exception e) {
					e.printStackTrace()
				}
				output.append(htmlData)
			}
			else{
				scriptCounter = 0
				List validScripts = new ArrayList()
				String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
				boolean notApplicable = false
				boolean skipStatus = false
					scripts.each { script ->
//						scriptInstance = Script.findById(script,[lock: true])
						def moduleName= scriptService.scriptMapping.get(script)
						if(moduleName){
						scriptInstance = scriptService.getScript(realPath,moduleName,script)
						if(scriptInstance){
						if(executionService.validateScriptBoxTypes(scriptInstance,deviceInstance)){
							if(executionService.validateScriptRDKVersions(scriptInstance,rdkVersion)){
								if(scriptInstance?.skip?.toString().equals("true")){
									skipStatus = true
									executionService.saveSkipStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance)
								}else{
									validScripts << scriptInstance
								}
							}else{
								notApplicable = true
								String rdkVersionData = ""
								rdkVersionData = scriptInstance?.rdkVersions

								String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData
								executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason)
							}
						}else{
							notApplicable = true
							String boxTypeData = ""

							String deviceBoxType = ""

							Device.withTransaction {
								Device dev = Device.findById(deviceInstance?.id)
								deviceBoxType = dev?.boxType
							}
								boxTypeData = scriptInstance?.boxTypes

							String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
							executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason)
						}
						}else{
				
							String reason = "No script is available with name :"+script+" in module :"+moduleName
								executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason)
				
						}
					}else{
				
					String reason = "No module information is present for script :"+script
					executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason)
				
				}
					}
				scriptGrpSize = validScripts?.size()
				Execution ex = Execution.findByName(execName)
				def exeId = ex?.id
				if((skipStatus || notApplicable)&& scriptGrpSize == 0){
					executionService.updateExecutionSkipStatusWithTransaction(FAILURE_STATUS, exeId)
					executionService.updateExecutionDeviceSkipStatusWithTransaction(FAILURE_STATUS, executionDevice?.id)
				}
				validScripts.each{ script ->
					
					scriptCounter++
					if(scriptCounter == scriptGrpSize){
						isMultiple = FALSE
					}
					
					try {
						htmlData = executeScript(execName, executionDevice, script, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics,executionName,isMultiple,null)
						output.append(htmlData)
					} catch (Exception e) {
					
						e.printStackTrace()
					}
					Thread.sleep(6000)
				}
			}
		}

		Execution executionInstance1 = Execution.findByName(execName)
		if(!pause){
			executionService.saveExecutionStatus(aborted, executionInstance1?.id)
		}
		htmlData = ""

		if(!aborted && !pause){

			def executionDeviceObj1
			ExecutionDevice.withTransaction{ wthTrans ->
				def executionObj = Execution.findByName(execName)
				def executionDeviceObj = ExecutionDevice.findAllByExecutionAndStatusNotEqual(executionObj, SUCCESS_STATUS)
				executionDeviceObj1 = executionDeviceObj
			}

			if((executionDeviceObj1) && (rerun)){
				htmlData = reRunOnFailure(realPath,filePath,execName,executionName,url)
				output.append(htmlData)
			}

		}else{
			resetAgent(deviceInstance)
		}
		deleteOutputFile(executionName)
		htmlData = output.toString()
		
		}
		catch(Exception ex){
			//println "Error "+ex.getMessage()
		}
		finally{
			if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
				executionService.deviceAllocatedList.remove(deviceInstance?.id)
			}
			
			String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
			Thread.start{
				deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
			}
		}
		
		return htmlData
	}

	/**
	 * Deletes the file created to store execution log
	 * @param opFileName
	 */
	private void deleteOutputFile(String opFileName){
		try{
			def fileName = Constants.SCRIPT_OUTPUT_FILE_PATH+opFileName+Constants.SCRIPT_OUTPUT_FILE_EXTN
			File opFile = grailsApplication.parentContext.getResource(fileName).file
			if(opFile.exists()){
				opFile.delete();
			}
		}catch(Exception e){
			e.printStackTrace();
		}
	}

	/**
	 * Calls when the execution of scripts is targeted on multiple devices.
	 * Scripts will be executed on multiple devices concurrently.
	 * @param execName
	 * @param device
	 * @param executionDevice
	 * @param scripts
	 * @param scriptGrp
	 * @param executionName
	 * @param filePath
	 * @param realPath
	 * @param groupType
	 * @param url
	 * @param isBenchMark
	 * @param isSystemDiagnostics
	 * @param rerun
	 * @return
	 */
	def executeScriptInThread(String execName, String device, ExecutionDevice executionDevice, def scripts, def scriptGrp,
			def executionName, def filePath, def realPath, def groupType, def url, def isBenchMark, def isSystemDiagnostics, def rerun){

		Future<String> future =  executorService.submit( {
			executescriptsOnDevice(execName, device, executionDevice, scripts, scriptGrp,
					executionName, filePath, realPath, groupType, url, isBenchMark, isSystemDiagnostics, rerun)} as Callable< String > )
	}

	/**
	 * Restart the script execution in case of device unavailablity
	 * @param execDevice
	 * @param grailsApplication
	 */
	public boolean restartExecution(ExecutionDevice execDevice, def grailsApplication){
		String htmlData = ""
		StringBuilder output = new StringBuilder()
		int scriptCounter = 0
		boolean pause = false
		String url = ""
		boolean aborted = false

		try {
			def rootFolder = grailsApplication.parentContext.getResource("/").file
					String rootPath = rootFolder.absolutePath
					String filePath = rootPath + "//fileStore"
					String realPath = rootPath
					def exId
					def exResults
					def eId = execDevice?.id
							ExecutionDevice.withTransaction {
				ExecutionDevice exDevice =  ExecutionDevice.findById(eId)
						exResults = exDevice?.executionresults
								exId = exDevice?.execution?.id
			}
			Execution execution
			boolean thirdParyExecution = false
			def thirdPartyExecutionDetails
			Execution.withTransaction {
				execution = Execution.findById(exId)
						thirdPartyExecutionDetails = execution?.thirdPartyExecutionDetails
								thirdParyExecution = (thirdPartyExecutionDetails != null)
			}
			ExecutionResult.withTransaction {
				exResults =  ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatus(execution,execDevice,PENDING)
			}
			Device deviceInstance
			url = execution?.applicationUrl
			String exName = execution?.name
			executionService.updateExecutionStatusData(INPROGRESS_STATUS, execution?.id)
			String isMultiple = TRUE
			int totalSize = exResults.size()
			exResults.each {
				try {
					scriptCounter++
					if(scriptCounter == totalSize){
						isMultiple = FALSE
					}
					
					def idVal = it?.id
					ExecutionResult.withTransaction {
						def exResult = ExecutionResult.findById(idVal)
								if(exResult?.status.equals(PENDING)){
									
											Device executionDevice = Device.findById(exResult?.deviceIdString)
											
											def scriptFile =ScriptFile.findByScriptName(exResult?.script)
											def script1 =scriptService.getScript(realPath,scriptFile.moduleName,scriptFile.scriptName)
											if(script1){
											if(executionService.validateScriptBoxTypes(script1,executionDevice)){
												aborted = executionService.abortList.contains(exId?.toString())
														
														String devStatus = ""
														if(!pause && !aborted){
															try {
																deviceInstance = executionDevice
																		devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, executionDevice)
																		/*Thread.start{
									 deviceStatusService.updateDeviceStatus(executionDevice, devStatus)
									 }*/
																		
																		if(devStatus.equals(Status.HANG.toString())){
																			resetAgent(deviceInstance, TRUE)
																			Thread.sleep(6000)
																			devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
																		}
															}
															catch(Exception eX){
															}
														}
												if(!aborted && !(devStatus.equals(Status.NOT_FOUND.toString()) || devStatus.equals(Status.HANG.toString()))&& !pause){
													
													
													htmlData = executeScript(exResult?.execution?.name, execDevice, script1 , executionDevice , url, filePath, realPath ,execution?.isBenchMarkEnabled.toString(), execution?.isSystemDiagnosticsEnabled?.toString(),exResult?.execution?.name,isMultiple,exResult)
															output.append(htmlData)
															if(!thirdParyExecution){
																Thread.sleep(6000)
															}
												}else{
													if(!aborted){
														pause = true
																def exeInstance = Execution.findByName(exResult.execution.name)
																ExecutionDevice.withTransaction {
															def exDev = ExecutionDevice.findById(execDevice?.id)
																	exDev.status = PAUSED
																	exDev.save(flush:true)
														}
														if(exeInstance){
															executionService.updateExecutionStatusData(PAUSED, exeInstance.id);
														}
													}
												}
											}
											}else{
											String reason = "No script is available with name :"+scriptFile?.scriptName+" in module :"+scriptFile?.moduleName
											executionService.saveNoScriptAvailableStatus(Execution.findByName(exResult?.execution?.name), executionDevice, scriptFile?.scriptName, deviceInstance,reason)
											}
								}
					}
				} catch (Exception e) {
					e.printStackTrace()
				}
			}
						
			if(aborted && executionService.abortList.contains(execution?.id?.toString())){				
				String dat = execution?.id?.toString()+","
						executionService.abortList.remove(execution?.id?.toString())
			}
			
			if(!pause){
				Execution executionInstance1 = Execution.findByName(exName)
				executionService.saveExecutionStatus(aborted, executionInstance1?.id)
				
			}
			
			//		if(!aborted && !pause){
			//
			//			def executionDeviceObj1
			//			boolean rerun = false
			//			  ExecutionDevice.withTransaction{ wthTrans ->
			//
			//				  def executionObj = Execution.findByName(exName)
			//				  println " execcc "+executionObj
			//				  println "executionObj?.isRerunRequired "+executionObj?.isRerunRequired
			//				  def executionDeviceObj = ExecutionDevice.findAllByExecutionAndStatusNotEqual(executionObj, SUCCESS_STATUS)
			//				  executionDeviceObj1 =  executionDeviceObj
			//				  rerun  	= executionObj?.isRerunRequired
			//				    }
			////			  if((executionDeviceObj1) && rerun ){
			////				  htmlData = reRunOnFailure(realPath,filePath,exName,exName,url)
			//////					  output.append(htmlData)
			////			  }
			//		  }
			
			if(aborted && deviceInstance ){
				resetAgent(deviceInstance)
			}
			
			if(!aborted && thirdPartyExecutionDetails && !pause){
				ThirdPartyExecutionDetails.withTransaction {
					scriptexecutionService.executeCallBackUrl(thirdPartyExecutionDetails.execName,thirdPartyExecutionDetails.url,thirdPartyExecutionDetails.callbackUrl,thirdPartyExecutionDetails.filePath,thirdPartyExecutionDetails.executionStartTime,thirdPartyExecutionDetails.imageName,thirdPartyExecutionDetails.boxType,realPath)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}finally{
//			if(!pause){
//				Execution executionInstance1 = Execution.findByName(exName)
//				executionService.saveExecutionStatus(aborted, executionInstance1?.id)
//			}
		}
		return pause;

	}
	
	/**
	 * Method to trigger the complete repeat execution
	 * @param execution
	 * @param execName
	 * @param grailsApplication
	 * @param deviceName
	 * @return
	 */
	public boolean triggerRepeatExecution(Execution execution , String execName , def grailsApplication,String deviceName){
		def scriptName = execution.script
//		def deviceName = execution.device
		def scriptGroup = execution.scriptGroup
		def url = execution.applicationUrl
		def groups = execution?.groups
		def isBenchMark = execution.isBenchMarkEnabled ? "true" : "false"
		def isSystemDiagnostics = execution.isSystemDiagnosticsEnabled ? "true" : "false"
		def rerun = execution.isRerunRequired ? "true" : "false"
		def htmlData
		def scriptGroupInstance 
		ScriptGroup.withTransaction {
			scriptGroupInstance= ScriptGroup.findByName(scriptGroup)
		}
		def rootFolder = grailsApplication.parentContext.getResource("/").file
		String rootPath = rootFolder.absolutePath
		String filePath = rootPath + "//fileStore"
		String realPath = rootPath
		def deviceInstance 
		Device.withTransaction {
			deviceInstance = Device.findByStbName(deviceName)
		}
		
		boolean paused = false

		boolean executionSaveStatus 
		
			executionSaveStatus = saveRepeatExecutionDetails(execName, "", deviceName, scriptGroupInstance,url,isBenchMark,isSystemDiagnostics,rerun,groups)
		
		def executionDevice
		if(executionSaveStatus){
			try{
				ExecutionDevice.withTransaction {
					executionDevice = new ExecutionDevice()
					executionDevice.execution = Execution.findByName(execName)
					executionDevice.dateOfExecution = new Date()
					executionDevice.device = deviceInstance?.stbName
					executionDevice.deviceIp = deviceInstance?.stbIp
					executionDevice.status = UNDEFINED_STATUS
					executionDevice.save(flush:true)
				}
			}
			catch(Exception e){
				e.printStackTrace()
			}
			
			def scriptId
			String deviceID = deviceInstance?.id
			executionService.executeVersionTransferScript(realPath,filePath,execName, executionDevice?.id, deviceInstance?.stbIp, deviceInstance?.logTransferPort)
			try {
				htmlData = repeatExecutionOnDevice(execName,deviceID , executionDevice, "", scriptGroupInstance?.id, execName,
					filePath, realPath, TEST_SUITE, url, isBenchMark, isSystemDiagnostics, rerun)

			} catch (Exception e) {
				e.printStackTrace()
			}

			Execution exe = Execution.findByName(execName)
			if(exe){
				paused = exe?.executionStatus.equals(Constants.PAUSED)
			}
		}
		return paused
	}
	
	/**
	 * Method to save the repeat execution details
	 */
	public boolean saveRepeatExecutionDetails(final String execName, String scriptName, String deviceName,
		ScriptGroup scriptGroupInstance , String appUrl,String isBenchMark , String isSystemDiagnostics,String rerun,Groups groups){
		   def executionSaveStatus = true
		   try {
			   Execution.withTransaction {
			   Execution execution = new Execution()
			   execution.name = execName
			   execution.script = scriptName
			   execution.device = deviceName
			   execution.scriptGroup = scriptGroupInstance?.name
			   execution.result = UNDEFINED_STATUS
			   execution.executionStatus = INPROGRESS_STATUS
			   execution.dateOfExecution = new Date()
			   execution.groups = groups
			   execution.applicationUrl = appUrl
			   execution.isRerunRequired = rerun?.equals("true")
			   execution.isBenchMarkEnabled = isBenchMark?.equals("true")
			   execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals("true")
			   if(! execution.save(flush:true)) {
				   executionSaveStatus = false
			   }
			   
			   }
		   }
		   catch(Exception th) {
			   th.printStackTrace()
			   executionSaveStatus = false
		   }
		   return executionSaveStatus
	   }
		
	/**
	 *	Method to execute a execute a script on device as part of repeat after pause
	 * @return
	 */
	def repeatExecutionOnDevice(String execName, String device, ExecutionDevice executionDevice, def scripts, def scriptGrp,
			def executionName, def filePath, def realPath, def groupType, def url, def isBenchMark, def isSystemDiagnostics, def rerun)
	{
		boolean aborted = false
		boolean pause = false
		def scriptInstance
		Device deviceInstance
		Device.withTransaction {
			deviceInstance = Device.findById(device)
		}
		ScriptGroup scriptGroupInstance
		StringBuilder output = new StringBuilder();
		def htmlData = ""
		int scriptGrpSize = 0
		int scriptCounter = 0
		def isMultiple = TRUE
		if(groupType == TEST_SUITE){
			scriptCounter = 0
			boolean skipStatus = false
			boolean notApplicable = false
			List validScriptList = new ArrayList()
			String rdkVersion = ""
			Device.withTransaction {
				Device dev = Device.findById(deviceInstance?.id)
				rdkVersion = executionService.getRDKBuildVersion(dev);
			}
			ScriptGroup.withTransaction { trans ->
				scriptGroupInstance = ScriptGroup.findById(scriptGrp)
				scriptGroupInstance.scriptList.each { script ->
					
					scriptInstance = scriptService.getScript(realPath, script?.moduleName, script?.scriptName)
					if(scriptInstance){
					if(executionService.validateScriptBoxTypes(scriptInstance,deviceInstance)){
						if(executionService.validateScriptRDKVersions(scriptInstance,rdkVersion)){
							if(scriptInstance.skip.toString().equals("true")){
								skipStatus = true
								executionService.saveSkipStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance)
							}else{
								validScriptList << scriptInstance
							}

						}else{
							notApplicable = true
							String rdkVersionData = ""

//							Script.withTransaction {
//								def scriptInstance1 = Script.findById(script?.id)
							
								rdkVersionData = scriptInstance?.rdkVersions
//							}

							String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData
							executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason)
						}
					}else{
						notApplicable = true
						String boxTypeData = ""

						String deviceBoxType = ""

						Device.withTransaction {
							Device dev = Device.findById(deviceInstance?.id)
							deviceBoxType = dev?.boxType

						}

//						Script.withTransaction {
//							def scriptInstance1 = Script.findById(script?.id)
							boxTypeData = scriptInstance?.boxTypes
//						}

						String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
						executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason)
					}
					}else{
					String reason = "No script is available with name :"+script?.scriptName+" in module :"+script?.moduleName
					executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script?.scriptName, deviceInstance,reason)
					}
				}
			}
			
			scriptGrpSize = validScriptList?.size()
			Execution ex = Execution.findByName(execName)
			def exeId = ex?.id

			if((skipStatus || notApplicable) && scriptGrpSize == 0){
//				executionService.updateExecutionSkipStatusWithTransaction(SKIPPED, exeId)
				executionService.updateExecutionSkipStatusWithTransaction(FAILURE_STATUS, exeId)
				executionService.updateExecutionDeviceSkipStatusWithTransaction(FAILURE_STATUS, executionDevice?.id)
			}
			boolean executionStarted = false
			List pendingScripts = []
			validScriptList.each{ scriptObj ->

				scriptCounter++
				if(scriptCounter == scriptGrpSize){
					isMultiple = FALSE
				}
				aborted = executionService.abortList.contains(exeId?.toString())

				String devStatus = ""
				if(!pause && !aborted){
					try {
						devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						/*Thread.start{
							deviceStatusService.updateDeviceStatus(deviceInstance, devStatus)
						}*/
					}
					catch(Exception eX){
					}
				}
				
				if(!aborted && !devStatus.equals(Status.NOT_FOUND.toString()) && !pause){
					executionStarted = true
					htmlData = executeScript(execName, executionDevice, scriptObj, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics, executionName, isMultiple,null)
					output.append(htmlData)
					Thread.sleep(6000)
				}else{
					if(!aborted && devStatus.equals(Status.NOT_FOUND.toString())){
						pause = true
					}

					if(!aborted && pause) {
						
						try {
							pendingScripts.add(scriptObj)
							def execInstance
							Execution.withTransaction {
								def execInstance1 = Execution.findByName(execName)
								execInstance = execInstance1
							}
							Script scriptInstanceObj
//							Script.withTransaction {
//								Script scriptInstance1 = Script.findById(scriptObj.id)
								scriptInstanceObj = scriptInstance
//							}
							Device deviceInstanceObj
							def devId = deviceInstance?.id
							Device.withTransaction {
								Device deviceInstance1 = Device.findById(devId)
								deviceInstanceObj = deviceInstance1
							}
							ExecutionDevice executionDevice1
							ExecutionDevice.withTransaction {
								def exDev = ExecutionDevice.findById(executionDevice?.id)
								executionDevice1 = exDev
							}

							ExecutionResult.withTransaction { resultstatus ->
								try {
									def executionResult = new ExecutionResult()
									executionResult.execution = execInstance
									executionResult.executionDevice = executionDevice1
									executionResult.script = scriptInstanceObj?.name
									executionResult.device = deviceInstanceObj?.stbName
									executionResult.execDevice = null
									executionResult.deviceIdString = deviceInstanceObj?.id?.toString()
									executionResult.status = PENDING
									executionResult.dateOfExecution = new Date()
									if(! executionResult.save(flush:true)) {
									}
									resultstatus.flush()
								}
								catch(Throwable th) {
									resultstatus.setRollbackOnly()
								}
							}
						} catch (Exception e) {
						
						}

					}
				}
			}
			if(aborted && executionService.abortList.contains(exeId?.toString())){
				executionService.abortList.remove(exeId?.toString())
			}

			if(!aborted && pause && pendingScripts.size() > 0 ){
				def exeInstance = Execution.findByName(execName)
				executionService.savePausedExecutionStatus(exeInstance?.id)
				executionService.saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
				//				ExecutionDevice.withTransaction {
				//					ExecutionDevice exDevice = ExecutionDevice.findById(idd)
				//					exDevice.status = PAUSED
				//					exDevice.save();
				//				}
			}
		}
		Execution executionInstance1 = Execution.findByName(execName)
		if(!pause){
			executionService.saveExecutionStatus(aborted, executionInstance1?.id)
		}
		htmlData = ""

		if(!aborted && !pause){

			def executionDeviceObj1
			ExecutionDevice.withTransaction{ wthTrans ->
				def executionObj = Execution.findByName(execName)
				def executionDeviceObj = ExecutionDevice.findAllByExecutionAndStatusNotEqual(executionObj, SUCCESS_STATUS)
				executionDeviceObj1 = executionDeviceObj
			}
			if((executionDeviceObj1) && (rerun.equals(TRUE))){
				htmlData = reRunOnFailure(realPath,filePath,execName,executionName,url)
				output.append(htmlData)
			}

		}else{
			resetAgent(deviceInstance)
		}
		deleteOutputFile(executionName)
		htmlData = output.toString()
		return htmlData
	}

}
