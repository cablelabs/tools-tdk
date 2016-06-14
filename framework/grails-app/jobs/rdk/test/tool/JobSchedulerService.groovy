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

import java.io.InputStream;
import java.net.URLConnection;
import java.text.DateFormat
import java.text.SimpleDateFormat
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
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

	static ExecutorService executorService = Executors.newCachedThreadPool()

	static triggers ={}

	/**
	 * Method which is invoked based on the schedule time
	 * @param context
	 */
	public void execute (JobExecutionContext context) {
		def jobName = context.jobDetail.key.name
		def triggerName = context.trigger.key.name

		try {
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
		} catch (Exception e) {
			e.printStackTrace()
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
		List pendingScripts = []
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
			//			ScriptService.getScriptNameFileList(realpath)

			def scriptInstance
			def scriptGroupInstance
			def deviceName

			String htmlData = ""
			boolean abortedExecution = false
			boolean pause = false
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
						eX.printStackTrace()
					}
					if(scripts){
						if(scripts.size() > 1){
							scriptName = MULTIPLESCRIPT
						}
						else{

							def moduleName= ScriptService.scriptMapping.get(scripts[0])

							scriptInstance = getScript(realpath,moduleName, scripts[0])

							scriptStatus = validateScriptBoxTypes(scriptInstance,deviceInstance)
							String rdkVersion = getRDKBuildVersion(deviceInstance);
							scriptVersionStatus = validateScriptRDKVersions(scriptInstance,rdkVersion)
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
								int scriptCnt = 0
								if(scriptGroupInstance?.scriptList?.size() > 0){
									scriptCnt = scriptGroupInstance?.scriptList?.size()
								}// Test case  count includes execution result page while executing multiple scripts.
								else if(scriptName.equals("Multiple Scripts")){
									scriptCnt  = scripts?.size()
								}
									println jobDetails.rerunOnFailure?.equals("true")
								Execution.withTransaction { status ->
									try {
										execution = new Execution()
										execution.name = execName
										execution.script = scriptName
										execution.device = deviceName
										execution.applicationUrl = url
										execution.scriptGroup = scriptGroupInstance?.name
										execution.result = UNDEFINED_STATUS
										execution.executionStatus = INPROGRESS_STATUS
										execution.dateOfExecution = new Date()//dateFormat.format(cal.getTime())
										execution.groups = jobDetails?.groups
										execution.isBenchMarkEnabled = jobDetails?.isBenchMark?.equals("true")
										execution.isSystemDiagnosticsEnabled = jobDetails?.isSystemDiagnostics?.equals("true")
										execution.isStbLogRequired= jobDetails.isStbLogRequired?.equals("true")
										execution.rerunOnFailure = jobDetails.rerunOnFailure?.equals("true")
										execution.scriptCount = scriptCnt
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
								executeVersionTransferScript(realpath, filePath, executionName, executionDevice?.id, deviceInstance.stbName, deviceInstance?.logTransferPort)
								int scriptGrpSize = 0
								int scriptCounter = 0
								def isMultiple = "true"
								if(jobDetails?.scriptGroup){
									scriptGroupInstance = ScriptGroup.findById(jobDetails?.scriptGroup,[lock: true])
									scriptCounter = 0
									List validScriptList = new ArrayList()

									boolean skipStatus = false
									boolean notApplicable = false

									String rdkVersion = getRDKBuildVersion(deviceInstance);
									scriptGroupInstance.scriptList.each { scrpt ->

										def script = getScript(realpath,scrpt?.moduleName, scrpt?.scriptName)

										if(script){
											if(validateScriptBoxTypes(script,deviceInstance)){
												if(validateScriptRDKVersions(script,rdkVersion)){
													if(script.skip.toString().equals("true")){
														skipStatus = true
														saveSkipStatus(Execution.findByName(execName), executionDevice, script, deviceInstance)
													}else{
														validScriptList << script
													}
												}else{
													notApplicable =true
													String rdkVersionData = ""
													rdkVersionData = script?.rdkVersions

													String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData

													saveNotApplicableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason)

												}

											}else{
												notApplicable =true
												String boxTypeData = ""

												String deviceBoxType = ""

												Device.withTransaction { deviceBoxType = deviceInstance?.boxType }

												//										Script.withTransaction {
												//											def scriptInstance1 = Script.findById(script?.id)
												boxTypeData = script?.boxTypes
												//										}

												String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
												saveNotApplicableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance, reason)
											}
										}else{
											String reason = "No script is available with name :"+scrpt?.scriptName+" in module :"+scrpt?.moduleName
											saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, scrpt?.scriptName, deviceInstance,reason)

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
									Properties props = new Properties()
									try {
										// rest call for log transfer starts
										props.load(grailsApplication.parentContext.getResource("/appConfig/logServer.properties").inputStream)
										if(validScriptList.size() > 0){
											if(props.get("logServerUrl")){
												Runnable runnable = new Runnable(){
															public void run(){
																def startStatus = initiateLogTransfer(execName, props.get("logServerUrl"), props.get("logServerAppName"), deviceInstance)
																if(startStatus){
																	println "Log transfer job created for $execName"
																}
																else{
																	println "Cannot create Log transfer job for $execName"
																}
															}
														}
												executorService.execute(runnable);
											}
										}
									} catch (Exception e) {
										e.printStackTrace()
									}

									validScriptList.each{ scriptObj ->
										scriptCounter++
										if(scriptCounter == scriptGrpSize){
											isMultiple = "false"
										}
										aborted = ExecutionService.abortList.contains(ex?.id?.toString())

										String deviceStatus = ""
										if(!pause && !aborted){
											try {
												deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
												/*Thread.start{
												 deviceStatusService.updateDeviceStatus(deviceInstance, devStatus)
												 }*/
												if(deviceStatus.equals(Status.HANG.toString())){
													resetAgent(deviceInstance, TRUE)
													Thread.sleep(6000)
													deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
												}
											}
											catch(Exception eX){
											}
										}


										if(!aborted && !(deviceStatus.equals(Status.NOT_FOUND.toString()) || deviceStatus.equals(Status.HANG.toString())) && !pause){
											htmlData = executeScript(execName, executionDevice, scriptObj , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark,jobDetails?.isSystemDiagnostics,jobDetails?.isStbLogRequired,executionName,isMultiple)
											output.append(htmlData)
											Thread.sleep(6000)
										}else{

											if(!aborted && (deviceStatus.equals(Status.NOT_FOUND.toString()) ||  deviceStatus.equals(Status.HANG.toString()))){
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

									try {
										if(validScriptList.size() > 0){
											if(props.get("logServerUrl")){
												Runnable runnable = new Runnable(){
															void run() {
																def status = stopLogTransfer(execName, props.get("logServerUrl"), props.get("logServerAppName"))
																if(status){
																	println "Stopped Log transfer job for $execName"
																}
																else{
																	println "Log transfer job scheduled for $execName failed to stop"
																}
															};
														}
												executorService.execute(runnable);
											}
										}
									} catch (Exception e) {
										e.printStackTrace()
									}

									if(aborted && ExecutionService.abortList.contains(ex?.id?.toString())){
										ExecutionService.abortList.remove(ex?.id?.toString())
									}
									if(!aborted && pause && pendingScripts.size() > 0 ){
										def exeInstance = Execution.findByName(execName)
										savePausedExecutionStatus(exeInstance?.id)
										saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
									}
								}
								else if(scripts){

									if(scripts instanceof String){
										//									scriptInstance = Script.findById(scripts,[lock: true])
										//									scriptId = scriptInstance?.id
										def moduleName= ScriptService.scriptMapping.get(scripts)
										scriptInstance = getScript(realpath,moduleName, scripts)

										isMultiple = "false"
										htmlData = executeScript(execName, executionDevice, scriptInstance , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,jobDetails?.isStbLogRequired,executionName,isMultiple, 	 jobDetails.groups.toString())
										output.append(htmlData)
									}
									else{
										scriptCounter = 0
										List<Script> validScripts = new ArrayList<Script>()
										String rdkVersion = getRDKBuildVersion(deviceInstance);
										boolean skipStatus =false
										boolean notApplicable =false
										scripts.each { script ->

											def moduleName= ScriptService.scriptMapping.get(script)
											scriptInstance = getScript(realpath,moduleName, script)

											//										scriptInstance = Script.findById(script,[lock: true])
											if(validateScriptBoxTypes(scriptInstance,deviceInstance)){
												if(validateScriptRDKVersions(scriptInstance,rdkVersion)){
													if(scriptInstance.skip.toString().equals("true")){
														skipStatus = true
														saveSkipStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance)
													}else{
														validScripts << scriptInstance
													}
												}else{
													notApplicable =true
													String rdkVersionData = ""
													//												Script.withTransaction {
													//													def scriptInstance1 = Script.findById(scriptInstance?.id)
													rdkVersionData = scriptInstance?.rdkVersions
													//												}

													String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData

													saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason)

												}

											}else{
												notApplicable =true
												String boxTypeData = ""

												String deviceBoxType = ""

												Device.withTransaction { deviceBoxType = deviceInstance?.boxType }

												//											Script.withTransaction {
												//												def scriptInstance1 = Script.findById(scriptInstance?.id)
												boxTypeData = scriptInstance?.boxTypes
												//											}

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
										Execution ex = Execution.findByName(execName)
										String deviceStatus
										def exeId = ex?.id
										validScripts.each{ script ->
											scriptCounter++
											if(scriptCounter == scriptGrpSize){
												isMultiple = "false"
											}
											aborted = ExecutionService.abortList.contains(exeId?.toString())
											if(!aborted && !pause)
											{
												try{
													deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
												}catch(Exception e){
													e.printStackTrace()
												}
											}
											if(!aborted && !(deviceStatus.equals(Status.NOT_FOUND.toString()) || deviceStatus.equals(Status.HANG.toString()))){
												htmlData = executeScript(execName, executionDevice, script , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,jobDetails?.isStbLogRequired, executionName,isMultiple, )
											}else {
												if(!aborted && deviceStatus.equals(Status.NOT_FOUND.toString())){
													pause = true
												}
												if(!aborted && pause){
													try{
														pendingScripts.add(script)
														def execInstance
														Execution.withTransaction {
															def execInstance1 = Execution.findByName(execName)
															execInstance = execInstance1
														}
														def scriptInstanceObj
														scriptInstanceObj = script
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

													}catch(Exception e){
														e.printStackTrace()
													}
												}

											}
											if(aborted && ExecutionService.abortList.contains(exeId?.toString())){
												ExecutionService.abortList.remove(ex?.toString())
											}
											if(!aborted && pause && pendingScripts.size() > 0 ){
												def exeInstance = Execution.findByName(execName)
												savePausedExecutionStatus(exeInstance?.id)
												saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
											}
											output.append(htmlData)
											Thread.sleep(6000)
										}
									}
								}

								Execution executionInstance1 = Execution.findByName(execName)
								if(!pause && executionInstance1){
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
							Execution.withTransaction{
								def execution1 = new Execution()
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
								execution1.isStbLogRequired= jobDetails.isStbLogRequired?.equals("true")
								execution1.rerunOnFailure = jobDetails.rerunOnFailure?.equals("true") 
								execution1.outputData = "Execution failed due to the unavailability of box"
								if(! execution1.save(flush:true)) {
									log.error "Error saving Execution instance : ${execution1.errors}"
								}
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
				
				if(!abortedExecution && !pause && (executionDeviceObj.size() > 0 ) && (jobDetails?.rerun?.toString()?.equals("true"))){
					try{
						htmlData = reRunOnFailure(realpath?.toString(),filePath?.toString(),url?.toString(),execName?.toString(),executionName?.toString(),jobDetails?.isBenchMark?.toString(), jobDetails?.isSystemDiagnostics?.toString(),jobDetails?.isStbLogRequired?.toString(),jobDetails?.rerunOnFailure?.toString(),jobDetails.rerun?.toString() )
					}catch(Exception e){
					println e.getMessage()
					e.printStackTrace()
					}
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
	//public static volatile Object  lock = new Object()
	def reRunOnFailure(final String realPath, final String filePath, String url, final String execName,final String uniqueExecutionName,
			final String isBenchMark, final String isSystemDiagnostics,final String islogReqd,  final String rerunOnFailure, final String rerun){
		boolean pause= false
		List pendingScripts =[]
		Execution executionInstance = Execution.findByName(execName)
		def resultArray = Execution.executeQuery("select a.result from Execution a where a.name = :exName",[exName: execName])
		def result = resultArray[0]
		def newExecName
		def execution
		Execution rerunExecutionInstance
		def executionSaveStatus = true
		if(result != SUCCESS_STATUS){
			def scriptName
			def scriptGroupInstance = ScriptGroup.findByName(executionInstance?.scriptGroup)			/**
			 * Get all devices for execution
			 */
			def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
			int cnt = 0
			boolean aborted = false
			executionDeviceList.each{ execDeviceInstance ->
				Device deviceInstance = Device.findByStbName(execDeviceInstance?.device)
				boolean allocated = false
				if(execDeviceInstance.status != SUCCESS_STATUS){
					String status1 = ""
					try {
						status1 = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						if(ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
							status1 = "BUSY"
						}else{
							if((status1.equals( Status.FREE.toString() ))){
								if(!ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
									allocated = true
									ExecutionService.deviceAllocatedList.add(deviceInstance?.id)
									Thread.start{
										DeviceStatusService?.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
									}
								}
							}
						}

					}
					catch(Exception eX){
						println  " ERROR "+ eX.printStackTrace()
					}
					if(cnt == 0){
						newExecName = execName + RERUN
						scriptName = executionInstance?.script
						def deviceName = deviceInstance?.stbName
						if(executionDeviceList.size() > 1){
							deviceName = MULTIPLE
						}

						int scriptCnt = 0
						ScriptGroup.withTransaction {
							def scriptGroupInstance1 = ScriptGroup.get(scriptGroupInstance?.id)
							if(scriptGroupInstance1?.scriptList?.size() > 0){
								scriptCnt = scriptGroupInstance1?.scriptList?.size()
							}
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
								//execution.groups = groups
								execution.applicationUrl = url
								execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals("true")
								execution.isBenchMarkEnabled = isBenchMark?.equals("true")
								execution.isStbLogRequired = islogReqd?.equals("true")
								execution?.rerunOnFailure = rerunOnFailure?.equals("true")
								execution.isRerunRequired = rerun?.equals("true")
								execution.scriptCount = scriptCnt
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
						executeVersionTransferScript(realPath, filePath, newExecName, executionDevice?.id, deviceInstance.stbName, deviceInstance?.logTransferPort)
						def executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(executionInstance,execDeviceInstance,SUCCESS_STATUS)
						def scriptInstance
						def htmlData
						def resultSize = executionResultList.size()
						int counter = 0
						def isMultiple = "true"
						Properties props = new Properties()
						try {
							props.load(grailsApplication.parentContext.getResource("/appConfig/logServer.properties").inputStream)
							// initiating log transfer
							if(executionResultList.size() > 0){
								if(props.get("logServerUrl")){
									Runnable runnable = new Runnable(){
												public void run(){
													def startStatus = initiateLogTransfer(newExecName, props.get("logServerUrl"), props.get("logServerAppName"), deviceInstance)
													if(startStatus){
														println "Log transfer job created for $execName"
													}
													else{
														println "Cannot create Log transfer job for $execName"
													}
												}
											}
									executorService.execute(runnable);
								}
							}
						} catch (Exception e) {
							e.printStackTrace()
						}
						executionResultList.each{ executionResult ->
							def scriptFile = ScriptFile.findByScriptName(executionResult?.script)
							scriptInstance = getScript(realPath,scriptFile?.moduleName,scriptFile?.scriptName)
							counter++
							if(counter == resultSize){
								isMultiple = "false"
							}
							def deviceStatus = " "
							try{
								deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
							}catch (Exception e){
								e.getMessage()
							}
							if(validateScriptBoxTypes(scriptInstance,deviceInstance)){
								Execution exec = Execution.findByName(newExecName)
								aborted = ExecutionService.abortList?.toString().contains(exec?.id?.toString())
								if(!aborted && !(deviceStatus?.toString().equals(Status.NOT_FOUND.toString()) || deviceStatus?.toString().equals(Status.HANG.toString())) && !pause){
									htmlData = executeScript(newExecName, executionDevice, scriptInstance, deviceInstance, url, filePath, realPath,isBenchMark,isSystemDiagnostics,islogReqd,uniqueExecutionName,isMultiple)

								}else{
									if(!aborted && (deviceStatus?.equals(Status.NOT_FOUND.toString()) ||  deviceStatus?.equals(Status.HANG.toString()))){
										pause = true
									}
									if(!aborted && pause) {
										try {
											pendingScripts.add(scriptInstance)
											def execInstance
											Execution.withTransaction {
												def execInstance1 = Execution.findByName(newExecName)
												execInstance = execInstance1
											}
											def scriptInstanceObj
											scriptInstanceObj = scriptInstance
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
													def executionResult1 = new ExecutionResult()
													executionResult1.execution = execInstance
													executionResult1.executionDevice = executionDevice1
													executionResult1.script = scriptInstanceObj?.name
													executionResult1.device = deviceInstanceObj?.stbName
													executionResult1.execDevice = null
													executionResult1.deviceIdString = deviceInstanceObj?.id?.toString()
													executionResult1.status = PENDING
													executionResult1.dateOfExecution = new Date()
													if(! executionResult1.save(flush:true)) {
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
						}
						// stopping log transfer
						try {
							if(executionResultList.size() > 0){
								if(props.get("logServerUrl")){
									Runnable runnable = new Runnable(){
												void run() {
													def status = stopLogTransfer(newExecName, props.get("logServerUrl"), props.get("logServerAppName"))
													if(status){
														println "Stopped Log transfer job for $execName"
													}
													else {
														println "Log transfer job scheduled for $execName failed to stop"
													}
												};
											}
									executorService.execute(runnable);
								}
							}
						} catch (Exception e) {
							e.printStackTrace()
						}
						Execution exec = Execution.findByName(newExecName)
						if(aborted && ExecutionService.abortList.contains(exec?.id?.toString())){
							saveExecutionStatus(aborted, exec?.id)
							ExecutionService.abortList.remove(exec?.id?.toString())
						}
						if(!aborted && pause && pendingScripts.size() > 0 ){
							savePausedExecutionStatus(exec?.id)
							saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
						}
						if(!aborted && !pause ){
							saveExecutionStatus(aborted, exec?.id)
						}			
					}
				}
				if(allocated && ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
					ExecutionService.deviceAllocatedList.remove(deviceInstance?.id)
				}
			}
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
	def executeVersionTransferScript(final String realPath, final String filePath, final String executionName, def exectionDeviceId, final String stbName, final String logTransferPort){
		try{
			def executionInstance = Execution.findByName(executionName)
			/*String fileContents = new File(filePath+DOUBLE_FWD_SLASH+VERSIONTRANSFER_FILE).text

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
			versnFile.delete()*/

			Device device
			Device.withTransaction{
				device = Device.findByStbName(stbName)
			}
			String versionFileName = "${executionInstance?.id}_${exectionDeviceId?.toString()}_version.txt"
			def versionFilePath = "${realPath}//logs//version//${executionInstance?.id}//${exectionDeviceId?.toString()}"
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//filetransfer.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				device.stbIp,
				device.agentMonitorPort,
				"/version.txt",
				versionFileName
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def outputData = scriptExecutor.executeScript(cmd,1)
			copyVersionLogsIntoDir(realPath, versionFilePath, executionInstance?.id, exectionDeviceId?.toString())
			
		
			if(device?.boxType?.type?.equalsIgnoreCase(BOXTYPE_CLIENT)){
				getDeviceDetails(device,device.agentMonitorPort,realPath)
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

	def String executeScript(final String executionName, final ExecutionDevice executionDevice, final def scriptInstance,
			final Device deviceInstance, final String url, final String filePath, final String realPath, final String isBenchMark, final String isSystemDiagnostics,final String isLogReqd,final String uniqueExecutionName,final String isMultiple) {
		String htmlData = ""

		String scriptData = convertScriptFromHTMLToPython(scriptInstance.scriptContent)

		String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES

		//		Script scriptInstance1 = Script.findById(scriptInstance.id,[lock: true])
		//		scriptInstance1.status = Status.ALLOCATED
		//		scriptInstance1.save(flush:true)

		Device deviceInstance1 = Device.findById(deviceInstance.id,[lock: true])

		def executionInstance = Execution.findByName(executionName,[lock: true])
		def executionId = executionInstance?.id
		Date executionDate = executionInstance?.dateOfExecution

		//def execStartTime = executionDate?.getTime()
		Date executionStartDt = new Date()
		def execStartTime =  executionStartDt.getTime()


		def executionResult

		ExecutionResult.withTransaction { resultstatus ->
			try {
				executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance.name
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
		String logFilePath = realPath?.toString()+"/logs/logs/" 
		def sFile = ScriptFile.findByScriptNameAndModuleName(scriptInstance?.name,scriptInstance?.primitiveTest?.module?.name)
		scriptData = scriptData.replace( REPLACE_TOKEN, METHOD_TOKEN + LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES +logFilePath+SINGLE_QUOTES + COMMA_SEPERATOR +
				executionId  + COMMA_SEPERATOR + executionDevice?.id + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.agentMonitorPort + COMMA_SEPERATOR + deviceInstance1?.statusPort + COMMA_SEPERATOR +
				sFile?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR + SINGLE_QUOTES + isBenchMark + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + isSystemDiagnostics + SINGLE_QUOTES + COMMA_SEPERATOR +
				SINGLE_QUOTES + isMultiple + SINGLE_QUOTES + COMMA_SEPERATOR)// + gatewayIp + COMMA_SEPERATOR)

		
		/*scriptData = scriptData.replace( REPLACE_TOKEN, METHOD_TOKEN + LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath + SINGLE_QUOTES  + COMMA_SEPERATOR +
			executionId  + COMMA_SEPERATOR + executionDevice?.id + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.logTransferPort + COMMA_SEPERATOR + deviceInstance1?.statusPort + COMMA_SEPERATOR +
			sFile?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR + SINGLE_QUOTES + isBenchMark + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + isSystemDiagnostics + SINGLE_QUOTES + COMMA_SEPERATOR +
			SINGLE_QUOTES + isMultiple + SINGLE_QUOTES + COMMA_SEPERATOR)// + gatewayIp + COMMA_SEPERATOR)
*/		scriptData	 = scriptData + "\nprint \"SCRIPTEND#!@~\";"

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
		String outData = executeScripts( file.getPath() , execTime,executionName)

		//def logTransferFileName = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDevice?.id.toString()}"
		def logTransferFileName = "${executionId}_${executionDevice?.id}_${executionResultId}_AgentConsoleLog.txt"
		def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"
		//new File("${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
		logTransfer(deviceInstance,logTransferFilePath,logTransferFileName, realPath, executionId,executionDevice?.id,executionResultId  )

		file.delete()		
		// TFTP transfer --->>>
		def logPath = "${realPath}/logs//${executionId}//${executionDevice?.id}//${executionResultId}//"
		copyLogsIntoDir(realPath,logPath ,executionId,executionDevice?.id, executionResultId)
		
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
		String singleScriptExecTime = String.valueOf(timeDifference)

		if(ExecutionService.abortList.contains(executionInstance?.id?.toString())){
			resetAgent(deviceInstance,TRUE)
		}else if(htmlData.contains(TDK_ERROR)){
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
				"true"
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
			Thread.sleep(4000)
		}else if(htmlData.contains("Pre-Condition not met")){
			if(htmlData.contains(KEY_SCRIPTEND)){
				htmlData = htmlData.replaceAll(KEY_SCRIPTEND,"")
			}
			updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
		}
		else{
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
				String outputData = htmlData
				updateExecutionResults(outputData,executionResultId,executionId,executionDevice?.id,timeDiff,timeDifference.toString())
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
						"true"
					]
					ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
					def resetExecutionData = scriptExecutor.executeScript(cmd,1)
					callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
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
						callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
						Thread.sleep(4000)
					} catch (Exception e) {
						e.printStackTrace()
					}

				}
			}
		}

		String performanceFilePath
		String performanceFileName 
		
		if(isBenchMark.equals("true") || isSystemDiagnostics.equals("true")){
			//performanceFileName = "${executionId}_${executionDevice?.id}_${executionResultId}_performanceFile.txt"
			performanceFileName =performanceFileName = "${executionId}_${executionDevice?.id}_${executionResultId}"
			//new File("${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
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
				deviceInstance?.agentMonitorPort,
				"PerformanceBenchMarking",
				performanceFileName // fileName				
			]
			
			ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
			htmlData += scriptExecutor.executeScript(cmd,1)
			copyPerformanceLogIntoDir(realPath, performanceFilePath,executionId,executionDevice?.id, executionResultId)	
		}
		if(isSystemDiagnostics.equals("true")){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				deviceInstance?.agentMonitorPort,
				"PerformanceSystemDiagnostics",
				performanceFileName				
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
			htmlData += scriptExecutor.executeScript(cmd,1)
			copyPerformanceLogIntoDir(realPath, performanceFilePath,executionId,executionDevice?.id, executionResultId)			
		}
		//def logTransferFileName1 = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDevice?.id.toString()}"
		def logTransferFileName1 = "${executionId}_${executionDevice?.id}_${executionResultId}_AgentConsoleLog.txt"
		def logTransferFilePath1 = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"

		new File("${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
		logTransfer1(deviceInstance,logTransferFilePath1,logTransferFileName1,realPath,executionId,executionDevice?.id, executionResultId)
		if(isLogReqd?.toString()?.equals("true")){
			transferSTBLog(scriptInstance?.primitiveTest?.module?.name, deviceInstance,""+executionId,""+executionDevice?.id,""+executionResultId, realPath)
		}
		return htmlData
	}
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def logTransfer1(def deviceInstance, def logTransferFilePath, def logTransferFileName, def realPath , def executionId, def executionDeviceId , def executionResultId){
		Thread.sleep(4000)
		try{
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callConsoleLogTransfer.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				"AgentConsole.log",
				logTransferFileName // File Name 				
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
		copyAgentconsoleLogIntoDir(realPath,logTransferFilePath,executionId,executionDeviceId,executionResultId  )
			Thread.sleep(4000)
		}
		catch(Exception e){
		}
	}
	/**
	 * Function for transfer the open sourse logs from "tftp server
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	def copyLogsIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId , def executionResultId ){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					if(!(file?.toString()?.contains("version.txt") || file.toString()?.contains("benchmark.log") || file.toString()?.contains("memused.log") || file.toString()?.contains("cpu.log") || file?.toString()?.contains("AgentConsoleLog.log"))){
						def logFileName =  file?.getName()?.split("_")
						if (file?.isFile() && logFileName.length >= 3 ) {
						if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString()) && executionResultId?.toString()?.equals(logFileName[2]?.toString())){
								String fileName = file.getName()
								if(fileName.toString().contains("\$:")){
									fileName = fileName.replaceAll('\\$:',"Undefined")
								}
								if(fileName.startsWith( logFileName[0] )){
									fileName = fileName.replaceFirst( logFileName[0]+UNDERSCORE+logFileName[1]+UNDERSCORE+logFileName[2]+UNDERSCORE, "" )
									fileName= logFileName[0]+UNDERSCORE+fileName
									new File(logTransferFilePath?.toString()).mkdirs()
									File logTransferPath  = new File(logTransferFilePath)
									if(file.exists()){
										boolean fileMoved = file.renameTo(new File(logTransferPath, fileName.trim()));
									}
								}
							}
						}
					}
				}
			}
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}
	
	
	
	

	/**
	 * Function for transfer stb logs from TM 
	 * @param moduleName
	 * @param dev
	 * @param execId
	 * @param execDeviceId
	 * @param execResultId
	 * @param realPath
	 * @return
	 */
	def transferSTBLog(def moduleName , def dev,def execId, def execDeviceId,def execResultId, def realPath){
		try {
			def module
			Module.withTransaction {
				module = Module.findByName(moduleName)
			}
			def destFolder = grailsApplication.parentContext.getResource("//logs//stblogs//execId_logdata.txt").file
			def destPath = destFolder.absolutePath
			def filePath = destPath.replace("execId_logdata.txt", "${execId}//${execDeviceId}//${execResultId}")
			def directoryPath =  "${execId}_${execDeviceId}_${execResultId}"
			def stbFilePath = "${realPath}//logs//stblogs//${execId}//${execDeviceId}//${execResultId}//"
			module?.stbLogFiles?.each{ name ->
				File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//filetransfer.py").file

				File fileStore = grailsApplication.parentContext.getResource("//fileStore//").file
				def fileStorePath = fileStore.absolutePath

				def absolutePath = layoutFolder.absolutePath
				String fName = name?.replaceAll("//", "_")
				fName = fName?.replaceAll("/", "_")
				
				if((absolutePath) && !(absolutePath.isEmpty())){
					String[] cmd = [
						"python",
						absolutePath,
						dev?.stbIp,
						dev?.agentMonitorPort,  // TFTP change
						name,
						directoryPath+"_"+fName // fileName
					]
					try {
						
						ScriptExecutor scriptExecutor = new ScriptExecutor()
						def outputData = scriptExecutor.executeScript(cmd,1)
						copyStbLogsIntoDir(realPath,stbFilePath,execId, execDeviceId,execResultId )
					}catch (Exception e) {
						e.printStackTrace()
					}
				}

			}
		} catch (Exception e) {
		}
	}
	/**
	 *  Function for move the performance realted like bench mark , cpu usage, meminfo and agent console log transfer
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	
	def copyAgentconsoleLogIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId , def executionResultId){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					if(file.toString()?.contains("AgentConsoleLog.txt")){
						def logFileName =  file.getName().split("_")
						if(logFileName?.length >= 3){
						if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString()) && executionResultId?.toString()?.equals(logFileName[2]?.toString())){
								new File(logTransferFilePath?.toString()).mkdirs()
								File logTransferPath  = new File(logTransferFilePath)
								if(file.exists()){
									boolean fileMoved = file.renameTo(new File(logTransferPath, logFileName.last()));
								}
							}
						}
					}
				}
			}
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}
	/**
	 * Function For Tranfer the performance related file using tftp
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	
	def copyPerformanceLogIntoDir(def realPath, def logTransferFilePath  , def executionId, def executionDeviceId , def executionResultId){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"

			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					if(file.toString()?.contains("benchmark.log") || file.toString()?.contains("memused.log") || file.toString()?.contains("cpu.log")){
						def logFileName =  file.getName().split("_")
						if(logFileName?.length >= 3){
						if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString()) && executionResultId?.toString()?.equals(logFileName[2]?.toString())){
								
							new File(logTransferFilePath?.toString()).mkdirs()
							File logTransferPath  = new File(logTransferFilePath)
							if(file.exists()){
								boolean fileMoved = file.renameTo(new File(logTransferPath, logFileName.last()));
							}
							}
						}
					}
				}
			}
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}
	
	/**
	 * Function for version.txt file transfer 
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	
	def copyVersionLogsIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId ){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					if(file?.toString().contains("version.txt")){
						def logFileName =  file.getName().split("_")
						if(logFileName?.length > 0){
							if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString())){
							def  versionFileName = logFileName[1]+"_"+logFileName.last()
							new File(logTransferFilePath?.toString()).mkdirs()
							File logTransferPath  = new File(logTransferFilePath)
							if(file.exists()){
								boolean fileMoved = file.renameTo(new File(logTransferPath, versionFileName));
							}
						}
						}
					}
				}
			}
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}
	
	/**
	 * To copy   the stb files in to perticular dir using tftp 
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	def copyStbLogsIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId , def executionResultId ){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					if(!(file?.toString()?.contains("version.txt") || file.toString()?.contains("benchmark.log") || file.toString()?.contains("memused.log") || file.toString()?.contains("cpu.log") || file?.toString()?.contains("AgentConsoleLog.log"))){
					def logFileName =  file.getName().split("_")
					if(logFileName?.length >= 3){
						if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString()) && executionResultId?.toString()?.equals(logFileName[2]?.toString())){
							def fName = file.getName()
							fName = fName?.replaceFirst(logFileName[0]+UNDERSCORE+logFileName[1]+UNDERSCORE+logFileName[2]+UNDERSCORE, "" )
							new File(logTransferFilePath?.toString()).mkdirs()
							File logTransferPath  = new File(logTransferFilePath)
							if(file.exists()){
								boolean fileMoved = file.renameTo(new File(logTransferPath,fName.trim()));
							}
						}
					}
					}
				}
			}
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}



	/**
	 * Method to call the script executor to execute the script
	 aram executionData
	 * @return
	 */
	public String executeScripts(final String executionData, int execTime,String executionName) {

		//		def output = new ScriptExecutor().execute( getCommand( executionData ), execTime)
		def output =  new ScriptExecutor().execute( getCommand( executionData ), execTime,executionName,ExecutionService?.executionProcessMap)
		return output
	}

	/**
	 * Method to check whether the agent reset failed. If the agent reset failed it will request to reboot the box.
	 * @param output
	 * @param device
	 * @return
	 */
	def callRebootOnAgentResetFailure(String output,Device device){
		if(output?.contains("Failed to reset agent") || output?.contains("Unable to reach agent")){
			rebootBox(device)
		}
	}
	/**
	 * Method to reboot the box by invoking the python script.
	 * @param deviceInstance
	 * @return
	 */
	def rebootBox(Device deviceInstance ){
		try {
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callRebootOnCrash.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetData = scriptExecutor.executeScript(cmd,1)
			Thread.sleep(10000)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def logTransfer(def deviceInstance, def logTransferFilePath, def logTransferFileName , def realPath , def executionId, def executionDeviceId , def executionResultId){
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callConsoleLogTransfer.py").file
		def absolutePath = layoutFolder.absolutePath
		String[] cmd = [
			PYTHON_COMMAND,
			absolutePath,
			deviceInstance?.stbIp,
			deviceInstance?.agentMonitorPort,
			"AgentConsole.log",
			logTransferFileName
			//logTransferFilePath
		]
		ScriptExecutor scriptExecutor = new ScriptExecutor()
		def resetExecutionData = scriptExecutor.executeScript(cmd,1)
		copyAgentconsoleLogIntoDir(realPath,logTransferFilePath,executionId,executionDeviceId,executionResultId  )
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
		callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		Thread.sleep(4000)
	}

	def resetAgent(def deviceInstance,def type){

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
		def absolutePath = layoutFolder.absolutePath
		String[] cmd = [
			PYTHON_COMMAND,
			absolutePath,
			deviceInstance?.stbIp,
			deviceInstance?.agentMonitorPort,
			type
		]
		ScriptExecutor scriptExecutor = new ScriptExecutor()
		def resetExecutionData = scriptExecutor.executeScript(cmd,1)
		callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
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
		try {
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//filetransfer.py").file
		def absolutePath = layoutFolder.absolutePath
		def filePath = "${realPath}//logs//devicelogs//${device?.stbName}//"
		String[] cmd = [
			"python",
			absolutePath,
			device?.stbIp,
			device?.agentMonitorPort,
			"/version.txt",
			"${device?.stbName}"+"_"+"${device?.stbName}.txt"
		]
		ScriptExecutor scriptExecutor = new ScriptExecutor()
		def outputData = scriptExecutor.executeScript(cmd,1)
		copyDeviceLogIntoDir(realPath,filePath)
		parseAndSaveDeviceDetails(device, filePath)
		} catch (Exception e) {
			e.printStackTrace()
		}
	
	}
	/**
	 * Copy the device logs file into devicelog directory using TFTP server.
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	def copyDeviceLogIntoDir(def realPath, def logTransferFilePath){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					
					def logFileName =  file.getName().split("_")
					if(logFileName?.length > 0){
					new File(logTransferFilePath?.toString()).mkdirs()
					File logTransferPath  = new File(logTransferFilePath)
					if(file.exists()){
						boolean fileMoved = file.renameTo(new File(logTransferPath, logFileName.last()));
						}
					}
				}
			}
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
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

	public boolean validateScriptRDKVersions(final Map script, final String rdkVersion){
		boolean scriptStatus = true
		String versionText = rdkVersion
		if(rdkVersion){
			versionText = rdkVersion.trim()
		}
		if(versionText && !(versionText?.equals("NOT_AVAILABLE") || versionText?.equals("NOT_VALID") || versionText?.equals("")) ){
			Script.withTransaction { trns ->
				if(script?.rdkVersions?.size() > 0 && !(script?.rdkVersions?.find {
					it?.buildVersion?.equals(versionText)
				})){
					scriptStatus = false
				}
			}
		}
		return scriptStatus
	}

	public boolean validateScriptBoxTypes(final Map script, final Device deviceInstance){
		boolean scriptStatus = true
		Script.withTransaction { trns ->
			def deviceInstance1 = Device.findById(deviceInstance?.id)
			if(!(script?.boxTypes?.find { it?.id == deviceInstance1?.boxType?.id })){
				scriptStatus = false
			}
		}
		return scriptStatus
	}



	def getScript(realPath,dirName,fileName){
		dirName = dirName?.trim()
		fileName = fileName?.trim()

		def moduleObj = Module.findByName(dirName)
		def scriptDirName = Constants.COMPONENT
		if(moduleObj){
			if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
				scriptDirName = Constants.INTEGRATION
			}
		}

		File file = new File( "${realPath}//fileStore//testscripts//"+scriptDirName+"//"+dirName+"//"+fileName+".py");
		Map script = [:]
		if(file.exists()){
			String s = ""
			List line = file.readLines()
			int indx = line?.findIndexOf {  it.startsWith("'''")} 
			String scriptContent = ""
			if(line.get(indx).startsWith("'''"))	{
				indx++
				while(indx < line.size() &&  !line.get(indx).startsWith("'''")){
					if(!(line.get(indx)?.equals(""))){ //Issue fix  for line gap between xml tags
						s = s + line.get(indx)+"\n"
					}
					indx++
				}
				indx ++
				while(indx < line.size()){
					scriptContent = scriptContent + line.get(indx)+"\n"
					indx++
				}
			}


			String xml = s
			XmlParser parser = new XmlParser();
			def node = parser.parseText(xml)
			script.put("id", node.id.text())
			script.put("version", node.version.text())
			script.put("name", node.name.text())
			script.put("skip", node.skip.text())
			def nodePrimitiveTestName = node.primitive_test_name.text()
			def primitiveMap = PrimitiveService.primitiveModuleMap
			def moduleName1 = primitiveMap.get(nodePrimitiveTestName)

			def moduleObj1 = Module.findByName(dirName)
			def scriptDirName1 = Constants.COMPONENT
			if(moduleObj1){
				if(moduleObj1?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
					scriptDirName1 = Constants.INTEGRATION
				}
			}

			def primitiveTest = getPrimitiveTest(realPath+"//fileStore//testscripts//"+scriptDirName1+"//"+moduleName1+"//"+moduleName1+".xml",nodePrimitiveTestName)

			script.put("primitiveTest",primitiveTest)
			def versList = []
			def btList = []
			Set btSet = node?.box_types?.box_type?.collect{ it.text() }
			Set versionSet = node?.rdk_versions?.rdk_version?.collect{ it.text() }
			btSet.each { bt ->
				btList.add(BoxType.findByName(bt))
			}
			versionSet.each { ver ->
				versList.add(RDKVersions.findByBuildVersion(ver))
			}
			script.put("rdkVersions", versList)
			script.put("boxTypes", btList)
			script.put("status", node?.status?.text())
			script.put("synopsis", node?.synopsis?.text())
			script.put("scriptContent", scriptContent)
			script.put("executionTime", node.execution_time.text())
		}
		return script
	}

	def getPrimitiveTest(def filePath,def primitiveTestName){
		File primitiveXml = new File(filePath)
		//def node = new XmlParser().parse(primitiveXml)
		def lines = primitiveXml?.readLines()
		int indx = lines?.findIndexOf { it.startsWith("<?xml")}
		String xmlContent =""
		while(indx < lines.size()){
					xmlContent = xmlContent + lines.get(indx)+"\n"
					indx++
		}
		def parser = new XmlParser();
		def node = parser.parseText(xmlContent?.toString())

		Map primitiveMap = [:]
		node.each{
			it.primitiveTests.each{
				it.primitiveTest.each {
					if("${it.attribute('name')}" == primitiveTestName){
						primitiveMap.put("name", "${it.attribute('name')}")
						primitiveMap.put("version",  "${it.attribute('version')}")
						primitiveMap.put("id","${it.attribute('id')}")
						Set paramList = []
						def moduleName = PrimitiveService.primitiveModuleMap.get(primitiveTestName)
						primitiveMap.put("module",Module.findByName(moduleName))
						def fun = Function.findByModuleAndName(Module.findByName(moduleName),it.function.text())
						primitiveMap.put("function",fun)
						it.parameters.each {
							it.parameter.each{
								def pType = ParameterType.findByNameAndFunction("${it.attribute('name')}",fun)
								Map param = [:]
								param.put("parameterType",pType)
								param.put("value", "${it.attribute('value')}")
								paramList.add(param)
							}
							primitiveMap.put("parameters",paramList)
						}
						//				 return primitiveMap
					}else{
						def ss = "${it.attribute('name')}"
						if(ss == primitiveTestName){
						}
					}
				}
			}
		}
		return primitiveMap
	}

	public void savePausedExecutionStatus(def exId){
		try {
			Execution.withSession {
				Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus where c.id = :execId",
						[newStatus: "PAUSED", execId: exId?.toLong()])
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

	}

	public void saveExecutionDeviceStatusData(String status, def exDevId){

		try {
			ExecutionDevice.withSession {
				ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStatus  where c.id = :execId",
						[newStatus: status, execId: exDevId?.toLong()])
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

	}

	public void saveNoScriptAvailableStatus(def executionInstance , def executionDevice , def scriptName , def deviceInstance, String reason){
		try{
			ExecutionResult.withTransaction { resultstatus ->
				try {
					ExecutionResult executionResult = new ExecutionResult()
					executionResult.execution = executionInstance
					executionResult.executionDevice = executionDevice
					executionResult.script = scriptName
					executionResult.device = deviceInstance?.stbName
					executionResult.status = Constants.SKIPPED_STATUS
					executionResult.dateOfExecution = new Date()
					executionResult.executionOutput = "Test not executed. Reason : "+reason
					if(! executionResult.save(flush:true)) {
						log.error "Error saving executionResult instance : ${executionResult.errors}"
					}
					resultstatus.flush()
				}
				catch(Throwable th) {
					resultstatus.setRollbackOnly()
				}
			}
		}catch(Exception ee){
		}
	}

	def initiateLogTransfer(String executionName, String server, String logAppName, Device device){
		int count = 3
		boolean logTransferInitiated = false

		while(count > 0 && !logTransferInitiated){
			HttpURLConnection connection = null
			try{
				println "initiating transaction"
				connection = new URL("http://$server/$logAppName/startScheduler/$executionName/$device.stbName/$device.stbIp/$device.statusPort/$device.logTransferPort").openConnection()
				connectToLogServerAndExecute(connection)
				println "Initiated log transfer for $executionName"
				logTransferInitiated = true
			}
			catch(Exception e) {
				e.printStackTrace()
				--count
			}
			finally{
				if(connection != null){
					connection.disconnect()
				}
			}
		}
		println "logTransferInitiated : $logTransferInitiated"
		logTransferInitiated

	}

	def stopLogTransfer(String executionName, String server, String logAppName){

		int count = 3
		boolean logTransferStopInitiated = false
		while(count > 0 && !logTransferStopInitiated){
			HttpURLConnection connection = null
			try{
				String url = "http://$server/$logAppName/stopScheduler/$executionName"
				print "url : $url"
				connection = new URL(url).openConnection()
				connectToLogServerAndExecute(connection)
				logTransferStopInitiated = true
			}
			catch(Exception e){
				e.printStackTrace()
				--count
			}
			finally{
				if(connection != null){
					connection.disconnect()
				}
			}
		}
		logTransferStopInitiated
	}

	def void connectToLogServerAndExecute(URLConnection connection) {
		connection.setConnectTimeout(120000)
		int responseCode = connection.getResponseCode()
		if(responseCode == 200){
			String finalresp = getResponse(connection.getInputStream())
			println finalresp
		}
		else{
			String finalresp = getResponse(connection.getErrorStream())
			try{
				String resp = finalresp.substring(finalresp.indexOf("<body><h1>")+"<body><h1>".length(), finalresp.indexOf("</h1>"))
				println resp.split("-")[1].trim()
			}
			catch(Exception e){
				println finalresp
			}
		}
	}

	def String getResponse(InputStream inputStream){
		BufferedReader buf = new BufferedReader(new InputStreamReader(inputStream))
		StringBuilder build = new StringBuilder()
		String x = null
		while( (x = buf.readLine())!= null){
			build.append(x).append("\n")
		}
		buf.close()
		String finalresp = build.toString()
		finalresp
	}
}
