/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
package com.comcast.rdk

import static com.comcast.rdk.Constants.*

import groovy.xml.MarkupBuilder

import java.text.SimpleDateFormat;
import java.util.List;

/**
 * Service class of ExecutionController 
 */

class ExecutedbService {

	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication

	/**
	 * Injects the executionService.
	 */
	def executionService
	
	def scriptService

	public static final String SI_NO_LABEL 					= "SI NO:"
	public static final String EXPORT_SCRIPT_LABEL 			= "Script"
	public static final String EXPORT_STATUS_LABEL 			= "Status"
	public static final String EXPORT_TIMETAKEN 			= "Time Taken(min)"
	public static final String EXPORT_DEVICE_LABEL 			= "Device"
	public static final String EXPORT_DEVICE_DETAILS_LABEL 	= "Image Details"
	public static final String EXPORT_LOGDATA_LABEL			= "Log Data"
	public static final String EXPORT_FUNCTION_LABEL 		= "Function: "
	public static final String EXPORT_FUNCTION_STATUS_LABEL = "Function Status: "
	public static final String EXPORT_EXPECTED_RESULT_LABEL = "Expected Result: "
	public static final String EXPORT_ACTUAL_RESULT_LABEL 	= "Actual Result: "
	public static final String EXPORT_IPADDRESS_LABEL 		= "IP Address"
	public static final String EXPORT_EXECUTION_TIME_LABEL 	= "Time taken for execution(min)"
	public static final String EXPORT_COLUMN1_LABEL 		= "C1"
	public static final String EXPORT_COLUMN2_LABEL 		= "C2"
	public static final String EXPORT_SYSTEMDIAGNOSTICS		= "PerformanceData"
	public static final String EXPORT_BENCHMARKING			= "TimeInfo"
	public static final String EXPORT_PERFORMANCE			= "Performance"

	public static final String MARK_ALL_ID1 				= "markAll1"
	public static final String MARK_ALL_ID2 				= "markAll2"
	public static final String UNDEFINED					= "undefined"


	/**
	 * Function to create data in xml format for execution result
	 * @param execName
	 * @return
	 */
	def String getExecutionDataInXmlFormat(final String execName){
		Execution executionInstance = Execution.findByName(execName)
		def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
		xml.executionResult(name: executionInstance?.name.toString(), status: executionInstance?.result.toString()) {
			executionDevice.each{ executionDeviceInstance ->
				device(name:executionDeviceInstance?.device.toString(), deviceIp:executionDeviceInstance?.deviceIp, executiondate:executionInstance?.dateOfExecution, timetakentoexecute:executionInstance?.executionTime, status:executionDeviceInstance?.status) {

					def summaryMap = getStatusList(executionInstance,executionDeviceInstance,executionDeviceInstance.executionresults?.size()?.toString())

					Summary(){
						TotalScriptsExecuted(summaryMap.get("Total Scripts in ScriptGroup"))
						Success(summaryMap?.get("SUCCESS"))
						Failure(summaryMap?.get("FAILURE"))
						NotApplicable(summaryMap?.get("N/A"))
						Skipped(summaryMap?.get("SKIPPED"))
						Pending(summaryMap?.get("PENDING"))
						ScriptTimedOut(summaryMap?.get("TIMED OUT"))
						Undefined(summaryMap?.get("UNDEFINED"))
					}

					executionDeviceInstance.executionresults.each{ executionResultInstance ->
						scripts(name:executionResultInstance?.script, status:executionResultInstance?.status, scriptexecutiontime:executionResultInstance?.executionTime){
							executionResultInstance.executemethodresults.each{executionResultMthdsInstance ->
								function(name:executionResultMthdsInstance?.functionName){
									expectedResult(executionResultMthdsInstance?.expectedResult)
									actualResult(executionResultMthdsInstance?.actualResult)
									status(executionResultMthdsInstance?.status)
								}
							}
							logData(executionResultInstance?.executionOutput)
						}

						performance(){
							def benchmarkList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,KEY_BENCHMARK)
							TimeInfo(){
								benchmarkList?.each{ bmInstance ->
									Function(APIName:bmInstance?.processName,ExecutionTime:bmInstance?.processValue+"(ms)")
								}
							}
							def systemDiagList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,KEY_SYSTEMDIAGNOSTICS)
							PerformanceData{
								systemDiagList?.each{ sdInstance ->
									Process(ProcessName:sdInstance?.processName,ProcessValue:sdInstance?.processValue)
								}
							}
						}
					}
				}
			}
		}
		return writer
	}
	
	/**
	 * Method to check the Execution Instance is available or not
	 *
	 */
	def isValidExecutionAvailable(Execution executionInstance ){
		List executionDeviceList = []
		executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		if(executionDeviceList){
			return Constants.SUCCESS_STATUS
		}
		return Constants.FAILURE_STATUS
	}


	/**
	 * Delete the selected execution results
	 * @param selectedRows
	 * @return
	 */
	def deleteSelectedRowOfExecutionResult(def selectedRows, String realPath) {
		List executionResultList = []
		List executionMethodResultInstanceList = []
		List performanceList = []
		int deleteCount = 0

		for(int i=0;i<selectedRows.size();i++){
			if(selectedRows[i] != UNDEFINED && selectedRows[i] != MARK_ALL_ID1 && selectedRows[i] != MARK_ALL_ID2 ){
				Execution executionInstance = Execution.findById(selectedRows[i].toLong())
				if(!executionInstance?.executionStatus?.equals(INPROGRESS_STATUS) ){
					if( !executionInstance?.executionStatus?.equals(PAUSED)){
				if(executionInstance){

					executionResultList  = ExecutionResult.findAllByExecution(executionInstance)
					executionResultList.each { executionResultInstance ->
						if(executionResultInstance){
							executionMethodResultInstanceList = ExecuteMethodResult.findAllByExecutionResult(executionResultInstance)
							if(executionMethodResultInstanceList){
								executionMethodResultInstanceList.each { executionMethodResultInstance ->
									executionMethodResultInstance.delete(flush:true)
								}
							}
							performanceList = Performance.findAllByExecutionResult(executionResultInstance)
							performanceList.each{ performance ->
								performance.delete(flush:true)
							}
						}
						executionResultInstance.delete(flush:true)
					}

					def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)

					executionDeviceList.each{ executionDeviceInstance ->
						executionDeviceInstance.delete(flush:true)
					}
					
					if(executionInstance?.thirdPartyExecutionDetails){
						executionInstance?.thirdPartyExecutionDetails = null;
						executionInstance?.save();
					}
					
					def thirdPartyExecutionDetailsList = ThirdPartyExecutionDetails.findAllByExecution(executionInstance)
					thirdPartyExecutionDetailsList?.each{ thirdPartyExecution ->
						thirdPartyExecution?.delete(flush:true)
					}

					def execId = executionInstance?.id

					executionInstance.delete(flush:true)
					deleteCount ++
					log.info "Deleted "+executionInstance

					/**
					 * Deletes the log files, crash files 										  
					 */

					String logFilePath = "${realPath}//logs//"+execId
					def logFiles = new File(logFilePath)
					if(logFiles.exists()){
						logFiles?.deleteDir()
					}
					String crashFilePath = "${realPath}//logs//crashlogs//"

					new File(crashFilePath).eachFileRecurse { file->
						if((file?.name).startsWith(execId.toString())){
							file?.delete()
						}
					}

					String versionFilePath = "${realPath}//logs//version//"+execId
					def versionFiles = new File(versionFilePath)
					if(versionFiles.exists()){
						versionFiles?.deleteDir()
					}

					String agentLogFilePath = "${realPath}//logs//consolelog//"+execId
					def agentLogFiles = new File(agentLogFilePath)
					if(agentLogFiles.exists()){
						agentLogFiles?.deleteDir()
					}
				}
				else{
					log.info "Invalid executionInstance"
				}
				}
				}
			}
		}
		return deleteCount
	}


	/**
	 * Function to create data in excel format for execution result
	 * @param executionInstance
	 * @param realPath
	 * @return
	 */
	def getDataForExcelExport(Execution executionInstance, String realPath) {
		List executionDeviceList = []
		List executionResultInstanceList = []
		List executionMethodResultInstanceList = []
		List executionReportData = []
		List dataList = []
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList = []
		List benchmarkList = []
		List systemDiagList = []

		columnWidthList = [0.35, 0.5]
		String deviceDetails

		String fileContents = ""
		def deviceName = ""
		def deviceIp = ""
		def executionTime = ""

		String filePath = ""
		def executionDeviceId
		def benchMarkDetails = ""
		def sdDetails = ""

		Map mapDevice = [:]
		Map mapIpAddress = [:]
		Map mapExecutionTime = [:]
		Map deviceDetailsMap = [:]
		Map blankRowMap = [:]

		Map summaryHead = [:]
		Map statusValue = [:]



		executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)

		executionDeviceList.each{ executionDeviceInstance ->

			deviceName = executionDeviceInstance?.device
			deviceIp = executionDeviceInstance?.deviceIp
			executionTime = executionDeviceInstance?.executionTime

			executionDeviceId = executionDeviceInstance?.id
			filePath = "${realPath}//logs//version//${executionInstance?.id}//${executionDeviceId?.toString()}//${executionDeviceId?.toString()}_version.txt"

			if(filePath){
				File file = new File(filePath)
				if(file.exists()){
					file.eachLine { line ->
						if(!(line.isEmpty())){
							if(!(line.startsWith( LINE_STRING ))){

								fileContents = fileContents + line + HTML_BR
							}
						}
					}
					deviceDetails = fileContents.replace(HTML_BR, NEW_LINE)
				}
				else{
					log.error "No version file found"
				}
			}
			else{
				log.error "Invalid file path"
			}
			
			String image = "Not Available"
			try {
				if(deviceDetails != null && deviceDetails.contains("imagename:")){
					String imagename = "imagename:"
					int indx = deviceDetails.indexOf(imagename)
					int endIndx = deviceDetails.indexOf("\n",indx)
					if(indx >0 && endIndx > 0){
						indx = indx + imagename.length()
						image = deviceDetails.substring(indx, endIndx)
					}
				}
			} catch (Exception e) {
				e.printStackTrace()
			}

			mapDevice 			= ["C1":EXPORT_DEVICE_LABEL,"C2":deviceName]
			mapIpAddress 		= ["C1":EXPORT_IPADDRESS_LABEL, "C2": deviceIp]
			mapExecutionTime 	= ["C1":EXPORT_EXECUTION_TIME_LABEL,"C2":executionTime]
			deviceDetailsMap    = ["C1":EXPORT_DEVICE_DETAILS_LABEL,"C2":image]
			blankRowMap 		= ["C1":"     ","C2":"     "]
			
			

			dataList.add(blankRowMap)
			dataList.add(mapDevice)
			dataList.add(mapIpAddress)
			dataList.add(mapExecutionTime)
			dataList.add(deviceDetailsMap)
			dataList.add(blankRowMap)

			executionResultInstanceList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDeviceInstance)//,[sort: "script",order: "asc"])

			def summaryMap = getStatusList(executionInstance,executionDeviceInstance,executionResultInstanceList?.size()?.toString())

			mapDevice 			= ["C1":"SUMMARY","C2":"   "]
			dataList.add(mapDevice)

			summaryMap.each{ mapInfo->
				statusValue 	= ["C1": mapInfo.key, "C2": mapInfo.value ]
				dataList.add(statusValue)
			}

			blankRowMap 		= ["C1":"     ","C2":"     "]
			dataList.add(blankRowMap)

			executionResultInstanceList.each{ executionResultInstance ->

				List functionList = []
				List expectedResultList = []
				List actualResultList = []
				List functionStatusList = []

				String scriptName = executionResultInstance?.script
				String status = executionResultInstance?.status
				String output = executionResultInstance?.executionOutput
				String scriptExecTime = executionResultInstance?.executionTime
				String executionOutput

				if(output){
					executionOutput = output.replace(HTML_BR, NEW_LINE)
					if(executionOutput && executionOutput.length() > 10000){
						executionOutput = executionOutput.substring(0, 10000)
					}
				}

				Map scriptNameMap 	= ["C1":EXPORT_SCRIPT_LABEL,"C2":scriptName]
				Map statusMap 		= ["C1":EXPORT_STATUS_LABEL,"C2":status]
				Map scriptTimeMap 	= ["C1":EXPORT_TIMETAKEN,"C2":scriptExecTime]
				Map logDataMap 		= ["C1":EXPORT_LOGDATA_LABEL,"C2":executionOutput]

				dataList.add(scriptNameMap)
				dataList.add(statusMap)
				dataList.add(scriptTimeMap)
				executionMethodResultInstanceList = ExecuteMethodResult.findAllByExecutionResult(executionResultInstance)
				if(executionMethodResultInstanceList){
					executionMethodResultInstanceList.each{ executionMethodResultInstance ->
						Map executionMethodResultMap = [:]
						def functionName = executionMethodResultInstance?.functionName
						def expectedResult = executionMethodResultInstance?.expectedResult
						def actualResult = executionMethodResultInstance?.actualResult
						def functionStatus = executionMethodResultInstance?.status
						functionList.add(functionName)
						expectedResultList.add(expectedResult)
						actualResultList.add(actualResult)
						functionStatusList.add(functionStatus)
					}
				}

				int functionCount = functionList.size()
				for(int i=0;i<functionCount;i++){

					def functionDetails
					functionDetails = EXPORT_EXPECTED_RESULT_LABEL+expectedResultList[i] + NEW_LINE +
							EXPORT_ACTUAL_RESULT_LABEL+actualResultList[i] + NEW_LINE + EXPORT_FUNCTION_STATUS_LABEL+functionStatusList[i] + NEW_LINE

					Map functionDetailsMap = ["C1":EXPORT_FUNCTION_LABEL+functionList[i],"C2":functionDetails]
					dataList.add(functionDetailsMap)
				}

				dataList.add(logDataMap)
				dataList.add(blankRowMap)

				populateChartData(executionInstance,realPath)

				benchMarkDetails = ""				
				sdDetails = ""
				
				benchmarkList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,KEY_BENCHMARK)
				systemDiagList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,KEY_SYSTEMDIAGNOSTICS)

				benchmarkList?.each{ bmInstance ->
					benchMarkDetails = benchMarkDetails + bmInstance?.processName + HYPHEN + bmInstance?.processValue +"(ms)" + NEW_LINE
				}

				systemDiagList?.each{ sdInstance ->
					sdDetails = sdDetails + sdInstance?.processName + HYPHEN + sdInstance?.processValue + NEW_LINE
				}
				if(benchmarkList || systemDiagList){
					Map performanceHeadMap = ["C1":EXPORT_PERFORMANCE]
					dataList.add(performanceHeadMap)
					dataList.add(blankRowMap)

					Map benchMarkHeadMap = ["C1":EXPORT_BENCHMARKING,"C2":benchMarkDetails]
					dataList.add(benchMarkHeadMap)

					Map sdHeadMap = ["C1":EXPORT_SYSTEMDIAGNOSTICS,"C2":sdDetails]
					dataList.add(sdHeadMap)
				}
			}
		}
		return dataList
	}


	/**
	 * Method to get the data for creating the consolidated report in excel format.
	 */
	def getDataForConsolidatedListExcelExport(Execution executionInstance, String realPath,String appUrl) {

		List executionDeviceList = []
		List executionResultInstanceList = []
		List columnWidthList = []
		columnWidthList = [0.1, 0.3, 0.1, 0.4]
		
		String deviceDetails

		String fileContents = ""
		def deviceName = ""
		def deviceIp = ""
		def executionTime = ""
		int totalCount = 0
		int testCount =0

		String filePath = ""
		def executionDeviceId

		Map summaryHead = [:]
		Map statusValue = [:]
		List fieldList = ["C1", "C2", "C3", "C4", "C5","C6","C7","C8","C9","C10"]


		executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def detailDataMap = [:]
		executionDeviceList.each{ executionDeviceInstance ->

			deviceName = executionDeviceInstance?.device
			deviceIp = executionDeviceInstance?.deviceIp
			executionTime = executionDeviceInstance?.executionTime

			executionDeviceId = executionDeviceInstance?.id
			filePath = "${realPath}//logs//version//${executionInstance?.id}//${executionDeviceId?.toString()}//${executionDeviceId?.toString()}_version.txt"
			if(filePath){
				File file = new File(filePath)
				if(file.exists()){
					file.eachLine { line ->
						if(!(line.isEmpty())){
							if(!(line.startsWith( LINE_STRING ))){
								fileContents = fileContents + line + HTML_BR
							}
						}
					}
					deviceDetails = fileContents.replace(HTML_BR, NEW_LINE)
				}
				else{
					//println "No version file found"
				}
			}
			else{
				//println "Invalid file path"
			}

			Map coverPageMap = [:]
			detailDataMap.put("CoverPage", coverPageMap)
			Map detailsMap = [:]
			coverPageMap.put("Details",detailsMap)
			detailsMap.put("Device", deviceName)
			detailsMap.put("DeviceIP", deviceIp)
			detailsMap.put("Execution Time (min)", executionTime)
			try {
				String image = "Not Available"
				if(deviceDetails != null && deviceDetails.contains("imagename:")){
					String imagename = "imagename:"
					int indx = deviceDetails.indexOf(imagename)
					int endIndx = deviceDetails.indexOf("\n",indx)
					if(indx >=0 && endIndx > 0){
						indx = indx + imagename.length()
						image = deviceDetails.substring(indx, endIndx)
					}
				}
				detailsMap.put("Image", image)
			} catch (Exception e) {
				e.printStackTrace()
			}
			
		

			executionResultInstanceList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDeviceInstance)//,[sort: "script",order: "asc"])
			def summaryMap = getStatusList(executionInstance,executionDeviceInstance,executionResultInstanceList?.size()?.toString())
			
			int counter = 1
			int counter1=1
			Date date = new Date()
			executionResultInstanceList.each{ executionResultInstance ->
				counter1= counter1+1
			
				String scriptName = executionResultInstance?.script
				String status = executionResultInstance?.status
				String output = executionResultInstance?.executionOutput
				String executionOutput
				String moduleName = ""
//				int  execution = executionResultInstance?.script?.count
//				Script.withTransaction {
//					Script scrpt = Script.findByName(scriptName)
//					moduleName = scrpt?.primitiveTest?.module?.name
				
//				}
				
				if(executionResultInstance?.category != Category.RDKB_TCL){
					def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
					moduleName = sMap.get(scriptName)
				}
				else{
					moduleName = 'tcl'
				}
				
				int i = 0
				
				if(!moduleName.equals("")){	
		//			def scriptObj1 = ScriptFile.findByModuleName(moduleName)
		
	
					def scriptObj = ScriptFile.findByScriptNameAndModuleName(scriptName,moduleName)
					if(scriptObj){
						def dataList					
						Map dataMapList = detailDataMap.get(moduleName)
							if(dataMapList == null){
								dataMapList = [:]
								detailDataMap.put(moduleName,dataMapList)
								//detailDataMap.put("total", summaryMap.get("Total Scripts"))
							}				
						
						if(dataMapList != null){
							dataList = dataMapList.get("dataList")
							if(dataList == null){
								dataList = []
								dataMapList.put("dataList",dataList)
								dataMapList.put("fieldsList",fieldList)
								counter = 1
						}else{
							counter =  dataMapList.get("counter")
						}
						if(dataList != null){
							
							if(output){
								executionOutput = output.replace(HTML_BR, NEW_LINE)
								if(executionOutput && executionOutput.length() > 10000){
									executionOutput = executionOutput.substring(0, 10000)
								}
							}
								
							String executed
							if( "PENDING".equals(status)){
								executed = "NO"
							}			
							else{
								executed = "YES"
							}
							/*Map dataMap = ["C1":counter,"C2":scriptName,"C3":status,"C4":executionOutput,"C5":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id,,"C6":parseTime(executionInstance?.dateOfExecution)] 						
							Map dataMap =["C1":counter,"C2":scriptName,"C3":executed,"C4":status,"C5":parseTime(executionInstance?.dateOfExecution),"C6":appUrl+"/execution/getExecutionOutput?execResId="+executionResultInstance?.id,"C7":"","C8":"","C9":"","C10":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id]*/
							Map dataMap
							def countOfExecutionOutput = executionOutput?.size()
							//For CGRTS-521 
							String executionLogData = executionOutput
							if(countOfExecutionOutput >= 1000 ){
								executionLogData = executionOutput+"\n More data use this link ....... \n " +appUrl+"/execution/getExecutionOutput?execResId="+executionResultInstance?.id
							}
							
							dataMap =["C1":counter,"C2":scriptName,"C3":executed,"C4":status,"C5":parseTime(executionInstance?.dateOfExecution),"C6":executionLogData,"C7":"","C8":"","C9":"","C10":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id]
							
							dataList.add(dataMap)
							counter ++
							dataMapList.put("counter",counter)
						}
					}
				}
			}
		}
	}			
		prepareStatusList(detailDataMap)
		return detailDataMap
	}
	
	/**
	 * Method to parse the time show in execution date in consolidated report.
	 */
	def parseTime(Date date){
		String dateString = ""
		try {
			SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy")
			dateString = sdf.format(date)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return dateString
	}

	/**
	 * Method to populate status list to show in cover page of consolidated report.
	 */
	def prepareStatusList(Map detailDataMap){
		Set keySet = detailDataMap.keySet();
		int counter = 1
		int totalScripts = 0
		int tSuccess = 0
		int tFailure = 0
		int tNa = 0
		int tSkip = 0
		int tTimeOut =0
		int scriptCount = 0;
		int totalScript = 0
		
		keySet.each { key ->
			if(!key.equals("CoverPage")){	
				int success = 0
				int failure = 0
				int na = 0
				int skip = 0
				int total = 0
				int timeOut = 0
			
				Map dataMap = detailDataMap.get(key)
				List dataList = dataMap.get("dataList")
				dataList.each { dMap ->
					
					if(!dMap.get("C4").equals("PENDING")){
						total ++
					}
					
					if(dMap.get("C4").equals(Constants.SUCCESS_STATUS)){
						success ++
					}else if(dMap.get("C4").equals(Constants.FAILURE_STATUS)){
						failure ++
					}else if(dMap.get("C4").equals(Constants.NOT_APPLICABLE_STATUS)){
						na ++
					}else if(dMap.get("C4").equals(Constants.SKIPPED_STATUS)){
						skip ++
					}else if(dMap.get("C4").equals("SCRIPT TIME OUT")){
						timeOut ++
					}
					//scriptCount = Integer.parseInt(dMap.get("total"))
					//scriptCount =dMap.get("total")
				}
				Map coverPageMap = detailDataMap.get("CoverPage")
				Map resultMap = [:]
				resultMap.put("Sl No", counter)
				resultMap.put("Module", key)
				//resultMap.put("Total",	scriptCount)
				resultMap.put("Executed", total)
				resultMap.put(Constants.SUCCESS_STATUS, success)
				resultMap.put(Constants.FAILURE_STATUS, failure)
				resultMap.put("SCRIPT TIME OUT", timeOut)
				resultMap.put(Constants.NOT_APPLICABLE_STATUS, na)
				resultMap.put(Constants.SKIPPED_STATUS, skip)

				coverPageMap.put(key, resultMap)
				counter ++

				tSuccess += success
				tFailure += failure
				tNa += na
				tSkip += skip
				totalScripts += total
				tTimeOut += timeOut
				//totalScript +=scriptCount

			}
		}
		//scriptCount=Integer.parseInt(resultMap.getAt("total"))
		Map coverPageMap = detailDataMap.get("CoverPage")
		Map resultMap = [:]
		
		resultMap.put("Sl No", "")
		resultMap.put("Module", "Total")
		//resultMap.put("Total", 	totalScript)
		resultMap.put("Executed", totalScripts)
		resultMap.put(Constants.SUCCESS_STATUS, tSuccess)
		resultMap.put(Constants.FAILURE_STATUS, tFailure)
		resultMap.put("SCRIPT TIME OUT", tTimeOut)
		resultMap.put(Constants.NOT_APPLICABLE_STATUS, tNa)
		resultMap.put(Constants.SKIPPED_STATUS, tSkip)
		//resultMap.put("Number of failed scripts linked with open defects","")
		//resultMap.put("Script Issue", "")
		//resultMap.put("Existing Issue", "")
		//resultMap.put("New Issue","")
		//resultMap.put("Environment Issue", "")
		//resultMap.put("Interface Change","")
		//resultMap.put("Remarks","")
		
		coverPageMap.put("Total", resultMap)
	}
	/**
	 * Function to populate performance data in db if the data is available only as files
	 * @param executionInstance
	 * @param realPath
	 * @return
	 */
	def populateChartData(final Execution executionInstance,final String realPath){
		//	if(!executionInstance?.isPerformanceDone){
		executionService.setPerformance(executionInstance,realPath)
		//	}
	}

	/**
	 * Get the execution status summary of script executed from the results.
	 * @param executionInstance
	 * @param executionDevice
	 * @param scriptCnt
	 * @return
	 */
	def Map getStatusList(final Execution executionInstance, final ExecutionDevice executionDevice, final String scriptCnt){

		def listStatusCount = [:]
		int scriptCount = 0

		if(executionInstance?.scriptGroup || executionInstance?.script.toString().equals("Multiple Scripts")){
			ScriptGroup scriptGrp = ScriptGroup.findByName(executionInstance?.scriptGroup)
			if(scriptGrp || executionInstance?.script.toString().equals("Multiple Scripts")){

				def successCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SUCCESS")

				def failureCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"FAILURE")

				def skippedCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SKIPPED")
				
				def naCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"N/A")
				
				def pendingCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"PENDING")
				
				def unknownCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"UNDEFINED")

				def timeoutCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SCRIPT TIME OUT")

				if((executionInstance?.scriptCount != 0 ) && (executionInstance?.scriptCount != null)){
					scriptCount = executionInstance?.scriptCount
				}
				else{
					scriptCount = Integer.parseInt(scriptCnt)
				}

				def executedCount = ExecutionResult.countByExecutionDevice(executionDevice)
				executedCount = executedCount - pendingCount 
				
				listStatusCount.put("Total Scripts",scriptCount?.toString())
				listStatusCount.put("Executed",""+executedCount?.toString())
				listStatusCount.put("SUCCESS",successCount?.toString())
				listStatusCount.put("FAILURE",failureCount?.toString())
				listStatusCount.put("N/A",naCount?.toString())
				listStatusCount.put("SKIPPED",skippedCount?.toString())
				listStatusCount.put("PENDING",pendingCount?.toString())
				listStatusCount.put("TIMED OUT",timeoutCount?.toString())
				listStatusCount.put("UNDEFINED",unknownCount?.toString())
			}
		}
		return listStatusCount
	}

	def Map getDetailedStatusList(final Execution executionInstance, final ExecutionDevice executionDevice, final String scriptCnt,String realPath){
		def dataMap = prepareDetailMap(executionInstance, KEY_GATEWAYIP)
				def listStatusCount = [:]
				int scriptCount = 0
		
				if(executionInstance?.scriptGroup){
					ScriptGroup scriptGrp = ScriptGroup.findByName(executionInstance?.scriptGroup)
					if(scriptGrp){
		
						def successCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SUCCESS")
		
						def failureCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"FAILURE")
		
						def skippedCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SKIPPED")
		
						def naCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"N/A")
		
						def pendingCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"PENDING")
		
						def unknownCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"UNDEFINED")
		
						def timeoutCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SCRIPT TIME OUT")
		
						if((executionInstance?.scriptCount != 0 ) && (executionInstance?.scriptCount != null)){
							scriptCount = executionInstance?.scriptCount
						}
						else{
							scriptCount = Integer.parseInt(scriptCnt)
						}
		
						def executedCount = ExecutionResult.countByExecutionDevice(executionDevice)
						executedCount = executedCount - pendingCount
						
						listStatusCount.put("Total Scripts",scriptCount?.toString())
						listStatusCount.put("Executed",""+executedCount?.toString())
						listStatusCount.put("SUCCESS",successCount?.toString())
						listStatusCount.put("FAILURE",failureCount?.toString())
						listStatusCount.put("N/A",naCount?.toString())
						listStatusCount.put("SKIPPED",skippedCount?.toString())
						listStatusCount.put("PENDING",pendingCount?.toString())
						listStatusCount.put("TIMED OUT",timeoutCount?.toString())
						listStatusCount.put("UNDEFINED",unknownCount?.toString())
					}
				}
				return listStatusCount
			}
	
	def prepareDetailMap(def executionInstance,def realPath){
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def detailDataMap = [:]
		def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
		executionDeviceList.each{ executionDeviceInstance ->
			def executionResultInstanceList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDeviceInstance)
			executionResultInstanceList.each{ executionResultInstance ->
				String scriptName = executionResultInstance?.script
				String status = executionResultInstance?.status
				Category category = executionResultInstance?.category 
				if(category != Category.RDKB_TCL){
					def moduleName = sMap.get(scriptName)
					
					if(moduleName && !moduleName.equals("null") && !moduleName.equals("")){
						
						def moduleMap = detailDataMap.get(moduleName)
						if(!moduleMap){
							moduleMap = [:]
							detailDataMap.put(moduleName,moduleMap)
						}
						def statusCounter = moduleMap.get(status)
						if(!statusCounter){
							statusCounter = 0
						}
						statusCounter ++
						moduleMap.put(status, statusCounter)
					}
				}
				else{
					def moduleName = 'tcl'
					
					if(moduleName && !moduleName.equals("null") && !moduleName.equals("")){
						
						def moduleMap = detailDataMap.get(moduleName)
						if(!moduleMap){
							moduleMap = [:]
							detailDataMap.put(moduleName,moduleMap)
						}
						def statusCounter = moduleMap.get(status)
						if(!statusCounter){
							statusCounter = 0
						}
						statusCounter ++
						moduleMap.put(status, statusCounter)
					}
				}
				
			}
		}
		
		
		TreeMap<String, Map> tMap = new TreeMap<String, Map>(detailDataMap)
		return tMap
	}

	/**
	 * Method to get the data for creating the consolidated report in excel format.
	 */
	def getDataForConsolidatedListPerformanceExcelExport(Execution executionInstance, String realPath,String appUrl) {

		List executionDeviceList = []
		List executionResultInstanceList = []
		List columnWidthList = []
		columnWidthList = [0.1, 0.3, 0.1, 0.4]
		
		String deviceDetails

		String fileContents = ""
		def deviceName = ""
		def deviceIp = ""
		def executionTime = ""
		int totalCount = 0
		int testCount =0

		String filePath = ""
		def executionDeviceId

		Map summaryHead = [:]
		Map statusValue = [:]
		List fieldList = ["C1", "C2", "C3", "C4", "C5","C6","C7","C8","C9","C10","C11"]


		executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def detailDataMap = [:]
		executionDeviceList.each{ executionDeviceInstance ->

			deviceName = executionDeviceInstance?.device
			deviceIp = executionDeviceInstance?.deviceIp
			executionTime = executionDeviceInstance?.executionTime

			executionDeviceId = executionDeviceInstance?.id
			filePath = "${realPath}//logs//version//${executionInstance?.id}//${executionDeviceId?.toString()}//${executionDeviceId?.toString()}_version.txt"
			if(filePath){
				File file = new File(filePath)
				if(file.exists()){
					file.eachLine { line ->
						if(!(line.isEmpty())){
							if(!(line.startsWith( LINE_STRING ))){
								fileContents = fileContents + line + HTML_BR
							}
						}
					}
					deviceDetails = fileContents.replace(HTML_BR, NEW_LINE)
				}
				else{
					//println "No version file found"
				}
			}
			else{
				//println "Invalid file path"
			}

			Map coverPageMap = [:]
			detailDataMap.put("CoverPage", coverPageMap)
			Map detailsMap = [:]
			coverPageMap.put("Details",detailsMap)
			detailsMap.put("Device", deviceName)
			detailsMap.put("DeviceIP", deviceIp)
			detailsMap.put("Execution Time (min)", executionTime)
			try {
				String image = "Not Available"
				if(deviceDetails != null && deviceDetails.contains("imagename:")){
					String imagename = "imagename:"
					int indx = deviceDetails.indexOf(imagename)
					int endIndx = deviceDetails.indexOf("\n",indx)
					if(indx >=0 && endIndx > 0){
						indx = indx + imagename.length()
						image = deviceDetails.substring(indx, endIndx)
					}
				}
				detailsMap.put("Image", image)
			} catch (Exception e) {
				e.printStackTrace()
			}
			
		

			executionResultInstanceList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDeviceInstance)//,[sort: "script",order: "asc"])
			def summaryMap = getStatusList(executionInstance,executionDeviceInstance,executionResultInstanceList?.size()?.toString())
			
			int counter = 1
			int counter1=1
			Date date = new Date()
			executionResultInstanceList.each{ executionResultInstance ->
				counter1= counter1+1
			
				String scriptName = executionResultInstance?.script
				String status = executionResultInstance?.status
				String output = executionResultInstance?.executionOutput
				String executionOutput
				String moduleName = ""
//				int  execution = executionResultInstance?.script?.count
//				Script.withTransaction {
//					Script scrpt = Script.findByName(scriptName)
//					moduleName = scrpt?.primitiveTest?.module?.name
				
//				}
				
				
				def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
				moduleName = sMap.get(scriptName)
				
				int i = 0
				
				if(!moduleName.equals("")){
		//			def scriptObj1 = ScriptFile.findByModuleName(moduleName)
		
	
					def scriptObj = ScriptFile.findByScriptNameAndModuleName(scriptName,moduleName)
					if(scriptObj){
						def dataList
						Map dataMapList = detailDataMap.get(moduleName)
							if(dataMapList == null){
								dataMapList = [:]
								detailDataMap.put(moduleName,dataMapList)
								//detailDataMap.put("total", summaryMap.get("Total Scripts"))
							}
						
						if(dataMapList != null){
							dataList = dataMapList.get("dataList")
							if(dataList == null){
								dataList = []
								dataMapList.put("dataList",dataList)
								dataMapList.put("fieldsList",fieldList)
								counter = 1
						}else{
							counter =  dataMapList.get("counter")
						}
						if(dataList != null){
							
							if(output){
								executionOutput = output.replace(HTML_BR, NEW_LINE)
								if(executionOutput && executionOutput.length() > 10000){
									executionOutput = executionOutput.substring(0, 10000)
								}
							}
								
							String executed
							if( "PENDING".equals(status)){
								executed = "NO"
							}
							else{
								executed = "YES"
							}
							/*Map dataMap = ["C1":counter,"C2":scriptName,"C3":status,"C4":executionOutput,"C5":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id,,"C6":parseTime(executionInstance?.dateOfExecution)]
							Map dataMap =["C1":counter,"C2":scriptName,"C3":executed,"C4":status,"C5":parseTime(executionInstance?.dateOfExecution),"C6":appUrl+"/execution/getExecutionOutput?execResId="+executionResultInstance?.id,"C7":"","C8":"","C9":"","C10":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id]*/
							Map dataMap
							def countOfExecutionOutput = executionOutput?.size()
							//For CGRTS-521
							String executionLogData = executionOutput
							if(countOfExecutionOutput >= 1000 ){
								executionLogData = executionOutput+"\n To view full log use this link ....... \r\n  " +appUrl+"/execution/getExecutionOutput?execResId="+executionResultInstance?.id
							}
							
							String exeTime = executionResultInstance?.executionTime
							String realExeTime = executionResultInstance?.totalExecutionTime
							float time1 = 0.0
							float time2 = 0.0
							 try {
								 time1 = Float.parseFloat(exeTime)
								 time1 = time1?.round(2)
								 time2 = Float.parseFloat(realExeTime)
								 time2 = time2?.round(2)
							} catch (Exception e) {
							}
							
							dataMap =["C1":counter,"C2":scriptName,"C3":executed,"C4":status,"C5":time1,"C6":parseTime(executionInstance?.dateOfExecution),"C7":executionLogData,"C8":"","C9":"","C10":"","C11":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id]
							
							dataList.add(dataMap)
							counter ++
							dataMapList.put("counter",counter)
						}
					}
				}
			}
		}
	}
		prepareStatusList(detailDataMap)
		return detailDataMap
	}
}
