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

import groovy.xml.MarkupBuilder
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

	public static final String EXPORT_SCRIPT_LABEL 			= "Script"
	public static final String EXPORT_STATUS_LABEL 			= "Status"
	public static final String EXPORT_DEVICE_LABEL 			= "Device"
	public static final String EXPORT_DEVICE_DETAILS_LABEL 	= "Device Details"
	public static final String EXPORT_LOGDATA_LABEL			= "Log Data"
	public static final String EXPORT_FUNCTION_LABEL 		= "Function: "
	public static final String EXPORT_FUNCTION_STATUS_LABEL = "Function Status: "
	public static final String EXPORT_EXPECTED_RESULT_LABEL = "Expected Result: "
	public static final String EXPORT_ACTUAL_RESULT_LABEL 	= "Actual Result: "
	public static final String EXPORT_IPADDRESS_LABEL 		= "IP Address"
	public static final String EXPORT_EXECUTION_TIME_LABEL 	= "Time taken for execution(min)"
	public static final String EXPORT_COLUMN1_LABEL 		= "C1"
	public static final String EXPORT_COLUMN2_LABEL 		= "C2"
	public static final String EXPORT_SYSTEMDIAGNOSTICS		= "SystemDiagnostics"
	public static final String EXPORT_BENCHMARKING			= "BenchMarking"
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
				device(name:executionDeviceInstance?.device.toString(), ip1:executionDeviceInstance?.deviceIp, exectime:executionDeviceInstance?.executionTime, status:executionDeviceInstance?.status) {
					executionDeviceInstance.executionresults.each{ executionResultInstance ->
						scripts(name:executionResultInstance?.script, status:executionResultInstance?.status){
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
							def benchmarkList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,"BenchMark")
							Benchmark(){
								benchmarkList?.each{ bmInstance ->
									Function(APIName:bmInstance?.processName,ExecutionTime:bmInstance?.processValue)
								}
							}
							def systemDiagList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,"SYSTEMDIAGNOSTICS")
							SystemDiagnostics{
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
	 * Delete the selected execution results
	 * @param selectedRows
	 * @return
	 */
	def deleteSelectedRowOfExecutionResult(def selectedRows) {
		List executionResultList = []
		List executionMethodResultInstanceList = []
		int deleteCount = 0

		for(int i=0;i<selectedRows.size();i++){
			if(selectedRows[i] != UNDEFINED && selectedRows[i] != MARK_ALL_ID1 && selectedRows[i] != MARK_ALL_ID2 ){
				Execution executionInstance = Execution.findById(selectedRows[i].toLong())
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
						}
						executionResultInstance.delete(flush:true)
					}

					def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)

					executionDeviceList.each{ executionDeviceInstance ->
						executionDeviceInstance.delete(flush:true)
					}

					executionInstance.delete(flush:true)
					deleteCount ++
					log.info "Deleted "+executionInstance

					/**
					 * Deletes the log files, crash files 										  
					 */
				}
				else{
					log.info "Invalid executionInstance"
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

			mapDevice 			= ["C1":EXPORT_DEVICE_LABEL,"C2":deviceName]
			mapIpAddress 		= ["C1":EXPORT_IPADDRESS_LABEL, "C2": deviceIp]
			mapExecutionTime 	= ["C1":EXPORT_EXECUTION_TIME_LABEL,"C2":executionTime]
			deviceDetailsMap    = ["C1":EXPORT_DEVICE_DETAILS_LABEL,"C2":deviceDetails]
			blankRowMap 		= ["C1":"     ","C2":"     "]

			dataList.add(blankRowMap)
			dataList.add(mapDevice)
			dataList.add(mapIpAddress)
			dataList.add(mapExecutionTime)
			dataList.add(deviceDetailsMap)
			dataList.add(blankRowMap)

			executionResultInstanceList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDeviceInstance)
			executionResultInstanceList.each{ executionResultInstance ->

				List functionList = []
				List expectedResultList = []
				List actualResultList = []
				List functionStatusList = []

				String scriptName = executionResultInstance?.script
				String status = executionResultInstance?.status
				String output = executionResultInstance?.executionOutput
				String executionOutput

				if(output){
					executionOutput = output.replace(HTML_BR, NEW_LINE)
					if(executionOutput && executionOutput.length() > 10000){
						executionOutput = executionOutput.substring(0, 10000)
					}
				}

				Map scriptNameMap 	= ["C1":EXPORT_SCRIPT_LABEL,"C2":scriptName]
				Map statusMap 		= ["C1":EXPORT_STATUS_LABEL,"C2":status]
				Map logDataMap 		= ["C1":EXPORT_LOGDATA_LABEL,"C2":executionOutput]

				dataList.add(scriptNameMap)
				dataList.add(statusMap)
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

				benchmarkList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,KEY_BENCHMARK)
				systemDiagList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,KEY_SYSTEMDIAGNOSTICS)

				benchmarkList?.each{ bmInstance ->
					benchMarkDetails = benchMarkDetails + bmInstance?.processName + HYPHEN + bmInstance?.processValue + NEW_LINE
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
	 * Function to populate performance data in db if the data is available only as files
	 * @param executionInstance
	 * @param realPath
	 * @return
	 */
	def populateChartData(final Execution executionInstance,final String realPath){
		if(!executionInstance?.isPerformanceDone){
			executionService.setPerformance(executionInstance,realPath)
		}
	}
}
