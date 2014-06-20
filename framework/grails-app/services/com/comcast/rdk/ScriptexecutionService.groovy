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

import com.google.gson.JsonArray
import com.google.gson.JsonObject
import com.google.gson.JsonPrimitive
import java.util.List;
import java.util.concurrent.FutureTask
import java.util.regex.Matcher
import java.util.regex.Pattern

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.Executors;
/**
 * Service class for the Asynchronous Execution of Scripts for REST.
 * @author sreejasuma
 */

class ScriptexecutionService {
	
	static datasource = 'DEFAULT'
	
    /**
	 * Injecting executor service.
	 */
	static ExecutorService executorService = Executors.newCachedThreadPool()
	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication
	
	def executionService
	
	def deviceStatusService
	
	def executescriptService
	
	/**
	 * Method to save details of execution in Execution Domain
	 * @param execName
	 * @param scriptName
	 * @param deviceName
	 * @param scriptGroupInstance
	 * @return
	 */
	public boolean saveExecutionDetails(final String execName, String scriptName, String deviceName,
			ScriptGroup scriptGroupInstance, String appUrl){

		def executionSaveStatus = true
		try{
			int scriptCnt = 0
			if(scriptGroupInstance?.scripts?.size() > 0){
				scriptCnt = scriptGroupInstance?.scripts?.size()
			}
			
			Execution execution = new Execution()
			execution.name = execName
			execution.script = scriptName
			execution.device = deviceName
			execution.scriptGroup = scriptGroupInstance?.name
			execution.result = UNDEFINED_STATUS
			execution.executionStatus = INPROGRESS_STATUS
			execution.dateOfExecution = new Date()
			execution.applicationUrl = appUrl
			execution.scriptCount = scriptCnt
			if(! execution.save(flush:true)) {
				log.error "Error saving Execution instance : ${execution.errors}"
				executionSaveStatus = false
			}
		}
		catch(Exception th) {
			//th.printStackTrace()
			executionSaveStatus = false
		}
		return executionSaveStatus
	}
	

	def executeScriptGroup(ScriptGroup scriptGroup, final String boxType,  final String execName, final String execDeviceId,
		Device deviceInstance, final String url, final String filePath, final String realPath, final String callbackUrl, final String imageName ){
		Future<String> future =  executorService.submit( { executeScriptGrp(scriptGroup, boxType, execName, execDeviceId, deviceInstance,
			url, filePath, realPath, callbackUrl, imageName)} as Callable< String > )
  
	}
		
	def String getCurlCommand(final String jsonString, final String callbackUrl){
		String curlCommand
		try{
			File jenkFile = grailsApplication.parentContext.getResource("//fileStore//jenkinscredential.txt").file
			String valueString
			String jenkUser=""
			String jenkPwd=""
			if(jenkFile.exists()){
			jenkFile.eachLine {
				if (it.startsWith('JENK_USER:')) {
					valueString = it
					valueString = valueString.replaceAll("JENK_USER:", "")
					jenkUser = valueString.trim()
				}
				else if(it.startsWith('JENK_PWD:')){
					valueString = it
					valueString = valueString.replaceAll("JENK_PWD:", "")
					jenkPwd = valueString.trim()
				}
			}
		}
			/*String jsonString = jsonData.toString();
			jsonString = jsonString.replaceAll("\"", "\\\\\"")*/
			
			if(jenkUser && jenkPwd && callbackUrl){
				curlCommand = "curl --fail -X POST --insecure --user ${jenkUser}:${jenkPwd} ${callbackUrl} -F json=\"{\\\"parameter\\\":[{\\\"name\\\":\\\"TDK_DATA\\\",\\\"value\\\":\\\"${jsonString}\\\"}]}\" --verbose"
				//curlCommand = "curl --fail -X POST --insecure --user ${jenkUser}:${jenkPwd} ${callbackUrl} -F json=\"${jsonString}\" --verbose"
			}
		}
		catch(Exception ex){
			ex.printStackTrace()
		}

		return curlCommand
	}
		
	def executeScriptGrp(ScriptGroup scriptGroup, final String boxType, final String execName, final String execDeviceId,
		Device deviceInstance, final String url, final String filePath, final String realPath, final String callbackUrl, final String imageName){
		
		boolean aborted = false
		boolean pause = false
		try{
		
			List<Script> validScripts = new ArrayList<Script>()
			boolean skipStatus = false
			boolean notApplicable = false
			String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
			
			scriptGroup.scripts.each { script ->
				if(validateBoxTypeOfScript(script,boxType)){
					if(executionService.validateScriptRDKVersion(script, rdkVersion)){
						if(script.skip){
							skipStatus = true
							executionService.saveSkipStatus(Execution.findByName(execName), ExecutionDevice.findById(execDeviceId), script, deviceInstance)
						}else{
							validScripts << script
						}
					}else{
						notApplicable =true
						String rdkVersionData = ""
						Script.withTransaction {
							def scriptInstance1 = Script.findById(script?.id)
							rdkVersionData = scriptInstance1?.rdkVersions
						}

						String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData

						executionService.saveNotApplicableStatus(Execution.findByName(execName), ExecutionDevice.findById(execDeviceId), script, deviceInstance,reason)
					}
				}else{
					notApplicable = true
					String boxTypeData = ""

					String deviceBoxType = ""

					Device.withTransaction {
						Device dev = Device.findById(deviceInstance?.id)
						deviceBoxType = dev?.boxType
					}

					Script.withTransaction {
						def scriptInstance1 = Script.findById(script?.id)
						boxTypeData = scriptInstance1?.boxTypes
					}

					String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData

					executionService.saveNotApplicableStatus(Execution.findByName(execName), ExecutionDevice.findById(execDeviceId), script, deviceInstance,reason)
				}
			}
			int scriptGrpSize = validScripts?.size()
			
			int scriptCounter = 0
			def isMultiple = "true"
			
			def executionStartTime = System.currentTimeMillis()
			
			Execution ex = Execution.findByName(execName)
			ExecutionDevice execDevice = ExecutionDevice.findById(execDeviceId)
			if((skipStatus || notApplicable)&& scriptGrpSize == 0){
				if(ex){
					executionService.updateExecutionSkipStatusWithTransaction(FAILURE_STATUS, ex?.id)
					executionService.updateExecutionDeviceSkipStatusWithTransaction(FAILURE_STATUS, execDevice?.id)
				}
			}
			
			boolean executionStarted = false
			List pendingScripts = []
			validScripts.each{ scriptInstance ->
				scriptCounter++
				if(scriptCounter == scriptGrpSize){
					isMultiple = "false"
				}
				
				
				aborted = ExecutionService.abortList.contains(ex?.id?.toString())
				String devStatus = ""
				if(!pause && !aborted){
					try {
						devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						/*Thread.start{
							deviceStatusService.updateDeviceStatus(deviceInstance, devStatus)
						}*/
						
						if(devStatus.equals(Status.HANG.toString())){
							executionService.resetAgent(deviceInstance, TRUE)
							Thread.sleep(6000)
							devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						}
						
					}
					catch(Exception eX){
					}
				}
				
				if(!aborted && !(devStatus.equals(Status.NOT_FOUND.toString()) || devStatus.equals(Status.HANG.toString())) && !pause){
					executionStarted = true
					def htmlData = executeScripts(execName, execDeviceId, scriptInstance , deviceInstance , url, filePath, realPath, isMultiple)
					if(isMultiple.equals("false")){
						Execution.withTransaction {
							Execution executionInstance = Execution.findByName(execName)
							executionInstance.executionStatus = COMPLETED_STATUS
							executionInstance.save(flush:true)
						}
					}
				}else{
					if(!aborted && (devStatus.equals(Status.NOT_FOUND.toString()) || devStatus.equals(Status.HANG.toString()))){
						pause = true
					}
					
					if(!aborted && pause) {
						pendingScripts.add(scriptInstance.getId())
						
						def execInstance = Execution.findByName(execName,[lock: true])
						Script scriptInstance1 = Script.findById(scriptInstance.id,[lock: true])
						Device deviceInstance1 = Device.findById(deviceInstance.id,[lock: true])
						def executionResult
						ExecutionResult.withTransaction { resultstatus ->
							try {
								executionResult = new ExecutionResult()
								executionResult.execution = execInstance
								executionResult.executionDevice = ExecutionDevice.findById(execDeviceId)
								executionResult.script = scriptInstance1?.name
								executionResult.device = deviceInstance1?.stbName
								executionResult.execDevice = null
								executionResult.deviceIdString = deviceInstance1?.id?.toString()
								executionResult.status = "PENDING"
								executionResult.dateOfExecution = new Date()
								if(! executionResult.save(flush:true)) {
	//								log.error "Error saving executionResult instance : ${executionResult.errors}"
								}
								resultstatus.flush()
								
							}
							catch(Throwable th) {
								resultstatus.setRollbackOnly()
							}
						}
						
					}
				}
			}
			
			if(aborted){
				if(executionService.abortList.contains(ex?.id?.toString())){
					executionService.abortList.remove(ex?.id?.toString())
				}
				
				Execution.withTransaction {
					Execution executionInstance = Execution.findByName(execName)
					executionInstance.executionStatus = ABORTED_STATUS
					executionInstance.isAborted = true
					executionInstance.save(flush:true)
				}
				
				executionService.resetAgent(deviceInstance, FALSE)
			}
			
			if(pause && pendingScripts.size() > 0 ){
				def exeInstance = Execution.findByName(execName)
				executionService.savePausedExecutionStatus(exeInstance?.id)

				ExecutionDevice.withTransaction {
					ExecutionDevice exDevice = ExecutionDevice.findById(execDeviceId)
					exDevice.status = "PAUSED"
					exDevice.save();
				}
			}
			
			
			Execution executionInstance1 = Execution.findByName(execName)
			if(!pause){
				executionService.saveExecutionStatus(aborted, executionInstance1?.id)
			}
			
			
			if(callbackUrl){
				if(pause){
					saveThirdPartyExecutionDetails(Execution.findByName(execName),execName,url,callbackUrl,filePath,executionStartTime,imageName,boxType)
				}else{
					executeCallBackUrl(execName,url,callbackUrl,filePath,executionStartTime,imageName,boxType)
				}
			}
					
		}
		catch(Exception e){
			e.printStackTrace()
		}
		finally{
			if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
				executionService.deviceAllocatedList.remove(deviceInstance?.id)
				String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
				Thread.start{
					deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
				}
			}
		}
	}
	
		def saveThirdPartyExecutionDetails(final def execution, final def execName, final def url, final def callbackUrl, final def filePath, 
			final def executionStartTime, final def imageName, final def boxType){
			
		try{
			ThirdPartyExecutionDetails details
			ThirdPartyExecutionDetails.withTransaction {
				details = new ThirdPartyExecutionDetails()
				details.execution = execution
				details.execName = execName
				details.url = url
				details.callbackUrl = callbackUrl
				details.filePath = filePath
				details.executionStartTime = executionStartTime
				details.imageName = imageName
				details.boxType = boxType
				details.save(flush:true)
			}
			if(details){
				Execution.withTransaction{
					Execution ex =Execution.findById(execution?.id)
					ex.thirdPartyExecutionDetails = details
					ex.save(flush:true)
				}
			}
		}catch(Exception e){
		e.printStackTrace()
		}
	}
			
		def executeCallBackUrl(final def execName, final def url, final def callbackUrl, final def filePath, 
			final def executionStartTime, final def imageName, final def boxType){
			String curlCommand = getCurlCommand(thirdPartyJsonResult(execName,url,executionStartTime,imageName,boxType), callbackUrl)
	
			File newFile = new File(filePath, execName+"-curlscript.sh");
			boolean isFileCreated = newFile.createNewFile()
			if(isFileCreated) {
				newFile.setExecutable(true, false )
			}

			if(curlCommand){
				PrintWriter fileNewPrintWriter = newFile.newPrintWriter();
				fileNewPrintWriter.print( curlCommand )
				fileNewPrintWriter.flush()
				fileNewPrintWriter.close()
				def absolutePath = newFile.absolutePath

				if(absolutePath != null){
		
					String[] cmd = [
						"sh",
						absolutePath
					]
					def outputData
					try {
						ScriptExecutor scriptExecutor = new ScriptExecutor()
						outputData = scriptExecutor.executeScript(cmd)
					} catch (Exception e) {
						e.printStackTrace()
					}
					
				}
			}
			if(newFile.exists()){
				newFile.delete();
			}
		}
		
		
		
		def String thirdPartyJsonResult(final String execName, final String appurl, final def executionStartTime,
			final String imageName, final String boxType ){

			JsonArray jsonArray = new JsonArray()
			JsonObject compNode
			JsonObject deviceNode
			JsonObject executionNode
			String appUrl = appurl
			String url
			appUrl = appUrl + "/execution/getDetailedTestResult?execResId="
			Execution executionInstance = Execution.findByName(execName)
			if(executionInstance){
				ScriptGroup scriptGrp = ScriptGroup.findByName(executionInstance?.scriptGroup)
				def executionResultStatus //= ExecutionResult.findAllByExecutionAndStatusIsNotNull(executionInstance)
				def scriptStatus = null
				def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
				def executionResult //= ExecutionResult.findAllByExecution(executionInstance)

				executionDevice.each{ execDevice ->
					url = ""
					compNode = new JsonObject()
					deviceNode = new JsonObject()
					executionResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
			
						List<ExecutionResult> execResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
						def componentMap = [:].withDefault {[]}
						def systemMap = [:].withDefault {[]}
						execResult.each{ execResObj ->
							Script.withTransaction { scriptRes ->
								Script script = Script.findByName(execResObj?.script)
								if(script.primitiveTest.module.testGroup.groupValue.toString().equals("E2E") ){
									List val1 = systemMap.get(script.primitiveTest.module.toString());
									if(!val1){
										val1 = []
										systemMap.put(script.primitiveTest.module.toString(), val1)
									}
									val1.add(execResObj?.id)
								}
								else{
									List val = componentMap.get(script.primitiveTest.module.toString());
									if(!val){
										val = []
										componentMap.put(script.primitiveTest.module.toString(), val)
									}
									val.add(execResObj?.id)
								}
							}
						}
						def statusVal
						def newmap = [:]
						JsonArray compArray = new JsonArray();
						
						componentMap.each{ k, v ->
							JsonObject compObject = new JsonObject();
							
							compObject.addProperty("ModuleName", k.toString())
							def lst = v
							statusVal = SUCCESS_STATUS
							
							JsonArray scriptStatusArray = new JsonArray();
							JsonObject scriptStatusNode
							lst.each{
								url = ""
								scriptStatusNode = new JsonObject()
								ExecutionResult exResult = ExecutionResult.findById(it)
								if(!exResult.status.equals(SUCCESS_STATUS)){
									statusVal = FAILURE_STATUS
								}
								scriptStatusNode.addProperty("ScriptName", exResult.script.toString())
								scriptStatusNode.addProperty("ScriptStatus", exResult.status.toString())

								/*JsonArray failedFunArray = new JsonArray()
								List fun = []
								JsonPrimitive el = new JsonPrimitive("fun1");
								JsonPrimitive el2 = new JsonPrimitive("fun2");
								failedFunArray.add(el)
								failedFunArray.add(el2)
								scriptStatusNode.add("FailedFunctions", failedFunArray)*/
								url = appUrl + exResult?.id.toString()
								scriptStatusNode.addProperty("LogUrl", url.toString())
								
								scriptStatusArray.add(scriptStatusNode)
								
							}
							
							newmap[k] = statusVal
							compObject.addProperty("ModuleStatus", statusVal.toString())
							compObject.add("ScriptDetails", scriptStatusArray)
							compArray.add(compObject)
						}
						
						JsonArray systemArray = new JsonArray();
						systemMap.each{ k, v ->
							JsonObject sysObject = new JsonObject();
							
							sysObject.addProperty("ModuleName", k.toString())
							def lst = v
							statusVal = SUCCESS_STATUS
							
							JsonArray scriptStatusArray = new JsonArray();
							JsonObject scriptStatusNode
							lst.each{
								url = ""
								scriptStatusNode = new JsonObject()
								ExecutionResult exResult = ExecutionResult.findById(it)
								if(!exResult.status.equals(SUCCESS_STATUS)){
									statusVal = FAILURE_STATUS
								}
								scriptStatusNode.addProperty("ScriptName", exResult.script.toString())
								scriptStatusNode.addProperty("ScriptStatus", exResult.status.toString())

							/*	JsonArray failedFunArray = new JsonArray()
								List fun = []
								JsonPrimitive el = new JsonPrimitive("fun1");
								JsonPrimitive el2 = new JsonPrimitive("fun2");
								failedFunArray.add(el)
								failedFunArray.add(el2)
								scriptStatusNode.add("FailedFunctions", failedFunArray)*/
								url = appUrl + exResult?.id.toString()
								scriptStatusNode.addProperty("LogUrl", url.toString())
								
								scriptStatusArray.add(scriptStatusNode)
								
							}
							
							newmap[k] = statusVal
							sysObject.addProperty("ModuleStatus", statusVal.toString())
							sysObject.add("ScriptDetails", scriptStatusArray)
							systemArray.add(sysObject)
						}
						def imgName = ""
						if(imageName){
							imgName = imageName
						}

						deviceNode.addProperty("Device",execDevice?.device?.toString())
						deviceNode.addProperty("BoxType",boxType?.toString())
						deviceNode.addProperty("ImageName",imgName?.toString())
						deviceNode.add("ComponentLevelDetails",compArray)
						deviceNode.add("SystemLevelDetails",systemArray)
						
						jsonArray.add(deviceNode)
					}
					executionNode = new JsonObject()
					executionNode.addProperty("ExecutionName",execName)
					executionNode.add("DEVICES", jsonArray)
				}
			
			
			JsonObject paramObject = new JsonObject();
			
			JsonArray paramArray = new JsonArray();
			JsonArray dataArray = new JsonArray();
			dataArray.add(executionNode)
			
			String dataString = dataArray.toString();


			//dataString  = dataString.replaceAll("\"", "")
		
			//    	dataString  = dataString.replaceAll("\"", "\\\\\\\\\\\\\"")
		//	return dataString
			
			/*JsonObject tdkObject = new JsonObject();
			tdkObject.addProperty("name", "TDK_DATA")
			tdkObject.addProperty("value", dataString)
			
			paramArray.add(tdkObject);
			
			paramObject.add("parameter", paramArray);
						
			return paramObject*/
			
			def execTime = executionInstance?.executionTime
			
			Double execTme
			
			try {

				execTme = Double.parseDouble(execTime)
				execTme = execTme * 60000

			} catch (Exception e) {
			}

			JsonObject tdkObject = new JsonObject();
			tdkObject.addProperty("service", "TDK" )
			tdkObject.addProperty("status", executionInstance?.result?.toString() )
			tdkObject.addProperty("started_at", executionStartTime.toString() )
			tdkObject.addProperty("started_by", "RDKPortal/Jenkins" )
			tdkObject.addProperty("duration", execTme.toString())
			tdkObject.add("result", dataArray )
			
			String newDataString = tdkObject.toString()
			newDataString  = newDataString.replaceAll("\"", "\\\\\\\\\\\\\"")
			
			return newDataString
			
		}
	
	/**
	 * Method to execute the script
	 * @param scriptGroupInstance
	 * @param scriptInstance
	 * @param deviceInstance
	 * @param url
	 * @return
	 */
	def String executeScripts(String executionName, String execDeviceId, Script scriptInstance,
			Device deviceInstance, final String url, final String filePath, final String realPath, final String isMultiple ) {
	
			
		String htmlData = ""

		String scriptData = convertScriptFromHTMLToPython(scriptInstance.scriptContent)
		 
		String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES

		def deviceInstance1 = Device.findById(deviceInstance.id,[lock: true])

		def executionInstance = Execution.findByName(executionName,[lock: true])
		def executionId = executionInstance?.id
		Date executionDate = executionInstance?.dateOfExecution
		
		def execStartTime = executionDate?.getTime()

		def executionDeviceInstance = ExecutionDevice.findById(execDeviceId)
		
		def executionResult
		ExecutionResult.withTransaction { resultstatus ->
			try {
				executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDeviceInstance
				executionResult.script = scriptInstance.name
				executionResult.device = deviceInstance.stbName
				executionResult.dateOfExecution = new Date()
				if(! executionResult.save(flush:true)) {
					log.error "Error saving executionResult instance : ${executionResult.errors}"
				}
				resultstatus.flush()
			}
			catch(Throwable th) {
				resultstatus.setRollbackOnly()
			}
		}
		
		String gatewayIp = deviceInstance1?.gatewayIp
		
		
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

		
		def executionResultId = executionResult?.id

		scriptData = scriptData.replace( REPLACE_TOKEN, METHOD_TOKEN + LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath +SINGLE_QUOTES + COMMA_SEPERATOR +
			executionId  + COMMA_SEPERATOR + execDeviceId + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.logTransferPort + COMMA_SEPERATOR + deviceInstance?.statusPort + COMMA_SEPERATOR +
			scriptInstance?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR+ SINGLE_QUOTES + "false" + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + "false" + SINGLE_QUOTES + COMMA_SEPERATOR +
			SINGLE_QUOTES + isMultiple + SINGLE_QUOTES + COMMA_SEPERATOR )//+ gatewayIp + COMMA_SEPERATOR)
		
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
		
		Date executionStartDt = new Date()
		def executionStartTime =  executionStartDt.getTime()
		

		String outData = executeScript( file.getPath(), scriptInstance.executionTime )
		
		
		def logTransferFileName = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDeviceInstance?.id.toString()}"		
		def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${execDeviceId}//${executionResultId}//"
		new File("${realPath}/logs//consolelog//${executionId}//${execDeviceId}//${executionResultId}").mkdirs()
		executescriptService.logTransfer(deviceInstance,logTransferFilePath,logTransferFileName)

		
		outData?.eachLine { line ->
			htmlData += (line + HTML_BR )
		}
		
		file.delete()
		String outputData = htmlData
		
		Date execEndDate = new Date()
		def execEndTime =  execEndDate.getTime()

		def timeDifference = ( execEndTime - executionStartTime  ) / 60000;

		String timeDiff =  String.valueOf(timeDifference)
		
		def resultArray = Execution.executeQuery("select a.executionTime from Execution a where a.name = :exName",[exName: executionName])
		
		BigDecimal myVal1
		if(resultArray[0]){
			myVal1= new BigDecimal (resultArray[0]) + new BigDecimal (timeDiff)
		}
		else{
			myVal1 =  new BigDecimal (timeDiff)
		}
						
		timeDiff =  String.valueOf(myVal1)
	
		
	   /* if(outputData) {
			
			executionService.updateExecutionResults(outputData,executionResultId,executionId, executionDeviceInstance?.id, timeDiff)
			
		   /* Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime where c.id = :execId",
				[newStatus: outputData, newTime: timeDiff, execId: executionId.toLong()])*/
	   // }
		
		if(htmlData.contains(TDK_ERROR)){
			htmlData = htmlData.replaceAll(TDK_ERROR,"")
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
			}
			executionService.updateExecutionResultsError(htmlData,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString(),timeDifference.toString())
			Thread.sleep(5000)
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				"false"
			]
			def resetExecutionData
			try {
				ScriptExecutor scriptExecutor = new ScriptExecutor()
				resetExecutionData = scriptExecutor.executeScript(cmd,1)
			} catch (Exception e) {
				e.printStackTrace()
			}
			Thread.sleep(6000)
		}
		else{
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
				String outputData1 = htmlData
				executionService.updateExecutionResults(outputData1,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString(),timeDifference.toString())
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
						ScriptExecutor scriptExecutor = new ScriptExecutor()
						def resetExecutionData = scriptExecutor.executeScript(cmd,1)
						htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
						executionService.updateExecutionResultsTimeOut(htmlData,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString(),timeDifference.toString())
						Thread.sleep(6000)
				}else{
					try {
						executionService.updateExecutionResultsError(htmlData,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString(),timeDifference.toString())
						Thread.sleep(5000)
						File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
						def absolutePath = layoutFolder.absolutePath
						String[] cmd = [
							PYTHON_COMMAND,
							absolutePath,
							deviceInstance?.stbIp,
							deviceInstance?.agentMonitorPort,
							"false"
						]
						def resetExecutionData
						try {
							ScriptExecutor scriptExecutor = new ScriptExecutor()
							resetExecutionData = scriptExecutor.executeScript(cmd,1)
						} catch (Exception e) {
							e.printStackTrace()
						}
						Thread.sleep(6000)
					} catch (Exception e) {
						e.printStackTrace()
					}
				}
			}
		}
		return htmlData
	}
			
	/**
	 * Method to call the script executor to execute the script
	 * @param executionData
	 * @return
	 */
	public String executeScript(final String executionData, final int executeTime) {
		new ScriptExecutor().execute( getCommand( executionData ),executeTime)
	}
	
	/**
	 * Method to validate script
	 * @param executionData
	 * @return
	 */
	public String validateScript(final String executionData) {
		new ScriptExecutor().validateScript( getCommand( executionData ))
	}
	
	/**
	 * Method to get the python script execution command.
	 * @param command
	 * @return
	 */
	public String getCommand(final String command) {
		String actualCommand = grailsApplication.config.python.execution.path +" "+ command
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
		def afterBr = afterspan.replaceAll(HTML_REPLACEBR, KEY_ENTERNEW_LINE)
		afterBr = afterBr.replaceAll(HTML_LESSTHAN,LESSTHAN);
		afterBr = afterBr.replaceAll(HTML_GREATERTHAN, GREATERTHAN)
		return afterBr;
	}
	
	/**
	 * Removes all span from the script
	 * @param script
	 * @return
	 */
	def removeAllSpan(String script) {
		Matcher m = Pattern.compile(HTML_PATTERN).matcher(script)
		while(m.find()){
			String match = m.group(1);
			script =script.replace(match, "");
		}
		String afterspan =script.replaceAll(HTML_PATTERN_AFTERSPAN, "")
		return afterspan
	}

	/**
	 * Validates whether the boxtype of device is same as that
	 * of the boxtype specified in the script
	 * @param scriptInstance
	 * @param deviceInstance
	 * @return
	 */
	public boolean validateScriptBoxType(final Script scriptInstance, final Device deviceInstance){
		boolean scriptStatus = true
		if(!(scriptInstance.boxTypes.find { it.id == deviceInstance.boxType.id })){
			scriptStatus = false
		}
		return scriptStatus
	}
	
	/**
	 * Validates whether the boxtype of device is same as that
	 * of the boxtype specified in the script
	 * @param scriptInstance
	 * @param deviceInstance
	 * @return
	 */
	public boolean validateBoxTypeOfScript(Script scriptInstance, String boxType){
		boolean scriptStatus = true
		def sId = scriptInstance?.id
		Script.withTransaction {
			def scriptInstance1 = Script.findById(sId)
			if(!(scriptInstance1.boxTypes.find { (it.name).equalsIgnoreCase( boxType ) })){
				scriptStatus = false
			}
		}
		return scriptStatus
	}
	
	
	/**
	 * Method to execute the versiontransfer.py script stored in filestore folder of webapps
	 *
	 * @param filePath
	 * @param executionName
	 * @param stbIp
	 * @return
	 */
	def executeVersionTransferScript(final String realPath, final String filePath, final String executionName, final String stbIp, final String logTransferPort){
		
		def executionInstance = Execution.findByName(executionName)
		String fileContents = new File(filePath+DOUBLE_FWD_SLASH+VERSIONTRANSFER_FILE).text
		
		fileContents = fileContents.replace(IP_ADDRESS, STRING_QUOTES+stbIp+STRING_QUOTES)
		
		fileContents = fileContents.replace(PORT, logTransferPort)
		
		String versionFilePath = "${realPath}//logs//version//${executionInstance?.id}_version.txt"
		fileContents = fileContents.replace(LOCALFILE, STRING_QUOTES+versionFilePath+STRING_QUOTES)
		
		String versionFile = TEMP_VERSIONFILE_NAME
					   
		File versnFile = new File(filePath, versionFile)
		boolean isVersionFileCreated = versnFile.createNewFile()
		if(isVersionFileCreated) {
			versnFile.setExecutable(true, false )
		}
		PrintWriter versnNewPrintWriter = versnFile.newPrintWriter();
		versnNewPrintWriter.print( fileContents )
		versnNewPrintWriter.flush()
				
		executeScript( versnFile.getPath() )
		versnFile.delete()
	}
	
	def String generateResultBasedOnTestRequest(final String caseId, final String callbackUrl, final String filePath, final String url, final String imageName, final String boxType){
		Execution execution
		def status = ""
		def execName
		if(caseId.startsWith("CI_")){
			execution = Execution.findByName(caseId.trim())
		}
		else{
			execution = Execution.find("from Execution as b where b.result=? and b.name like 'CI%' order by b.id desc",['FAILURE'])			
		}
		if(execution){
			execName = execution?.name
			def executionStartTime = System.currentTimeMillis()
			executeCallBackUrl(execName,url,callbackUrl,filePath,executionStartTime,imageName,boxType)
			status = "Done"
		}
		return status		
	}
		

	def thirdPartyJsonResultFromController(final String execName, final String appurl ){
		JsonArray jsonArray = new JsonArray()
		JsonObject compNode
		JsonObject deviceNode
		JsonObject executionNode
		String appUrl = appurl
		String url
		appUrl = appurl + "/execution/getDetailedTestResult?execResId="
		Execution executionInstance = Execution.findByName(execName)
		if(executionInstance){
			ScriptGroup scriptGrp = ScriptGroup.findByName(executionInstance?.scriptGroup)
			def executionResultStatus //= ExecutionResult.findAllByExecutionAndStatusIsNotNull(executionInstance)
			def scriptStatus = null
			def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
			def executionResult //= ExecutionResult.findAllByExecution(executionInstance)

			executionDevice.each{ execDevice ->
				url = ""
				compNode = new JsonObject()
				deviceNode = new JsonObject()
				executionResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
		
					List<ExecutionResult> execResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
					def componentMap = [:].withDefault {[]}
					def systemMap = [:].withDefault {[]}
					execResult.each{ execResObj ->
						Script.withTransaction { scriptRes ->
							Script script = Script.findByName(execResObj?.script)
							if(script.primitiveTest.module.testGroup.groupValue.toString().equals("E2E") ){
								List val1 = systemMap.get(script.primitiveTest.module.toString());
								if(!val1){
									val1 = []
									systemMap.put(script.primitiveTest.module.toString(), val1)
								}
								val1.add(execResObj?.id)
							}
							else{
								List val = componentMap.get(script.primitiveTest.module.toString());
								if(!val){
									val = []
									componentMap.put(script.primitiveTest.module.toString(), val)
								}
								val.add(execResObj?.id)
							}
						}
					}
					def statusVal
					def newmap = [:]
					JsonArray compArray = new JsonArray();
					
					componentMap.each{ k, v ->
						JsonObject compObject = new JsonObject();
						
						compObject.addProperty("ModuleName", k.toString())
						def lst = v
						statusVal = SUCCESS_STATUS
						
						JsonArray scriptStatusArray = new JsonArray();
						JsonObject scriptStatusNode
						lst.each{
							url = ""
							scriptStatusNode = new JsonObject()
							ExecutionResult exResult = ExecutionResult.findById(it)
							if(!exResult.status.equals(SUCCESS_STATUS)){
								statusVal = FAILURE_STATUS
							}
							scriptStatusNode.addProperty("ScriptName", exResult.script.toString())
							scriptStatusNode.addProperty("ScriptStatus", exResult.status.toString())

							url = appUrl + exResult?.id.toString()
							scriptStatusNode.addProperty("LogUrl", url.toString())
							
							scriptStatusArray.add(scriptStatusNode)
							
						}
						
						newmap[k] = statusVal
						compObject.addProperty("ModuleStatus", statusVal.toString())
						compObject.add("ScriptDetails", scriptStatusArray)
						compArray.add(compObject)
					}
					
					JsonArray systemArray = new JsonArray();
					systemMap.each{ k, v ->
						JsonObject sysObject = new JsonObject();
						
						sysObject.addProperty("ModuleName", k.toString())
						def lst = v
						statusVal = SUCCESS_STATUS
						
						JsonArray scriptStatusArray = new JsonArray();
						JsonObject scriptStatusNode
						lst.each{
							url = ""
							scriptStatusNode = new JsonObject()
							ExecutionResult exResult = ExecutionResult.findById(it)
							if(!exResult.status.equals(SUCCESS_STATUS)){
								statusVal = FAILURE_STATUS
							}
							scriptStatusNode.addProperty("ScriptName", exResult.script.toString())
							scriptStatusNode.addProperty("ScriptStatus", exResult.status.toString())

							url = appUrl + exResult?.id.toString()
							scriptStatusNode.addProperty("LogUrl", url.toString())
							
							scriptStatusArray.add(scriptStatusNode)
							
						}
						
						newmap[k] = statusVal
						sysObject.addProperty("ModuleStatus", statusVal.toString())
						sysObject.add("ScriptDetails", scriptStatusArray)
						systemArray.add(sysObject)
					}

					deviceNode.addProperty("Device",execDevice?.device.toString())
					deviceNode.add("ComponentLevelDetails",compArray)
					deviceNode.add("SystemLevelDetails",systemArray)
					jsonArray.add(deviceNode)
				}
				executionNode = new JsonObject()
				executionNode.addProperty("ExecutionName",execName)
				
				String execStatus
				if(executionInstance?.executionStatus){
					execStatus = executionInstance?.executionStatus
				}
				else{
					execStatus = "IN-PROGRESS"
				}
								
				executionNode.addProperty("ExecutionStatus",execStatus.toString())
				executionNode.add("DEVICES", jsonArray)
		}
		return executionNode
	}

}
