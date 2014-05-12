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

	/**
	 * Injects the deviceStatusService.
	 */
	def deviceStatusService

	/**
	 * Injects the scriptexecutionService.
	 */
	def scriptexecutionService

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
	def String executeScript(final String executionName, final ExecutionDevice executionDevice, final Script scriptInstance,
			final Device deviceInstance, final String url, final String filePath, final String realPath, final String isBenchMark, final String isSystemDiagnostics,final String uniqueExecutionName,final String isMultiple, def executionResult) {

		String htmlData = ""
		String scriptData = executionService.convertScriptFromHTMLToPython(scriptInstance.scriptContent)
		String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES

		def executionInstance = Execution.findByName(executionName)
		def executionId = executionInstance?.id
		Date executionDate = executionInstance?.dateOfExecution

		def execStartTime = executionDate?.getTime()
		if(executionResult == null){
			ExecutionResult.withTransaction { resultstatus ->
				try {
					executionResult = new ExecutionResult()
					executionResult.execution = executionInstance
					executionResult.executionDevice = executionDevice
					executionResult.script = scriptInstance.name
					executionResult.device = deviceInstance.stbName
					if(! executionResult.save(flush:true)) {
						log.error "Error saving executionResult instance : ${executionResult.errors}"
					}
					resultstatus.flush()
				}
				catch(Throwable th) {
					resultstatus.setRollbackOnly()
				}
			}
		}

		def executionResultId = executionResult?.id
		scriptData = scriptData.replace( IP_ADDRESS , stbIp )
		scriptData = scriptData.replace( PORT , deviceInstance?.stbPort )

		String gatewayIp = deviceInstance?.gatewayIp

		scriptData = scriptData.replace( REPLACE_TOKEN, LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath +SINGLE_QUOTES + COMMA_SEPERATOR +
				executionId  + COMMA_SEPERATOR + executionDevice?.id + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.logTransferPort + COMMA_SEPERATOR + deviceInstance?.statusPort + COMMA_SEPERATOR +
				scriptInstance?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR + SINGLE_QUOTES + isBenchMark + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + isSystemDiagnostics + SINGLE_QUOTES + COMMA_SEPERATOR +
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
		String outData = executionService.executeScript( file.getPath() , scriptInstance.executionTime, uniqueExecutionName , scriptInstance.getName())
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
			if(htmlData.contains(KEY_SCRIPTEND)){
				htmlData = htmlData.replaceAll(KEY_SCRIPTEND,"")
			}
			executionService.updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff)
			Thread.sleep(4000)
			resetAgent(deviceInstance)
		}
		else{
			if(htmlData.contains(KEY_SCRIPTEND)){
				htmlData = htmlData.replaceAll(KEY_SCRIPTEND,"")
				String outputData = htmlData
				executionService.updateExecutionResults(outputData,executionResultId,executionId,executionDevice?.id,timeDiff)
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
						TRUE
					]
					ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
					def resetExecutionData = scriptExecutor.executeScript(cmd)
					htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
					executionService.updateExecutionResults(htmlData,executionResultId,executionId,executionDevice?.id)
					Thread.sleep(4000)
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
			htmlData += scriptExecutor.executeScript(cmd)
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
			htmlData += scriptExecutor.executeScript(cmd)
		}
		return htmlData
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
	def resetAgent(def deviceInstance){

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
		def resetExecutionData = scriptExecutor.executeScript(cmd)
		Thread.sleep(4000)
	}


	/**
	 * Re run the tests if the status of script execution is not failure
	 * @param realPath
	 * @param filePath
	 * @param execName
	 * @return
	 */
	def reRunOnFailure(final String realPath, final String filePath, final String execName, final String uniqueExecutionName, final String appUrl){
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
								scriptInstance = Script.findByName(executionResult?.script)
								if(counter == resultSize){
									isMultiple = FALSE
								}
								if(executionService.validateScriptBoxType(scriptInstance,deviceInstance)){
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
			Execution.withTransaction {
				Execution executionInstance1 = Execution.findByName(newExecName)
				executionService.saveExecutionStatus(aborted, executionInstance1?.id)
			}
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
		Device deviceInstance = Device.findById(device)
		ScriptGroup scriptGroupInstance
		StringBuilder output = new StringBuilder();
		def htmlData = ""
		int scriptGrpSize = 0
		int scriptCounter = 0
		def isMultiple = TRUE
		if(groupType == TEST_SUITE){

			scriptCounter = 0
			boolean skipStatus = false
			List<Script> validScriptList = new ArrayList<Script>()

			ScriptGroup.withTransaction { trans ->
				scriptGroupInstance = ScriptGroup.findById(scriptGrp)
				scriptGroupInstance.scripts.each { script ->
					if(executionService.validateScriptBoxType(script,deviceInstance)){
						if(script.skip){
							skipStatus = true
							executionService.saveSkipStatus(Execution.findByName(execName), executionDevice, script, deviceInstance)
						}else{
							validScriptList << script
						}
					}
				}
			}

			scriptGrpSize = validScriptList?.size()
			Execution ex = Execution.findByName(execName)
			def exeId = ex?.id
			
			if(skipStatus && scriptGrpSize <= 0){
				executionService.updateExecutionSkipStatusWithTransaction(SKIPPED, exeId)
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
				if(!pause){
					try {
						devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						Thread.start{
							deviceStatusService.updateDeviceStatus(deviceInstance, devStatus)
						}
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
				
					if(devStatus.equals(Status.NOT_FOUND.toString())){
						pause = true
					}

					if(pause) {
						try {
							pendingScripts.add(scriptObj.getId())
							def execInstance
							Execution.withTransaction {
								def execInstance1 = Execution.findByName(executionName)
								execInstance = execInstance1
							}
							Script scriptInstanceObj
							Script.withTransaction {
							Script scriptInstance1 = Script.findById(scriptObj.id)
							scriptInstanceObj = scriptInstance1
							}
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
								executionResult.execDevice = deviceInstanceObj
								executionResult.status = PENDING
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
			if(executionService.abortList.contains(exeId?.toString())){
				executionService.abortList.remove(exeId?.toString())
			}
			if(pause && pendingScripts.size() > 0 ){
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
				scriptInstance = Script.findById(scripts,[lock: true])
				isMultiple = FALSE
				htmlData = executeScript(execName, executionDevice, scriptInstance, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics,executionName,isMultiple,null)
				output.append(htmlData)
			}
			else{
				scriptCounter = 0
				List<Script> validScripts = new ArrayList<Script>()
				scripts.each { script ->

					scriptInstance = Script.findById(script,[lock: true])
					if(executionService.validateScriptBoxType(scriptInstance,deviceInstance)){
						validScripts << scriptInstance
					}
				}
				scriptGrpSize = validScripts?.size()
				validScripts.each{ script ->
					scriptCounter++
					if(scriptCounter == scriptGrpSize){
						isMultiple = FALSE
					}

					htmlData = executeScript(execName, executionDevice, script, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics,executionName,isMultiple,null)
					output.append(htmlData)
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
	public void restartExecution(ExecutionDevice execDevice, def grailsApplication){

		String htmlData = ""
		StringBuilder output = new StringBuilder()
		int scriptCounter = 0
		boolean pause = false
		String url = ""
		boolean aborted = false

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
		exResults =  ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatus(execution,execDevice,PENDING)

		Device deviceInstance
		url = execution?.applicationUrl
		String exName = execution?.name
		executionService.updateExecutionStatusData(INPROGRESS_STATUS, execution?.id)
		String isMultiple = TRUE
		int totalSize = exResults.size()
		exResults.each {

			scriptCounter++
			if(scriptCounter == totalSize){
				isMultiple = FALSE
			}

			def idVal = it?.id
			ExecutionResult.withTransaction {
				def exResult = ExecutionResult.findById(idVal)
				if(exResult?.status.equals(PENDING)){

					if(executionService.validateScriptBoxType(Script.findByName(exResult?.script),exResult?.execDevice)){

						aborted = executionService.abortList.contains(exId?.toString())
						
						
						String devStatus = ""
						if(!pause && !aborted){
							try {
								deviceInstance = exResult?.execDevice
								devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, exResult?.execDevice)
								Thread.start{
									deviceStatusService.updateDeviceStatus(exResult?.execDevice, devStatus)
								}
							}
							catch(Exception eX){
							}
						}
						

						if(!aborted && !devStatus.equals(Status.NOT_FOUND.toString()) && !pause){

							htmlData = executeScript(exResult?.execution?.name, execDevice, Script.findByName(exResult?.script) , exResult?.execDevice , url, filePath, realPath ,execution?.isBenchMarkEnabled.toString(), execution?.isSystemDiagnosticsEnabled?.toString(),exResult?.execution?.name,isMultiple,exResult)
							output.append(htmlData)
							if(!thirdParyExecution){
								Thread.sleep(6000)
							}

						}else{
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

						if(executionService.abortList.contains(execution?.id?.toString())){
							executionService.abortList.remove(execution?.id?.toString())
						}

					}
				}
			}
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

		if(thirdPartyExecutionDetails){
			ThirdPartyExecutionDetails.withTransaction {
				scriptexecutionService.executeCallBackUrl(thirdPartyExecutionDetails.execName,thirdPartyExecutionDetails.url,thirdPartyExecutionDetails.callbackUrl,thirdPartyExecutionDetails.filePath,thirdPartyExecutionDetails.executionStartTime,thirdPartyExecutionDetails.imageName,thirdPartyExecutionDetails.boxType)
			}
		}

	}


}
