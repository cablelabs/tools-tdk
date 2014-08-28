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
import org.quartz.JobExecutionContext

import com.comcast.rdk.*

import javax.servlet.http.HttpServletRequest

import static com.comcast.rdk.Constants.*

import java.util.regex.Pattern

import org.codehaus.groovy.grails.commons.ConfigurationHolder

import rdk.test.tool.DeviceStatusJob

import org.codehaus.groovy.grails.web.json.JSONObject

import grails.converters.JSON

/**
 * Schedular class to schedule script execution for a future date
 * Quartz Schedular
 * @author sreejasuma
 *
 */
class JobSchedulerService implements Job{

	def grailsApplication
	boolean transactional = false

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
		def deviceList = []
		boolean allocated = false
		def deviceInstance //= Device.findById(jobDetails?.device, [lock: true])
		try {
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

			String htmlData = ""
			boolean abortedExecution = false

			def scriptObject
			def scriptName

			DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT);
			Calendar cal = Calendar.getInstance();

			if(devices instanceof String){
				deviceList << devices
				deviceInstance = Device.findById(devices, [lock: true])
				deviceName = deviceInstance?.stbName
			}
			else{
				(devices).each{ deviceid -> deviceList << deviceid }
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
					boolean aborted = false
					deviceId = deviceInstance?.id
					def scriptStatus = true
					def scriptVersionStatus =true
					def scriptId
					String devStatus = ""
					try {
						devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						synchronized (ExecutionController.lock) {
							if(ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
								devStatus = "BUSY"
							}else{
								if((devStatus.equals( Status.FREE.toString() ))){
									if(!ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
										allocated = true
										ExecutionService.deviceAllocatedList.add(deviceInstance?.id)
									}
								}
							}
						}
						
				   }
				   catch(Exception eX){
				   }

			  
					if(scripts){
						if(scripts.size() > 1){
							scriptName = MULTIPLESCRIPT
						}
						else{
							scriptInstance = Script.findById(scripts[0],[lock: true])
							scriptStatus = validateScriptBoxType(scriptInstance,deviceInstance)
							String rdkVersion = getRDKBuildVersion(deviceInstance);
							scriptVersionStatus = validateScriptRDKVersion(scriptInstance,rdkVersion)
							scriptName = scriptInstance?.name
						}
					}else if(scriptGrpId){
						scriptGroupInstance = ScriptGroup.findById(scriptGrpId,[lock: true])
					}
					
					if( devStatus.equals( Status.FREE.toString() )){
						
						if(!ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
							allocated = true
							ExecutionService.deviceAllocatedList.add(deviceInstance?.id)
						}
					
					if(scriptStatus && scriptVersionStatus){
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
									execution.executionStatus = INPROGRESS_STATUS
									execution.dateOfExecution = new Date()//dateFormat.format(cal.getTime())
									execution.groups = jobDetails?.groups
									execution.isBenchMarkEnabled = jobDetails?.isBenchMark?.equals("true")
									execution.isSystemDiagnosticsEnabled = jobDetails?.isSystemDiagnostics?.equals("true")
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
								boolean skipStatus = false
								boolean notApplicable = false

								String rdkVersion = getRDKBuildVersion(deviceInstance);
								scriptGroupInstance.scriptsList.each { script ->

									if(validateScriptBoxType(script,deviceInstance)){
										if(validateScriptRDKVersion(script,rdkVersion)){
											if(script.skip){
												skipStatus = true
												saveSkipStatus(Execution.findByName(execName), executionDevice, script, deviceInstance)
											}else{
												validScriptList << script
											}
										}else{
											notApplicable =true
											String rdkVersionData = ""
											Script.withTransaction {
												def scriptInstance1 = Script.findById(script?.id)
												rdkVersionData = scriptInstance1?.rdkVersions
											}

											String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData

											saveNotApplicableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason)

										}

									}else{
										notApplicable =true
										String boxTypeData = ""

										String deviceBoxType = ""

										Device.withTransaction { deviceBoxType = deviceInstance?.boxType }

										Script.withTransaction {
											def scriptInstance1 = Script.findById(script?.id)
											boxTypeData = scriptInstance1?.boxTypes
										}

										String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
										saveNotApplicableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance, reason)
									}


								}
								scriptGrpSize = validScriptList?.size()

								if((skipStatus || notApplicable )&& scriptGrpSize == 0){
									Execution ex = Execution.findByName(execName)
									if(ex){
										updateExecutionStatus(FAILURE_STATUS, ex?.id)
										updateExecutionDeviceSkipStatus(FAILURE_STATUS, executionDevice?.id)
									}
								}

								Execution ex = Execution.findByName(execName)
								validScriptList.each{ scriptObj ->
									scriptCounter++
									if(scriptCounter == scriptGrpSize){
										isMultiple = "false"
									}
									aborted = ExecutionService.abortList.contains(ex?.id?.toString())
									if(!aborted){
										htmlData = executeScript(execName, executionDevice, scriptObj , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,executionName,isMultiple)
										output.append(htmlData)
										Thread.sleep(6000)
									}
								}

								if(aborted && ExecutionService.abortList.contains(ex?.id?.toString())){
									ExecutionService.abortList.remove(ex?.id?.toString())
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
									String rdkVersion = getRDKBuildVersion(deviceInstance);
									boolean skipStatus =false
									boolean notApplicable =false
									scripts.each { script ->
										scriptInstance = Script.findById(script,[lock: true])
										if(validateScriptBoxType(scriptInstance,deviceInstance)){
											if(validateScriptRDKVersion(scriptInstance,rdkVersion)){
												if(scriptInstance.skip){
													skipStatus = true
													saveSkipStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance)
												}else{
													validScripts << scriptInstance
												}
											}else{
												notApplicable =true
												String rdkVersionData = ""
												Script.withTransaction {
													def scriptInstance1 = Script.findById(scriptInstance?.id)
													rdkVersionData = scriptInstance1?.rdkVersions
												}
	
												String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData
	
												saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason)
	
											}
	
										}else{
											notApplicable =true
											String boxTypeData = ""
	
											String deviceBoxType = ""
	
											Device.withTransaction { deviceBoxType = deviceInstance?.boxType }
	
											Script.withTransaction {
												def scriptInstance1 = Script.findById(scriptInstance?.id)
												boxTypeData = scriptInstance1?.boxTypes
											}
	
											String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
											saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance, reason)
										}
									}
									
									scriptGrpSize = validScripts?.size()
									
									if((skipStatus || notApplicable )&& scriptGrpSize == 0){
									Execution ex = Execution.findByName(execName)
									if(ex){
										updateExecutionStatus(FAILURE_STATUS, ex?.id)
										updateExecutionDeviceSkipStatus(FAILURE_STATUS, executionDevice?.id)
									}
								}
									
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

							Execution executionInstance1 = Execution.findByName(execName)
							if(executionInstance1){
								saveExecutionStatus(aborted, executionInstance1?.id)
							}
							
							Device devInstance1 = Device.findById(device)
							if(ExecutionService.deviceAllocatedList.contains(devInstance1?.id)){
								ExecutionService.deviceAllocatedList.remove(devInstance1?.id)
							}

							if(aborted){
								abortedExecution = true
								resetAgent(deviceInstance)
							}

						}
					}
					else{

						output.append(htmlData)
					}
			   }else{
			   
			   try {
				   Execution execution1 = new Execution()
				   execution1.name = executionName
				   execution1.script = scriptName
				   execution1.device = deviceName
				   execution1.scriptGroup = scriptGroupInstance?.name
				   execution1.result = FAILURE_STATUS
				   execution1.executionStatus = FAILURE_STATUS
				   execution1.dateOfExecution = new Date()
				   execution1.applicationUrl = url
				   execution1.isRerunRequired = jobDetails?.rerun?.equals("true")
				   execution1.isBenchMarkEnabled = jobDetails?.isBenchMark?.equals("true")
				   execution1.isSystemDiagnosticsEnabled = jobDetails?.isSystemDiagnostics?.equals("true")
				   execution1.outputData = "Execution failed due to the unavailability of box"
				   if(! execution1.save(flush:true)) {
					   log.error "Error saving Execution instance : ${execution1.errors}"
				   }
			   }
			   catch(Exception th) {
				   th.printStackTrace()
			   }
			   
			   }

					htmlData = ""
				}

				/**
				 * Re run on failure
				 */
				def executionObj = Execution.findByName(execName)
				def executionDeviceObj = ExecutionDevice.findAllByExecutionAndStatusNotEqual(executionObj, SUCCESS_STATUS)

				if(!abortedExecution && (executionDeviceObj.size() > 0 ) && (jobDetails?.rerun)){
					htmlData = reRunOnFailure(realpath,filePath,url,execName,executionName,jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,jobDetails?.groups)
					output.append(htmlData)
				}

			}

		} catch (Exception e) {
			e.printStackTrace()
		}
		finally{
			deviceList.each{ device ->
				Device devInstance1 = Device.findById(device)
				if(allocated && ExecutionService.deviceAllocatedList.contains(devInstance1?.id)){
					ExecutionService.deviceAllocatedList.remove(devInstance1?.id)
				}
			}			
		}
	}


	public void saveNotApplicableStatus(def executionInstance , def executionDevice , def scriptInstance , def deviceInstance, String reason){
		ExecutionResult.withTransaction { resultstatus ->
			try {
				ExecutionResult executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance.name
				executionResult.device = deviceInstance.stbName
				executionResult.status = Constants.NOT_APPLICABLE_STATUS
				executionResult.executionOutput = "Test not executed . Reason : "+reason
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
			boolean aborted = false
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
								execution.executionStatus = INPROGRESS_STATUS
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
							counter++
							if(counter == resultSize){
								isMultiple = "false"
							}

							if(validateScriptBoxType(scriptInstance,deviceInstance)){
								Execution exec = Execution.findByName(newExecName)
								aborted = ExecutionService.abortList.contains(exec?.id?.toString())
								if(!aborted){
									htmlData = executeScript(newExecName, executionDevice, scriptInstance, deviceInstance, url, filePath, realPath,isBenchMark,isSystemDiagnostics,uniqueExecutionName,isMultiple)
									Thread.sleep(6000)
								}
							}

						}

						if(aborted){
							resetAgent(deviceInstance)
						}
					}

				}
			}
			Execution exec = Execution.findByName(newExecName)
			if(aborted && ExecutionService.abortList.contains(exec?.id?.toString())){
				ExecutionService.abortList.remove(exec?.id?.toString())
			}

			saveExecutionStatus(aborted, exec?.id)


		}
	}

	/**
	 * Method to execute the script to get the device's version details
	 * @param realPath
	 * @param filePath
	 * @param executionName
	 * @param exectionDeviceId
	 * @param stbIp
	 * @param logTransferPort
	 * @return
	 */
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
			executeScriptFile( versnFile.getPath() )
			versnFile.delete()
			
			Device device			
			Device.withTransaction{
				 device = Device.findByStbIp(stbIp)
			}
			
			if(device?.boxType?.type?.equalsIgnoreCase(BOXTYPE_CLIENT)){
				getDeviceDetails(device,logTransferPort,realPath)
			}			
		}
		catch(Exception ex){
		}
	}
	
	/**
	 * Method to call the script executor to execute the script
	 * @param executionData
	 * @return
	 */
	public String executeScriptFile(final String executionData) {
		new ScriptExecutor().execute( getCommand( executionData ),1)
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
		def executionResultId = executionResult?.id
		
		def mocaDeviceList = Device.findAllByStbIpAndMacIdIsNotNull(deviceInstance1?.stbIp)
		
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

		String gatewayIp = deviceInstance1?.gatewayIp

		scriptData = scriptData.replace( REPLACE_TOKEN, METHOD_TOKEN + LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath +SINGLE_QUOTES + COMMA_SEPERATOR +
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
		PrintWriter fileNewPrintWriter = file.newPrintWriter()
		fileNewPrintWriter.print( scriptData )
		fileNewPrintWriter.flush()
		fileNewPrintWriter.close()
		String outData = executeScripts( file.getPath() , scriptInstance.executionTime)
		
		def logTransferFileName = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDevice?.id.toString()}"
		def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"

		new File("${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
		logTransfer(deviceInstance,logTransferFilePath,logTransferFileName)

		file.delete()
		outData?.eachLine { line ->
			htmlData += (line + HTML_BR )
		}
		Date execEndDate = new Date()
		def execEndTime =  execEndDate.getTime()
		def timeDifference = ( execEndTime - execStartTime  ) / 60000;
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
		if(htmlData.contains(TDK_ERROR)){
			htmlData = htmlData.replaceAll(TDK_ERROR,"")
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
			}
			updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,timeDifference.toString())
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
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			Thread.sleep(4000)
		}
		else{
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
				String outputData = htmlData
				updateExecutionResults(outputData,executionResultId,executionId,executionDevice?.id,timeDiff,timeDifference.toString())
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
					def resetExecutionData = scriptExecutor.executeScript(cmd,1)
					htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
					updateExecutionResultsTimeOut(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,timeDifference.toString())
					Thread.sleep(4000)
				}else{
					try {
						updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,timeDifference.toString())
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
						def resetExecutionData = scriptExecutor.executeScript(cmd,1)
						Thread.sleep(4000)
					} catch (Exception e) {
						e.printStackTrace()
					}

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
			htmlData += scriptExecutor.executeScript(cmd,1)
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
			htmlData += scriptExecutor.executeScript(cmd,1)
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
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def logTransfer(def deviceInstance, def logTransferFilePath, def logTransferFileName){
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callConsoleLogTransfer.py").file
		def absolutePath = layoutFolder.absolutePath
		String[] cmd = [
			PYTHON_COMMAND,
			absolutePath,
			deviceInstance?.stbIp,
			deviceInstance?.agentMonitorPort,
			deviceInstance?.logTransferPort,
			"${logTransferFileName}_AgentConsole.log",
			logTransferFilePath			
		]
		ScriptExecutor scriptExecutor = new ScriptExecutor()
		def resetExecutionData = scriptExecutor.executeScript(cmd,1)
		
		Thread.sleep(4000)
	}

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

	def getRDKBuildVersion(Device device){

		def outputData
		def absolutePath
		def boxIp = device?.stbIp
		def port = device?.agentMonitorPort

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callGetRDKVersion.py").file
		absolutePath = layoutFolder.absolutePath

		if(boxIp != null && port != null ){
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				boxIp,
				port
			]

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			outputData = scriptExecutor.executeScript(cmd,1)
		}

		if(outputData){
			outputData = outputData.trim()
		}else{
			outputData = ""
		}

		String rdkVersion = ""
		if(outputData.equals("METHOD_NOT_FOUND") || outputData.equals("AGENT_NOT_FOUND") || outputData.equals("NOT_DEFINED")){
			rdkVersion = "NOT_AVAILABLE"
		}else if(outputData.contains("DOT")){
			rdkVersion = outputData.replace("DOT",".")
		}else if(!outputData.equals("") && !outputData.startsWith("RDK")){
			rdkVersion = "RDK"+outputData.replace("DOT",".")
		}else{
			rdkVersion = outputData
		}

		if(rdkVersion && rdkVersion.contains(" ")){
			rdkVersion.replaceAll(" ", "")
		}

		return rdkVersion
	}

	public boolean validateScriptRDKVersion(final Script scriptInstance, final String rdkVersion){
		boolean scriptStatus = true
		String versionText = rdkVersion
		if(rdkVersion){
			versionText = rdkVersion.trim()
		}
		if(versionText && !(versionText?.equals("NOT_AVAILABLE") || versionText?.equals("NOT_VALID") || versionText?.equals("")) ){
			Script.withTransaction { trns ->
				def scriptInstance1 = Script.findById(scriptInstance?.id)
				if(scriptInstance1?.rdkVersions.size() > 0 && !(scriptInstance1?.rdkVersions?.find {
					it?.buildVersion?.equals(versionText)
				})){
					scriptStatus = false
				}
			}
		}
		return scriptStatus
	}

	public void updateExecutionResults(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId, 
		final String timeDiff, final String singleScriptExecTime){

		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput, c.executionTime = :newTime  where c.id = :execId",
				[newOutput: outputData, newTime: singleScriptExecTime, execId: executionResultId])
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
	public void updateExecutionResultsTimeOut(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId, 
		final def timeDiff, final String singleScriptExecTime){

		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput , c.status = :newStatus, c.executionTime = :newTime  where c.id = :execId",
				[newOutput: outputData, newStatus: "SCRIPT TIME OUT", newTime: singleScriptExecTime, execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.result = :newStatus , c.executionTime = :newTime where c.id = :execId",
				[newStatus: outputData, newStatus: "FAILURE", newTime: timeDiff,  execId: executionId.toLong()])
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
	public void updateExecutionResultsError(final String resultData,final long executionResultId, final long executionId, final long executionDeviceId,
		final String timeDiff, final String singleScriptExecTime){

		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput , c.status = :newStatus, c.executionTime = :newTime  where c.id = :execId",
				[newOutput: resultData, newStatus: "FAILURE", newTime: singleScriptExecTime, execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime, c.result = :newStatus where c.id = :execId",
				[newStatus: resultData, newTime: timeDiff, newStatus: "FAILURE", execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat where c.id = :execDevId",
				[newStat: "FAILURE", execDevId: executionDeviceId.toLong()])

	}

	public void saveSkipStatus(def executionInstance , def executionDevice , def scriptInstance , def deviceInstance){
		ExecutionResult.withTransaction { resultstatus ->
			try {
				ExecutionResult executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance.name
				executionResult.device = deviceInstance.stbName
				executionResult.status = SKIPPED_STATUS
				executionResult.dateOfExecution = new Date()
				executionResult.executionOutput = "Test skipped , Reason :"+scriptInstance.remarks
				if(! executionResult.save(flush:true)) {
					log.error "Error saving executionResult instance : ${executionResult.errors}"
				}
				resultstatus.flush()
			}
			catch(Throwable th) {
				resultstatus.setRollbackOnly()
			}
		}

		try {
			Execution.withTransaction {
				Execution execution = Execution.findById(executionInstance?.id)
				if(!execution.result.equals( FAILURE_STATUS )){
					execution.result = FAILURE_STATUS
					execution.save(flush:true)
				}
			}

			ExecutionDevice.withTransaction {
				ExecutionDevice execDeviceInstance = ExecutionDevice.findById(executionDevice?.id)
				if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
					execDeviceInstance.status = FAILURE_STATUS
					execDeviceInstance.save(flush:true)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	public void updateExecutionStatus(final String status, final long executionId){
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.result = :reslt where c.id = :execId",
				[newStatus: status, reslt: status, execId: executionId.toLong()])
	}

	public void updateExecutionDeviceSkipStatus(final String status, final long executionId){
		ExecutionDevice.withTransaction {
			ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat where c.id = :execDevId",
					[newStat: status, execDevId: executionId])
		}
	}

	/**
	 * Method to save the execution status
	 * @param isAborted
	 * @param exId
	 */
	public void saveExecutionStatus(boolean isAborted, def exId){

		String status = ""
		if(isAborted){
			status = ABORTED_STATUS
		}else{
			status = COMPLETED_STATUS
		}
		try {
			Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus , c.isAborted = :abort where c.id = :execId",
					[newStatus: status, abort: isAborted, execId: exId?.toLong()])

		} catch (Exception e) {
			e.printStackTrace()
		}

	}

	/**
	 * Method to reset the agent status
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
		def resetExecutionData = scriptExecutor.executeScript(cmd,1)
		Thread.sleep(4000)
	}

	/**
	 * Method to execute the script to transfer box parameters to /logs/devicelogs
	 * @param device
	 * @param logTransferPort
	 * @param realPath
	 * @return
	 */
	def getDeviceDetails(Device device, def logTransferPort, def realPath){
		
		new File("${realPath}//logs//devicelogs//${device?.stbName}").mkdirs()

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//filetransfer.py").file
		def absolutePath = layoutFolder.absolutePath
		def filePath = "${realPath}//logs//devicelogs//${device?.stbName}//"
		
		String[] cmd = [
			"python",
			absolutePath,
			device?.stbIp,
			logTransferPort,
			"/opt/TDK/trDetails.log",
			filePath+"${device?.stbName}.txt"
		]

	    ScriptExecutor scriptExecutor = new ScriptExecutor()
	    def outputData = scriptExecutor.executeScript(cmd,1)
		
		parseAndSaveDeviceDetails(device, filePath)		
	}
    
	/**
	 * Parse the file which contains box parameters
	 * @param device
	 * @param filePath
	 * @return
	 */
	def parseAndSaveDeviceDetails(Device device, def filePath){

		try {
			File file = new File(filePath+"${device?.stbName}.txt")

			def map = [:]
			def bootargs = false

			def driversloaded = false
			def driversLoaded = ""

			def partitions = false
			def partition = ""

			def mounts = false
			def mount = ""

			file.eachLine { line ->
				if(line.startsWith("{\"paramList\"")){
					JSONObject userJson = JSON.parse(line)
					userJson.each { id, data ->
						data.each{ val ->

							switch ( val.name.toString().trim() ) {

								case "Device.DeviceInfo.Manufacturer":
									map["Manufacturer"] = val.value.toString()

								case "Device.DeviceInfo.ModelName":
									map["ModelName"] = val.value.toString()

								case "Device.DeviceInfo.SerialNumber":
									map["SerialNumber"] = val.value.toString()

								case "Device.DeviceInfo.HardwareVersion":
									map["HardwareVersion"] = val.value.toString()

								case "Device.DeviceInfo.SoftwareVersion":
									map["SoftwareVersion"] = val.value.toString()

								case "Device.DeviceInfo.ProcessorNumberOfEntries":
									map["NumberOfProcessor"] = val.value.toString()

								case "Device.DeviceInfo.Processor.1.Architecture":
									map["Architecture"] = val.value.toString()

								case "Device.DeviceInfo.UpTime":
									map["UpTime"] = val.value.toString()

								case "Device.DeviceInfo.ProcessStatus.ProcessNumberOfEntries":
									map["NumberOfProcessRunning"] = val.value.toString()

								case "Device.Ethernet.InterfaceNumberOfEntries":
									map["NumberOfInterface"] = val.value.toString()

								case "Device.DeviceInfo.MemoryStatus.Total":
									map["TotalMemory"] = val.value.toString()

								case "Device.DeviceInfo.MemoryStatus.Free":
									map["FreeMemory"] = val.value.toString()

								default:
									log.info("Default")
							}
						}
					}
				}

				if(bootargs){
					map["BootArgs"] = line
					bootargs = false
				}

				if(line.startsWith("#Bootagrs START")){
					bootargs = true
				}

				if(line.startsWith("#Driversloaded END")){
					map["Driversloaded"] = driversLoaded
					driversloaded = false
				}

				if(driversloaded){
					driversLoaded = driversLoaded + line + "<br>"
				}

				if(line.startsWith("#Driversloaded")){
					driversloaded = true
				}

				if(line.startsWith("#Partitions END")){
					map["Partitions"] = partition
					partitions = false
				}

				if(partitions){
					partition = partition + line + "<br>"
				}

				if(line.startsWith("#Partitions START")){
					partitions = true
				}

				if(line.startsWith("#mounts END")){
					map["Mount"] = mount
					mounts = false
				}

				if(mounts){
					mount = mount + line + "<br>"
				}

				if(line.startsWith("#mounts START")){
					mounts = true
				}
			}

			def deviceDetailsList = DeviceDetails.findAllByDevice(device)

			if(deviceDetailsList?.size() > 0){
				DeviceDetails.executeUpdate("delete DeviceDetails d where d.device = :instance1",[instance1:device])
			}

			DeviceDetails deviceDetails = new DeviceDetails()

			map?.each{ k,v ->
				deviceDetails = new DeviceDetails()
				deviceDetails.device = device
				deviceDetails.deviceParameter = k
				deviceDetails.deviceValue = v
				deviceDetails.save(flush:true)
			}

		} catch (Exception e) {
		}

	}
	
}
