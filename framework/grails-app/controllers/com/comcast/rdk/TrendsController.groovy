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
		def executionName =  Execution?.findAllByIsBenchMarkEnabledAndIsSystemDiagnosticsEnabled('1','1')
		def execName = []
		executionName?.each { name->
			if(name.scriptGroup != null ){
				execName.add(name)
			}
		}
		/*List executionName = [] 			
		List<Execution> executionList = c.list {
			isNotNull("scriptGroup")
			maxResults(200)
			order("id", "desc")			
		}	
		[executionList : executionList]*/	
		[executionList : execName,startIndex:0,endIndex:8]
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
			
			scriptGrpSize = scriptGroupInstance.scriptList.size()
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
				//executionUndefinedResultList = ExecutionResult.findAllByExecutionAndStatus(execution,UNDEFINED_STATUS)
	
				int unexecutedScripts = scriptGrpSize - (executionSuccessResultList.size() + executionFailureResultList.size())// + executionUndefinedResultList.size())
	
				executionSuccessList.add(executionSuccessResultList.size())
				executionFailureList.add(executionFailureResultList.size())
				//executionUndefinedList.add(executionUndefinedResultList.size())
				executionNotExecutedList.add(unexecutedScripts)
			}
	
			listdate.add(executionSuccessList)
			listdate.add(executionFailureList)
			//listdate.add(executionUndefinedList)
			listdate.add(executionNotExecutedList)
		}
		def mapData = [listdate:listdate, execName: executionList?.name, yCount : scriptGrpSize]
		render mapData as JSON
	}
	
	def populateChartData(final Execution executionInstance){
		//if(!executionInstance?.isPerformanceDone){
			executionService.setPerformance(executionInstance,request.getRealPath('/'))
		//}
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
			int scriptGrpSize = scriptGroupInstance?.scriptList?.size()	
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
	def getStatusSystemDiagnosticsCPUData(){
		
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
	
			def cpuValues = []
			def cpuPercValues = []
			def performanceSd
			String cpumemValue = ""
			String memValue = ""
			executionList.each{ execution ->
				populateChartData(execution)
				Double cpuTotal = 0
				Double cpuPeak = 0
				int counter = 0
				execution?.executionresults?.each{ execResult ->
					counter ++
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,Constants.CPU_AVG)
						if(performanceSd?.processValue){
							def cpuAvg = 0
							try {
								cpuAvg = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							cpuTotal = cpuTotal +  cpuAvg
						}
						
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,Constants.CPU_PEAK)
						if(performanceSd?.processValue){
							def cpuPercentage = 0
							try {
								cpuPercentage = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							if(cpuPeak < cpuPercentage){
								cpuPeak = cpuPercentage
							}
						}
						
						
				}
				cpuValues.add(cpuTotal/counter)
				cpuPercValues.add(cpuPeak)
			}	
			cpuMemoryList.add(cpuValues)
			cpuMemoryList.add(cpuPercValues)
		}
		def mapData = [execName: executionList?.name, systemDiag : cpuMemoryList]
		render mapData as JSON
	}

	
	/**
	 * Shows the chart to draw the chart based on SystemDiagnostics
	 * @return
	 */
	def getStatusSystemDiagnosticsPeakMemoryData(){
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
	
			def memoryValues = []
			def memoryValues2 = []
			def memoryValues3 = []
			def performanceSd
			String cpumemValue = ""
			String memValue = ""
			executionList.each{ execution ->
				populateChartData(execution)
				Double cpuTotal = 0
				Double memoryAvailFirstTotal = 0
				Double memoryUsedPeakTotal = 0
				float memoryPercentagePeakTotal = 0
				int counter = 0
				execution?.executionresults?.each{ execResult ->
					counter ++
						
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,Constants.MEMORY_AVAILABLE_PEAK)
						if(performanceSd?.processValue){
							def memoryPercentage = 0
							try {
								memoryPercentage = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							memoryAvailFirstTotal = memoryAvailFirstTotal +  memoryPercentage
						}
						
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,Constants.MEMORY_USED_PEAK)
						if(performanceSd?.processValue){
							def memoryPercentage = 0
							try {
								memoryPercentage = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							memoryUsedPeakTotal = memoryUsedPeakTotal +  memoryPercentage
						}
						
				}
				memoryValues.add(memoryAvailFirstTotal/counter)
				memoryValues2.add(memoryUsedPeakTotal/counter)
			}
			cpuMemoryList.add(memoryValues)
			cpuMemoryList.add(memoryValues2)
		}
		def mapData = [execName: executionList?.name, systemDiag : cpuMemoryList]
		render mapData as JSON
	}
	
	/**
	 * Shows the chart to draw the chart based on SystemDiagnostics
	 * @return
	 */
	def getStatusSystemDiagnosticsMemoryPercData(){
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
	
			def memoryValues = []
			def memoryValues2 = []
			def memoryValues3 = []
			def performanceSd
			String cpumemValue = ""
			String memValue = ""
			executionList.each{ execution ->
				populateChartData(execution)
				Double cpuTotal = 0
				Double memoryPercPeakTotal = 0
				int counter = 0
				execution?.executionresults?.each{ execResult ->
					
						counter++
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,Constants.MEMORY_PERC_PEAK)
						if(performanceSd?.processValue){
							def memoryPercentage = 0
							try {
								memoryPercentage = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							memoryPercPeakTotal = memoryPercPeakTotal +  memoryPercentage
						}
						
						
				}
				memoryValues.add(memoryPercPeakTotal/counter)
			}
			cpuMemoryList.add(memoryValues)
		}
		def mapData = [execName: executionList?.name, systemDiag : cpuMemoryList]
		render mapData as JSON
	}

	/**
	 * Shows the chart to draw the line chart based on the execution status
	 * The chart display like three status - success , failure , Not Found 
	 *  
	 * @return
	 */
	def getStatusChartData1(){	 
		def listdate = []
		def executionSuccessList = []
		def executionFailureList = []
		def executionUndefinedList = []
		def executionNotExecutedList = []	
		def cpuMemoryList = []
		List<Execution> executionList
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		int scriptGrpSize
		int totalScriptGroupSize = 0 
		if(executionList){
			List<ExecutionResult> executionSuccessResultList
			List<ExecutionResult> executionFailureResultList
			List<ExecutionResult> executionUndefinedResultList
			executionList?.each{ execution ->
				scriptGrpSize = 0
				
				def scriptGroupName =  ScriptGroup.findByName(execution?.scriptGroup)
				if(  scriptGroupName){
					scriptGrpSize = scriptGroupName?.scriptList.size()	
					if( totalScriptGroupSize < scriptGrpSize ){
						totalScriptGroupSize = scriptGrpSize
					}					
				}
				populateChartData(execution)
				
				executionSuccessResultList = ExecutionResult.findAllByExecutionAndStatus(execution,SUCCESS_STATUS)
				executionFailureResultList = ExecutionResult.findAllByExecutionAndStatus(execution,FAILURE_STATUS)
				int unexecutedScripts = scriptGrpSize - (executionSuccessResultList.size() + executionFailureResultList.size())// + executionUndefinedResultList.size())
				executionSuccessList.add(executionSuccessResultList.size())
				executionFailureList.add(executionFailureResultList.size())
				executionNotExecutedList.add(unexecutedScripts)
			}
			listdate.add(executionSuccessList)
			listdate.add(executionFailureList)
			listdate.add(executionNotExecutedList)
		}
		def mapData = [listdate:listdate, execName: executionList?.name, yCount : totalScriptGroupSize, success : executionSuccessList , failure : executionFailureList , notFound : executionNotExecutedList]
		render mapData as JSON
	}
	
	
	/**
	 * Shows the chart to draw the line chart based on the benchmark data
	 * The  plotting the graph according to the timing info value.
	 * @return
	 */
	def getStatusBenchMarkData1(){	
	
		def executionList 
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		int sIndex = 0
		int eIndex = 0
		try {
			sIndex =  Integer.parseInt(params?.startIndex)
			eIndex = Integer.parseInt(params?.endIndex)
		} catch (Exception e) {
			e.printStackTrace()
		}
		Map valueMap = [:]
		List commonScripts = []
		List curList = []
		if(executionList && sIndex >= 0 && eIndex > 0 ){
			List scriptsList = []
			try{
				executionList?.each {  ex ->
					List  slist = []
					def sg = ScriptGroup.findByName(ex?.scriptGroup)
					slist.addAll(sg?.scriptList?.scriptName);
					scriptsList.add(slist);
				}
			}catch(Exception e ){
			
			}
			if(scriptsList?.size() > 0){
				commonScripts = scriptsList?.get(0)
				scriptsList?.each { tList ->
					commonScripts = commonScripts?.intersect(tList);
				}
			}
			def performanceSd
			if(commonScripts?.size() < eIndex){
				eIndex = commonScripts?.size()
			}
			curList = commonScripts?.subList(sIndex,eIndex)
			curList?.each {  scriptName ->
				executionList.each{ execution ->
					def exRes = ExecutionResult?.findByExecutionAndScript(execution,scriptName)
					performanceSd = Performance.findByExecutionResultAndPerformanceType(exRes,"BENCHMARK")
					def timingInfo   = 0
					if(performanceSd?.processValue){
						try {
							timingInfo = Double.parseDouble(performanceSd?.processValue)
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
					def valueList = valueMap?.get(execution?.name)
					if(valueList == null){
						valueList = []
						valueMap.put(execution?.name, valueList)
					}
					valueList?.add(timingInfo)
				}
			}
		}
		def mapData = [execName: valueMap?.keySet(), systemDiag : valueMap?.values() , scripts :curList , benchmark :valueMap?.values() ,maxSize : commonScripts?.size()]
		render mapData as JSON
	}
	
	/**
	 * Shows the chart to draw the line chart based on the CPU- Utilization  
	 * @return
	 */  
	def getStatusSystemDiagnosticsCPUData1(){
		def executionList
		List  cpuValues1 = []
	if(params?.executionIds){
		executionList = getExecutionLists(params?.executionIds)
	}
	else{
		executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
	}	
	int sIndex = 0
	int eIndex = 0
	try {
		sIndex =  Integer.parseInt(params?.startIndex)
		eIndex = Integer.parseInt(params?.endIndex)
	} catch (Exception e) {
		e.printStackTrace()
	}
	Map valueMap = [:]
	List commonScripts = []
	List curList = []
	if(executionList && sIndex >= 0 && eIndex > 0 ){		
		List scriptsList = []
		try{
		executionList?.each {  ex ->
			List  slist = []
			def sg = ScriptGroup.findByName(ex?.scriptGroup)
			slist.addAll(sg?.scriptList?.scriptName);
			scriptsList.add(slist);
		}
		}catch(Exception e){
		
		} 
		if(scriptsList?.size() > 0){
			commonScripts = scriptsList?.get(0)
			scriptsList?.each { tList ->
				commonScripts = commonScripts?.intersect(tList);
			}
		}		
		def performanceSd
		if(commonScripts?.size() < eIndex){
			eIndex = commonScripts?.size()
		}
		curList = commonScripts?.subList(sIndex,eIndex)
		curList?.each {  scriptName ->
			executionList.each{ execution ->
				def exRes = ExecutionResult?.findByExecutionAndScript(execution,scriptName)
				performanceSd = Performance.findByExecutionResultAndProcessName(exRes,Constants.CPU_PEAK)
				def cpuUtilization  = 0
				if(performanceSd?.processValue){
					try {
						cpuUtilization = Double.parseDouble(performanceSd?.processValue)
					} catch (Exception e) {
						e.printStackTrace()
					}
				}
				def valueList = valueMap?.get(execution?.name)
				if(valueList == null){
					valueList = []
					valueMap.put(execution?.name, valueList)
				}
				valueList?.add(cpuUtilization)
				
			}
		}
		}
		def mapData = [execName: valueMap?.keySet(), systemDiag : valueMap?.values() , scripts :curList , cpuValuesTest :valueMap?.values() ,maxSize : commonScripts?.size()]
		render mapData as JSON
	}
	/**
	 * Shows the chart to draw the line chart based on the Memory Utilization 
	 * @return
	 */
	def getStatusSystemDiagnosticsPeakMemoryData1(){		
		def executionList
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		int sIndex = 0
		int eIndex = 0		
		try {
			sIndex =  Integer.parseInt(params?.startIndex)
			eIndex = Integer.parseInt(params?.endIndex)
		} catch (Exception e) {
			e.printStackTrace()
		}		
		Map valueMap = [:]
		List commonScripts = []
		List curList = []
		if(executionList && sIndex >= 0 && eIndex > 0 ){
			
			List scriptsList = []
			try {
			executionList?.each {  ex ->
				List  slist = []
				def sg = ScriptGroup.findByName(ex?.scriptGroup)
				slist.addAll(sg?.scriptList?.scriptName);
				scriptsList.add(slist);
			}
			}catch (Exception e){
			
			}
			if(scriptsList?.size() > 0){
				commonScripts = scriptsList?.get(0)
				scriptsList?.each { tList ->
					commonScripts = commonScripts?.intersect(tList);
				}
			}	
			
			def performanceSd
			if(commonScripts?.size() < eIndex){
				eIndex = commonScripts?.size()
			}			
			curList = commonScripts?.subList(sIndex,eIndex)
			curList?.each {  scriptName ->
				executionList.each{ execution ->
					def exRes = ExecutionResult?.findByExecutionAndScript(execution,scriptName)
					performanceSd = Performance.findByExecutionResultAndProcessName(exRes,Constants.MEMORY_USED_PEAK)
					def memoryPercentage = 0
					if(performanceSd?.processValue){
						try {
							memoryPercentage = Double.parseDouble(performanceSd?.processValue)
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
					def valueList = valueMap?.get(execution?.name)
					if(valueList == null){
						valueList = []
						valueMap.put(execution?.name, valueList)
					}
					valueList?.add(memoryPercentage)
				}
			}
		}
		def mapData = [execName: valueMap?.keySet(), systemDiag : valueMap?.values() , scripts :curList , memoryValuesTest :valueMap?.values() ,maxSize : commonScripts?.size()]
		render mapData as JSON

	}

	/**
	 * Shows the chart to draw line chart based on the Memory Used Percentage 
	 * @return
	 */
	def getStatusSystemDiagnosticsMemoryPercData1(){
		def executionList
		
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}		
		int sIndex = 0
		int eIndex = 0
		try {
			sIndex =  Integer.parseInt(params?.startIndex)
			eIndex = Integer.parseInt(params?.endIndex)
		} catch (Exception e) {
			e.printStackTrace()
		}		
		Map valueMap = [:]
		List commonScripts = []
		List curList = []
		
		if(executionList && sIndex >= 0 && eIndex > 0 ){
			List scriptsList = []
			try{
			executionList?.each {  ex ->
				List  slist = []
				def sg = ScriptGroup.findByName(ex?.scriptGroup)
				slist.addAll(sg?.scriptList?.scriptName);
				scriptsList.add(slist);
			}
			}catch(Exception  e){
			
			}
			if(scriptsList?.size() > 0){
				commonScripts = scriptsList?.get(0)
				scriptsList?.each { tList ->
					commonScripts = commonScripts?.intersect(tList);
				}
			}	
			if(commonScripts?.size() < eIndex){
				eIndex = commonScripts?.size()
			}
			curList = commonScripts?.subList(sIndex,eIndex)		
			def performanceSd
			curList?.each {  scriptName ->
				executionList.each{ execution ->
					def exRes = ExecutionResult?.findByExecutionAndScript(execution,scriptName)
					performanceSd = Performance.findByExecutionResultAndProcessName(exRes,Constants.MEMORY_PERC_PEAK)
					def memoryPercentage = 0
					if(performanceSd?.processValue){
						try {
							memoryPercentage = Double.parseDouble(performanceSd?.processValue)
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
					def valueList = valueMap?.get(execution?.name)
					if(valueList == null){
						valueList = []
						valueMap.put(execution?.name, valueList)
					}
					valueList?.add(memoryPercentage)
				}
			}
		}
		def mapData = [execName: valueMap?.keySet(), systemDiag : valueMap?.values() , scripts :curList , memoryValuesTest :valueMap?.values() ,maxSize : commonScripts?.size()]
		render mapData as JSON
	}

	/**
	 * Shows the chart to draw the chart based on Paging data
	 * @return
	 */
	def getPagingData(){
		
		def executionList
		def systemDiagList = []
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
	
			def pageInValues = []
			def pageOutValues = []
			def performanceSd
		
			executionList.each{ execution ->
				populateChartData(execution)
				Double pageInTotal = 0
				Double pageOutTotal = 0
				execution?.executionresults?.each{ execResult ->
					
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,"PAGING : pgpgin/s")
						if(performanceSd?.processValue){
							def pageInVal = 0
							try {
								pageInVal = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							pageInTotal = pageInTotal +  pageInVal
						}
						
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,"PAGING : pgpgout/s")
						if(performanceSd?.processValue){
							def pageOutVal = 0
							try {
								pageOutVal = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							pageOutTotal = pageOutTotal +  pageOutVal
						}
				}
				pageInValues.add(pageInTotal)
				pageOutValues.add(pageOutTotal)
			}
			systemDiagList.add(pageInValues)
			systemDiagList.add(pageOutValues)
		}
		def mapData = [execName: executionList?.name, systemDiag : systemDiagList]
		render mapData as JSON

	}
	
	/**
	 * Shows the chart to draw the chart based on Swap Data
	 * @return
	 */
	def getSwapData(){

		def executionList
		def systemDiagList = []
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
			def swapValues = []
			def performanceSd
	
			executionList.each{ execution ->
				populateChartData(execution)
				Double swapTotal = 0
				Double loadAvgTotal = 0
				execution?.executionresults?.each{ execResult ->											
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,"SWAPING")
						if(performanceSd?.processValue){
							def swapVal = 0
							try {
								swapVal = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							swapTotal = swapTotal +  swapVal
						}							
				}
				swapValues.add(swapTotal)
			}
			systemDiagList.add(swapValues)
		}
		def mapData = [execName: executionList?.name, systemDiag : systemDiagList]
		render mapData as JSON
	}
/**
 * Plot the graph using the load average data
 * @return
 */
	
	def getLoadAverage(){
		
		def executionList
		def systemDiagList = []
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		
		executionList?.intersect(systemDiagList)
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
			def loadAvgValues = []
			def performanceSd
	
			executionList.each{ execution ->
				populateChartData(execution)
				
				Double loadAvgTotal = 0
				execution?.executionresults?.each{ execResult ->

						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,"LOAD AVERAGE")
						if(performanceSd?.processValue){
							def loadAvgVal = 0
							try {
								loadAvgVal = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							loadAvgTotal = loadAvgTotal +  loadAvgVal
						}
				}
				loadAvgValues.add(loadAvgTotal)
			}
			systemDiagList.add(loadAvgValues)
		}
		def mapData = [execName: executionList?.name, systemDiag : systemDiagList]
				
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
		//performance data enabled execution names
		def executionNameList = Execution.findAllByIsBenchMarkEnabledAndIsSystemDiagnosticsEnabled('1','1')
		def executionNames=[]
		int executionNameCount = 0
		executionNameList.each { execName ->
			if(executionNameCount <= countRes){
				if(execName.scriptGroup.toString().equals(scriptGroupInstance?.toString()) && execName.device.toString().equals(deviceInstance?.toString())){
					executionNames.add(execName)
					executionNameCount++
				}
			}
		}
		/*def c = Execution.createCriteria()
		List<Execution> executionList = c.list {
			and {
				eq("scriptGroup", scriptGroupInstance?.name)
				eq("device", deviceInstance?.stbName)
			}
			order("id", "desc")
			maxResults(countRes)			
		}*/
		return executionNames
	}
	
	/**
	 * Returns execution list based on execution id's
	 * @param executionIds
	 * @return
	 */
	def List<Execution> getExecutionLists(final String executionIds){
		def  executionArray = executionIds.split(",")
		List<Execution> executionList = []
		Execution execution
		Execution executionInstance = Execution.findById(executionArray[0])
		//def scriptGroup = executionInstance?.scriptGroup
		def counter = 0
		executionArray.each{ executionId ->			
			if(counter < 10){
					execution = Execution.findById(executionId)	
					if(execution?.scriptGroup){	
					//if(scriptGroup.equals(execution?.scriptGroup)){
						executionList << execution
					//}
					}
			}
			counter++
		}
		return executionList
	}
	
	
}
