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
import grails.converters.JSON

/**
 * Controller class for showing charts 
 * 
 */

class TrendsController {

	def executionService
	
	def index() {
	}

	/**
	 * Redirects to chart.gsp with the last 200 executions of script group
	 * @return
	 */
	def chart() {		
		def c = Execution.createCriteria()
		List<Execution> executionList = c.list {
			isNotNull("scriptGroup")
			maxResults(200)
			order("id", "desc")			
		}

		[executionList : executionList]
	}

	/**
	 * Shows the chart to draw the chart based on the execution status
	 * @return
	 */
	def getStatusChartData(){
		
		def listdate = []
		def cpuMemoryList = []
		List<Execution> executionList

		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		int scriptGrpSize
		
		if(executionList){
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
			
			scriptGrpSize = scriptGroupInstance.scripts.size()
			def executionSuccessList = []
			def executionFailureList = []
			def executionUndefinedList = []
			def executionNotExecutedList = []
	
			List<ExecutionResult> executionSuccessResultList
			List<ExecutionResult> executionFailureResultList
			List<ExecutionResult> executionUndefinedResultList
	
			executionList?.each{ execution ->
				
				populateChartData(execution)
				
				executionSuccessResultList = ExecutionResult.findAllByExecutionAndStatus(execution,SUCCESS_STATUS)
				executionFailureResultList = ExecutionResult.findAllByExecutionAndStatus(execution,FAILURE_STATUS)
				executionUndefinedResultList = ExecutionResult.findAllByExecutionAndStatus(execution,UNDEFINED_STATUS)
	
				int unexecutedScripts = scriptGrpSize - (executionSuccessResultList.size() + executionFailureResultList.size() + executionUndefinedResultList.size())
	
				executionSuccessList.add(executionSuccessResultList.size())
				executionFailureList.add(executionFailureResultList.size())
				executionUndefinedList.add(executionUndefinedResultList.size())
				executionNotExecutedList.add(unexecutedScripts)
			}
	
			listdate.add(executionSuccessList)
			listdate.add(executionFailureList)
			listdate.add(executionUndefinedList)
			listdate.add(executionNotExecutedList)
		}
		def mapData = [listdate:listdate, execName: executionList?.name, yCount : scriptGrpSize]
		render mapData as JSON
	}
	
	def populateChartData(final Execution executionInstance){
		if(!executionInstance?.isPerformanceDone){
			executionService.setPerformance(executionInstance,request.getRealPath('/'))
		}
	}

	/**
	 * Shows the chart to draw the chart based on the benchmark data
	 * @return
	 */
	def getStatusBenchMarkData(){
				
		def executionList
		def timeList = []
		
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
			int scriptGrpSize = scriptGroupInstance?.scripts?.size()	
			def performanceList = []				
			executionList.each{ execution ->
				
				populateChartData(execution)
				Double timetotal = 0				
				execution?.executionresults?.each{ execResult ->
					performanceList = Performance.findAllByExecutionResultAndPerformanceType(execResult,"BENCHMARK")
					performanceList.each{ performance ->
						if(performance?.processValue){
							timetotal = timetotal + Double.parseDouble(performance?.processValue)
						}
					}
				}
				timeList.add(timetotal/1000)
			}
		}

		def mapData = [execName: executionList?.name, benchmark : timeList]
		render mapData as JSON
	}

	/**
	 * Shows the chart to draw the chart based on SystemDiagnostics
	 * @return
	 */
	def getStatusSystemDiagnosticsData(){

		def executionList
		def cpuMemoryList = []
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
	
			def performanceList = []
			def cpuValues = []
			def memoryValues = []
			def performanceSd
			String cpumemValue = ""
			String memValue = ""
			executionList.each{ execution ->
				populateChartData(execution)
				Double cpuTotal = 0
				Double memoryTotal = 0
				execution?.executionresults?.each{ execResult ->
					
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,"%CPU")
						if(performanceSd?.processValue){
							def cpuPercentage = 0
							try {
								cpuPercentage = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							cpuTotal = cpuTotal +  cpuPercentage
						}
						
						
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,"%MEMORY")
						if(performanceSd?.processValue){
							def memoryPercentage = 0
							try {
								memoryPercentage = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							memoryTotal = memoryTotal +  memoryPercentage
						}
						
				}
				cpuValues.add(cpuTotal)
				memoryValues.add(memoryTotal)
			}	
			cpuMemoryList.add(cpuValues)
			cpuMemoryList.add(memoryValues)			
		}
		def mapData = [execName: executionList?.name, systemDiag : cpuMemoryList]
		render mapData as JSON
	}

	/**
	 * Returns execution list
	 * @param scriptGroup
	 * @param deviceId
	 * @param maxRes
	 * @return
	 */
	def List<Execution> getExecutionList(final String scriptGroup, final String deviceId, final String maxRes){
		
		ScriptGroup scriptGroupInstance = ScriptGroup.findById(scriptGroup)
		Device deviceInstance = Device.findById(deviceId)

		int countRes = Integer.parseInt(maxRes)
		def c = Execution.createCriteria()
		List<Execution> executionList = c.list {
			and {
				eq("scriptGroup", scriptGroupInstance?.name)
				eq("device", deviceInstance?.stbName)
			}
			order("id", "desc")
			maxResults(countRes)			
		}
	}
	
	/**
	 * Returns execution list based on execution id's
	 * @param executionIds
	 * @return
	 */
	def List<Execution> getExecutionLists(final String executionIds){		
		def executionArray = executionIds.split(",")
		List<Execution> executionList = []
		Execution execution
		def executionInstance = Execution.findById(executionArray[0])
		def scriptGroup = executionInstance?.scriptGroup
		def counter = 0			
		executionArray.each{ executionId ->
			if(counter < 10){
				execution = Execution.findById(executionId)
				if(scriptGroup.equals(execution?.scriptGroup)){
					executionList << execution
				}
			}
			counter++
		}				
		return executionList
	}
	
	
}
