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
import static org.quartz.DateBuilder.*
import static org.quartz.TriggerBuilder.*
import static org.quartz.CronScheduleBuilder.*
import static org.quartz.TriggerKey.*
import static org.quartz.JobKey.*
import org.apache.shiro.SecurityUtils
import grails.converters.JSON
import groovy.json.JsonSlurper
import java.text.DateFormat
import java.text.SimpleDateFormat
import org.quartz.JobDetail
import org.quartz.Scheduler
import org.quartz.SimpleTrigger
import org.quartz.Trigger
import org.quartz.Job
import org.quartz.JobBuilder
import org.quartz.impl.triggers.SimpleTriggerImpl
import rdk.test.tool.*
import java.util.date.*
import com.google.gson.JsonArray
import com.google.gson.JsonObject

import groovy.xml.MarkupBuilder
import org.custommonkey.xmlunit.*

/**
 * A class that handles the Execution of scripts.
 * @author sreejasuma
 */
class ExecutionController {
    
    def scriptexecutionService
    /**
     * Injects quartz scheduler
     */
    def quartzScheduler
    /**
     * Injects the executionService.
     */
    def executionService             
    /**
     * Injects the grailsApplication.
     */
    def grailsApplication 
	
	def utilityService
	
	def exportService   // Export service provided by Export plugin
	
	def deviceStatusService
	
	def primitivetestService
	
	public static Object  lock = new Object()
	private static int execIdCounter = 0
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
	public static final String EXPORT_SHEET_NAME 			= "Execution_Results"
	public static final String EXPORT_FILENAME 				= "ExecutionResults-"
	public static final String EXPORT_EXCEL_FORMAT 			= "excel"
	public static final String EXPORT_EXCEL_EXTENSION 		= "xls"
	public static final String MARK_ALL_ID1 				= "markAll1"
	public static final String MARK_ALL_ID2 				= "markAll2"
	public static final String UNDEFINED					= "undefined"
	

    def index() {
		
        redirect(action: "create")
    }
    /**
     * Method to unschedule a quartz job
     */
    def unScheduleJob(){       
        def countVariable = 0
        def jobDetailInstance   
        if(params?.listCount){ // to delete record(s) from list.gsp            
            for (iterateVariable in params?.listCount){
                countVariable++
                if(params?.("chkbox"+countVariable) == KEY_ON){                    
                    def idDb = params?.("id"+countVariable).toLong()
                    jobDetailInstance = JobDetails.get(idDb)
                    def triggname = jobDetailInstance?.triggerName
                    def jobname = jobDetailInstance?.triggerName
                    quartzScheduler.unscheduleJob(triggerKey(triggname));
                    quartzScheduler.deleteJob(jobKey(jobname));                                        
                    if (jobDetailInstance) {                            
                          jobDetailInstance.delete(flush: true)                           
                    }                    
                }
            }                
        }
        render(template: "scheduleTable", model: [jobDetailList : JobDetails.list()])        
    }

    /**
     * Method to create a cron tab based on the selection of
     * schedule type in the gsp page by the user
     */    
    def createCronScheduleTab(def params) {
        String status = SUCCESS_STATUS
        String cronschedule = ""
        String queryString = ""
        String weekDay = params?.weekDay
        String weekDays = ""
        switch ( params?.reccurGroup ) {
            case KEY_DAILY:
                switch(params?.reccurDaily){
                    case KEY_DAILYDAYS:
                        if((params?.dailyDaysCount).isEmpty()){
                            cronschedule = message(code: 'schedule.novalue.dailydays')
                            status = ERROR_STATUS
                        }
                        else{
                            queryString = "Every ${params?.dailyDaysCount} days"
                            cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} */${params?.dailyDaysCount} * ?"
                        }
                        break
                    case KEY_DAILYWEEKDAY:
                        queryString = "All Weekdays"
                        cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? * 2-6"
                        break
                    default:
                        cronschedule = message(code: 'schedule.error.dailydays')
                        status = ERROR_STATUS
                        break
                }
                break
        
            case KEY_WEEKLY:
                if(weekDay){
                    if(weekDay instanceof String){
                        queryString = "Weekly on ${weekDay}"
                        cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? * ${weekDay}"
                    }
                    else{
                        weekDay.each{ it->
                            weekDays = weekDays+it+COMMA_SEPERATOR
                        }
                        weekDays = weekDays.substring( 0, (weekDays.size()-1) )
                        queryString = "Weekly on ${weekDays}"
                        cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? * ${weekDays}"
                    }
                }
                else{                    
                    cronschedule = message(code: 'schedule.error.weekly')
                    status = ERROR_STATUS
                }
                break
        
            case KEY_MONTHLY:
             
                switch(params?.reccurMonthly){
                    case KEY_MONTHLYDAYS:
                        if((params?.monthlyMonthCount).isEmpty() || (params?.monthlyDaysCount).isEmpty() ){
                            cronschedule = message(code: 'schedule.novalue.monthly')
                            status = ERROR_STATUS
                        }
                        else{
                            queryString = "Day ${params?.monthlyDaysCount} of every ${params?.monthlyMonthCount} month"
                            cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ${params?.monthlyDaysCount} */${params?.monthlyMonthCount} ?"
                        }
                        break
                    case KEY_MONTHLYCOMPLEX:
                        if((params?.monthlyMonthCnt).isEmpty()){
                            cronschedule = message(code: 'schedule.empty.monthly')
                            status = ERROR_STATUS
                        }
                        else{
                            if((params?.daytype).equals( KEY_LASTDAY )){
                                queryString = "Last  ${executionService.getDayName(params?.dayName)} of every ${(params?.monthlyMonthCnt)} month"                                
                                cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? */${params?.monthlyMonthCnt} ${params?.dayName}${params?.daytype}"
                            }
                            else{
                                queryString = "${executionService.getOptionName(params?.daytype)} ${executionService.getDayName(params?.dayName)} of every ${params?.monthlyMonthCnt} month"
                                cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? */${params?.monthlyMonthCnt} ${params?.dayName}#${params?.daytype}"
                            }
                        }
                        break
                        
                    default:
                        cronschedule = message(code: 'schedule.error.monthly')
                        status = ERROR_STATUS
                        break
                }
                break

            default: break             
        } 
        return [status,cronschedule,queryString]
    }
    
    /**
     * Schedule a quartz job
     * @return
     */
    def scheduleOneOff() {
        
         String cronschedule
         String startDateString = (params?.startdate).toString()
         String endDateString = (params?.enddate).toString()
         Date startDate = new SimpleDateFormat(SCHEDULE_DATEFORMAT).parse(startDateString)
         Date endDate = new SimpleDateFormat(SCHEDULE_DATEFORMAT).parse(endDateString)
         String status
         String resultString
         String queryString
         String jobName = KEY_JOB+System.currentTimeMillis().toString()
         String triggerName = KEY_TIGGER+System.currentTimeMillis().toString()
 
         List<String> scriptList = new ArrayList<String>()
         String scheduleDate = (params?.testdate).toString()
         java.util.Date date = new SimpleDateFormat(SCHEDULE_DATEFORMAT).parse(scheduleDate)
         if( Date.getMillisOf( date ) < System.currentTimeMillis() && (params?.scheduleGroup.equals( KEY_ONETIME )) ){
             render message(code: 'schedule.valid.date')
             return
         }   
         else if(Date.getMillisOf( startDate ) < System.currentTimeMillis() && (params?.scheduleGroup.equals( KEY_RECCURENCE ))){
             render message(code: 'schedule.valid.startdate')
             return
         }
         else if((endDate < startDate) && (params?.scheduleGroup.equals( KEY_RECCURENCE ))){
             render message(code: 'schedule.valid.startenddate')
             return
         }                   
         else{
 
             String[] scriptIdArray = (params?.scriptlist).split(COMMA_SEPERATOR)
             scriptIdArray.each{ scriptid ->
                 if(!(scriptid.isEmpty()))
                 {
                     scriptList.add(scriptid)
                 }
             }

            JobDetail job = JobBuilder.newJob(JobSchedulerService.class)
             .withIdentity(jobName).build();
             
             Trigger trigger
             if(params?.scheduleGroup.equals( KEY_ONETIME )){
                 queryString = KEY_ONETIME
                 startDate = date
                 endDate = null
                 trigger = new SimpleTriggerImpl(triggerName, date)
             }
             else if(params?.scheduleGroup.equals( KEY_RECCURENCE )){

                (status, resultString, queryString) = createCronScheduleTab(params)
                if(status.equals(ERROR_STATUS)){
                    render resultString
                    return
                }
                else{
                    cronschedule = resultString
                }
                
                trigger = newTrigger()
                    .withIdentity(triggerName)
                    .withSchedule(cronSchedule(cronschedule))
                    .startAt(startDate)
                    .endAt(endDate)
                    .forJob(jobName)
                    .build();
            }             
             try{
                 quartzScheduler.scheduleJob(job, trigger)
             }
             catch(Exception qEx){
                 render message(code: 'schedule.invalid.dates')
                 return
             }
			 			 
			 int repeatCount = (params?.repeatCount).toInteger()
			 
             JobDetails jobDetails = new JobDetails()
             jobDetails.jobName = jobName
             jobDetails.triggerName = triggerName
             jobDetails.script = scriptList
             jobDetails.scriptGroup = params?.scriptGroup
             jobDetails.device = params?.deviceId
             jobDetails.deviceGroup = null
             jobDetails.realPath = getRealPath()
             jobDetails.appUrl = getApplicationUrl()
             jobDetails.filePath = "${request.getRealPath('/')}//fileStore"
             jobDetails.queryString = queryString
             jobDetails.startDate = startDate
             jobDetails.endDate = endDate
             jobDetails.oneTimeScheduleDate = date
			 jobDetails.isSystemDiagnostics = params?.isSystemDiagnostics
			 jobDetails.isBenchMark = params?.isBenchMark
			 jobDetails.rerun = params?.rerun
			 jobDetails.repeatCount = repeatCount
			 jobDetails.groups = utilityService.getGroup()
             jobDetails.save(flush:true)
			 def jobDetailList = JobDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
             render(template: "scheduleTable", model: [jobDetailList : jobDetailList])
             return
         }
     }

    /**
     * Method to display the schedule page with previously scheduled job details
     * @param max
     * @return
     */
    def showSchedular(Integer max){
		
        params.max = Math.min(max ?: 10, 100)	
		def repeatCount = (params?.repeatId)
		def rerun = params?.rerun
		
        [scripts : params?.scripts, device : params?.deviceId, scriptGroup : params?.scriptGroup, jobDetailList : JobDetails.list(), 
			jobInstanceTotal: JobDetails.count(), isSystemDiagnostics : params?.systemDiagnostics, isBenchMark : params?.benchMarking, rerun : rerun, repeatCount : repeatCount]
    }
	
    /**
     * Creates the execution page with the listing of devices 
     * @param max
     * @return
     */
    def create(Integer max) {

		params.max = Math.min(max ?: 10, 100)

		def deviceInstanceList = Device.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(),[order: 'asc', sort: 'stbName'])
		def executionInstanceList = Execution.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(),params)
		def executionInstanceListCnt = Execution.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
	
        def devices = Device.list([order: 'asc', sort: 'stbName'])
        
        if(params?.devicetable) {
            // This is called from execution-resolver.js loadXmlDoc. This is for automatic page refresh.
            def result = [executionInstanceList : executionInstanceList, executorInstanceTotal: executionInstanceListCnt?.size()]
            render view:"executionhistorytable", model:result
            return
        }       
        else if(params?.devicestatustable) {  
            // This is called from execution-resolver.js loadXmlDoc. This is for automatic page refresh.   
     
            def result1 = [url: getApplicationUrl(), deviceList : deviceInstanceList, deviceInstanceTotal: deviceInstanceList?.size()]
            render view:"devicelist", model:result1
            return
        }
		else{
			try{
				DeviceStatusUpdater.updateDeviceStatus(grailsApplication,deviceStatusService);
			}catch(Exception e){
				e.printStackTrace();
			}
			deviceInstanceList = Device.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(),[order: 'asc', sort: 'stbName'])
		}
        [url : getApplicationUrl(), deviceList : deviceInstanceList, error: params.error, executionInstanceList : executionInstanceList, executorInstanceTotal: executionInstanceListCnt?.size(),
            jobDetailList : JobDetails?.list(), jobInstanceTotal: JobDetails?.count(), deviceInstanceTotal: deviceInstanceList?.size()]
    
    }

    /**
     * Show the device IP and the scripts based on the selection
     * of device name from the list
     * @return
     */
    def showDevices(){
        def device = Device.get( params?.id )
        // def scripts = Script.list([order: 'asc', sort: 'name'])
        // def scriptGrp = ScriptGroup.list([order: 'asc', sort: 'name'])
		
		def scripts = Script.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(),[order: 'asc', sort: 'name'])
		def scriptGrp = ScriptGroup.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(),[order: 'asc', sort: 'name'])
		
		DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)		
        Calendar cal = Calendar.getInstance()
        [datetime :  dateFormat.format(cal.getTime()).toString(), device : device, scriptGrpList : scriptGrp, scriptList : scripts]
    }

    /**
     * Method to get the current date and time from server
     * to display in execution name field of execution page
     * @return
     */
    def showDateTime(){
        def listdate = []
        DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
        Calendar cal = Calendar.getInstance()        
        listdate << dateFormat.format(cal.getTime()).toString()
        render listdate as JSON
    }
    
    /**
     * Method to get the current url and to create
     * new url upto the application name
     * @return
     */
    def String getApplicationUrl(){
        String currenturl = request.getRequestURL().toString();
        String[] urlArray = currenturl.split( URL_SEPERATOR );
        String url = urlArray[INDEX_ZERO] + DOUBLE_FWD_SLASH + urlArray[INDEX_TWO] + URL_SEPERATOR + urlArray[INDEX_THREE]
        return url
    }

    /**
     * Method to return the real path of the application
     * @return
     */
    def String getRealPath(){           
     /*   String s = request.getSession().getServletContext().getRealPath("/") 
        s = s.replace( '\\', '/' )
        return s  */
        return request.getSession().getServletContext().getRealPath(URL_SEPERATOR) 
    }     
    
    /**
     * REST interface to support script execution with the parameters passed.
     * @param stbName
     * @param boxType
     * @param suiteName
     * @return
     */
	  def thirdPartyTest(final String stbName, final String boxType, final String suiteName, final String callbackUrl ){
        String htmlData = ""
        String outData = ""
        String url = ""
        def execName = ""
		
		JsonObject jsonOutData = new JsonObject()
		ScriptGroup scriptGroup = ScriptGroup.findByName(suiteName)
		def scriptStatusFlag				
        Device deviceInstance
		def deviceNotExistStatus = ""
		def deviceNotExistCnt = 0
		def deviceList = stbName.split(',')
		def executionNameForCheck
		deviceList.each{
			
			String stbname = it.toString().trim()
			deviceInstance = Device.findByStbName(stbname)			
			if(deviceInstance){
			
			  if(deviceInstance?.boxType?.name.equals(boxType.trim())){
			  	
				if(scriptGroup){
					scriptGroup?.scripts?.each{ script ->
						/**
						 * Checks whether atleast one script matches with the box type of device.
						 * If so execution will proceed with that one script
						 */
						if(executionService.validateScriptBoxType(script,deviceInstance)){
							scriptStatusFlag = true
						}
					}
					if(scriptStatusFlag){
		     
							if((deviceInstance.deviceStatus.equals( Status.FREE ))){
			                   
									def scriptname
									def deviceName
									ExecutionDevice executionDevice
				                    def execution                
				                    url = getApplicationUrl()
				                    String filePath = "${request.getRealPath('/')}//fileStore"
				                    def executionSaveStatus = true
									/**
									 * Even if there is multiple devices, the execution instance need to be created only once.
									 * 'executionNameForCheck' is used to bypass the creation of execution instance
									 */
									if(!executionNameForCheck){
					                    DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
					                    Calendar cal = Calendar.getInstance() 
										deviceName = deviceInstance?.stbName             
					                    execName = CI_EXECUTION+deviceName+dateFormat.format(cal.getTime()).toString()
										
										if(deviceList.size() > 1 ){
											executionNameForCheck = execName
											deviceName = MULTIPLE
										}	
																			
										//execName = execName 
										executionSaveStatus = scriptexecutionService.saveExecutionDetails(execName, scriptname, deviceName, scriptGroup)
									}
									if(executionSaveStatus){
										execution = Execution.findByName(execName)
										try{
											executionDevice = new ExecutionDevice()
											executionDevice.execution = execution
											executionDevice.dateOfExecution = new Date()
											executionDevice.device = deviceInstance?.stbName
											executionDevice.deviceIp = deviceInstance?.stbIp
											executionDevice.status = UNDEFINED_STATUS
											executionDevice.save(flush:true)
										}
										catch(Exception e){
											//e.printStackTrace()
										}
										String getRealPathString  = getRealPath()											
										scriptexecutionService.executeScriptGroup(scriptGroup, boxType, execName, executionDevice?.id.toString(), deviceInstance, url, filePath, getRealPathString, callbackUrl )										
									}
									else{
										deviceNotExistCnt++
										outData = outData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
			                    
				            }
				            else if(deviceInstance.deviceStatus.equals( Status.ALLOCATED )){
								deviceNotExistCnt++
				                outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
				            }
							else if(deviceInstance.deviceStatus.equals( Status.NOT_FOUND )){
								deviceNotExistCnt++
								outData = outData + " Device ${deviceInstance?.stbName} is not up/ Agent is not running"
							}
							else if(deviceInstance.deviceStatus.equals( Status.HANG )){
								deviceNotExistCnt++
								outData = outData + " Device ${deviceInstance?.stbName} is hanged"
							}
							else if(deviceInstance.deviceStatus.equals( Status.BUSY )){
								deviceNotExistCnt++
								outData = outData + " Device ${deviceInstance?.stbName} is Busy"
							}							
						}
						else{
							deviceNotExistCnt++
							outData = outData +" BoxType of Scripts in ScriptGroup is not matching with BoxType of Device ${deviceInstance?.stbName}"
						}
					}
					else{
						deviceNotExistCnt++
						outData = outData + " Script Group does not exist"
					}
			  	  }
			  	  else{
						deviceNotExistCnt++
						outData = outData + " Mismatch between the device ${stbname} and box type ${boxType}"
				  }						
			}
	        else{				
				deviceNotExistCnt++
	            outData = outData + " - Device ${it} not found"
	        }   
	  }

        if(deviceNotExistCnt < deviceList.size()){
          //  url = url + "/execution/showResult?execName=${execName}&scrGrp=${scriptGroup?.id}"
			url = url + "/execution/thirdPartyJsonResult?execName=${execName}"			
			jsonOutData.addProperty("status", "RUNNING"+outData);
			jsonOutData.addProperty("result", url);
        }
        else{
            url = outData
			jsonOutData.addProperty("status", "FAILURE");
			jsonOutData.addProperty("result", url);
        }
        render jsonOutData        
    }

	def getDeviceStatusList(){
		def deviceList = Device.list()
		JsonObject devices = new JsonObject()
		deviceList.each{ device ->
			devices.addProperty(device.stbName.toString()+LEFT_PARANTHESIS+device.stbIp.toString()+RIGHT_PARANTHESIS+LEFT_PARANTHESIS+device.boxType.toString()+RIGHT_PARANTHESIS, device.deviceStatus.toString())
		}
		render devices
	}
	
	def getDeviceStatus(final String stbName, final String boxType){
		JsonObject device = new JsonObject()
		if(stbName && boxType)	{
			def deviceInstance = Device.findByStbName(stbName)//,BoxType.findByName(boxType.trim()))			
			device.addProperty(deviceInstance.stbName.toString()+LEFT_PARANTHESIS+deviceInstance.stbIp.toString()+RIGHT_PARANTHESIS, deviceInstance.deviceStatus.toString())
		}
		render device		
	}
	
	def thirdPartyJsonResult(final String execName, final String appurl ){
		JsonArray jsonArray = new JsonArray()
		JsonObject compNode
		JsonObject deviceNode
		JsonObject executionNode
		String appUrl = appurl
		String url
		appUrl = getApplicationUrl() + "/execution/getDetailedTestResult?execResId="
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
					execStatus = "InProgress"
				}
								
				executionNode.addProperty("ExecutionStatus",execStatus.toString())
				executionNode.add("DEVICES", jsonArray)
			}
		render executionNode
	}
	
    /**
     * Execute the script
     * @return
     */
    def executeScriptMethod() {		
		def exId
        Script scriptInstance
        def scriptGroupInstance
        def scriptStatus = true
        Device deviceInstance = Device.findById(params?.id, [lock: true])
        String htmlData = ""
        def deviceId
		def executionName
		def scriptType = params?.myGroup	
		def deviceList = []
		def deviceName
		ExecutionDevice executionDevice = new ExecutionDevice()
		if(params?.devices instanceof String){
			deviceList << params?.devices
			deviceInstance = Device.findById(params?.id, [lock: true])
			deviceName = deviceInstance?.stbName
		}
		else{
			(params?.devices).each{ deviceid ->
				deviceList << deviceid
			}
			deviceName = MULTIPLE
		}
		
		if(params?.execName){
			executionName = params.execName
		}
		else{
			executionName = params?.name
		}
		int repeatCount = (params?.repeatNo).toInteger()
		
        def executionInstance = Execution.findByName(executionName)
        if(!(params?.name)){
            htmlData = message(code: 'execution.name.blank')
        }
        else if(executionInstance){
            htmlData = message(code: 'execution.name.duplicate')
        }
        else if(deviceInstance?.deviceStatus.toString().equals(Status.BUSY.toString())){
            htmlData = message(code: 'execution.script.running')
        }
		else if(!params?.scriptGrp && !params?.scripts){
			htmlData = message(code: 'execution.noscript.selected')
		}	
		else if(repeatCount == 0){
			htmlData = "Give a valid entry in repeat"
		}	
        else{
			
        	StringBuilder output = new StringBuilder();
			try{
			def isBenchMark = "false"
			def isSystemDiagnostics = "false"
			if(params?.systemDiagnostics.equals("on")){
				isSystemDiagnostics = "true"
			}
			if(params?.benchMarking.equals("on")){
				isBenchMark = "true"
			}
            def scriptName
            String url = getApplicationUrl()
            String filePath = "${request.getRealPath('/')}//fileStore"   
			def execName
			def executionNameForCheck
			for(int i = 0; i < repeatCount; i++ ){ 
				executionNameForCheck = null
				deviceList.each{ device ->
					deviceInstance = Device.findById(device)
					def executionSaveStatus = true
					def execution = null
					def scripts = null
					deviceId = deviceInstance?.id
					if(scriptType == SINGLE_SCRIPT){
						scripts = params?.scripts
						if(scripts instanceof String){
							scriptInstance = Script.findById(params?.scripts,[lock: true])
							scriptStatus = executionService.validateScriptBoxType(scriptInstance,deviceInstance)
							scriptName = scriptInstance?.name
						}
						else{
							scriptName = MULTIPLESCRIPT
						}
					}else{
						scriptGroupInstance = ScriptGroup.findById(params?.scriptGrp,[lock: true])
					}
					if(scriptStatus){
						if(!executionNameForCheck){
							if(i > 0){
								execName = executionName + UNDERSCORE +i
							}
							else{
								execName = executionName
							}
							executionSaveStatus = executionService.saveExecutionDetails(execName, scriptName, deviceName, scriptGroupInstance)
							if(deviceList.size() > 0 ){
								executionNameForCheck = execName
							}
						}
						else{
							execution = Execution.findByName(executionNameForCheck)
							execName = executionNameForCheck
						}
						if(executionSaveStatus){
							try{
								executionDevice = new ExecutionDevice()
								executionDevice.execution = Execution.findByName(execName)
								executionDevice.dateOfExecution = new Date()
								executionDevice.device = deviceInstance?.stbName
								executionDevice.deviceIp = deviceInstance?.stbIp
								executionDevice.status = UNDEFINED_STATUS
								executionDevice.save(flush:true)
							}
							catch(Exception e){
								e.printStackTrace()
							}

							def scriptId
							if((!(params?.scriptGrp)) && (!(params?.scripts))){
								render ""
								return
							}
							else{								
								executionService.executeVersionTransferScript(request.getRealPath('/'),filePath,execName, executionDevice?.id, deviceInstance?.stbIp, deviceInstance?.logTransferPort)
							}
							int scriptGrpSize = 0
							int scriptCounter = 0
							def isMultiple = "true"
							if(params?.myGroup == TEST_SUITE){
								scriptGroupInstance = ScriptGroup.findById(params?.scriptGrp,[lock: true])								
								scriptCounter = 0
								List<Script> validScriptList = new ArrayList<Script>()
								scriptGroupInstance.scripts.each { script ->									
									if(executionService.validateScriptBoxType(script,deviceInstance)){
										validScriptList << script										
									}												
								}
								scriptGrpSize = validScriptList?.size()
								validScriptList.each{ scriptObj ->
									scriptCounter++
									if(scriptCounter == scriptGrpSize){
										isMultiple = "false"
									}
									htmlData = executeScript(execName, executionDevice, scriptObj , deviceInstance , url, filePath, getRealPath(), isBenchMark, isSystemDiagnostics,executionName,isMultiple)
									/*if(isMultiple.equals("false")){
										Execution.withTransaction {
											Execution executionInstance1 = Execution.findByName(execName)
											executionInstance1.executionStatus = "COMPLETED"
											executionInstance1.save(flush:true)
										}
									}*/
									output.append(htmlData)
									Thread.sleep(6000)
								}						
							}
							else if(params?.myGroup == SINGLE_SCRIPT){
								if(scripts instanceof String){
									scriptInstance = Script.findById(params?.scripts,[lock: true])
									scriptId = scriptInstance?.id
									isMultiple = "false"
									htmlData = executeScript(execName, executionDevice, scriptInstance , deviceInstance , url, filePath, getRealPath(), isBenchMark, isSystemDiagnostics,executionName,isMultiple)									
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
											isMultiple = "false"
										}
										
										htmlData = executeScript(execName, executionDevice, script , deviceInstance , url, filePath, getRealPath(), isBenchMark, isSystemDiagnostics,executionName,isMultiple)
									/*	if(isMultiple.equals("false")){
											Execution.withTransaction {
												Execution executionInstance1 = Execution.findByName(execName)
												executionInstance1.executionStatus = "COMPLETED"
												executionInstance1.save(flush:true)
											}
										}*/
										output.append(htmlData)
										Thread.sleep(6000)
									}
								}
							}
							else{
								render ""
								return
							}
						}
					}
					else{
						htmlData = message(code: 'execution.boxtype.nomatch')
						output.append(htmlData)
					}
//					render htmlData
					htmlData = ""					
				}
				/**
				 * Re run on failure
				 */
				def executionObj = Execution.findByName(execName)
				def executionDeviceObj = ExecutionDevice.findAllByExecutionAndStatusNotEqual(executionObj, SUCCESS_STATUS)

				if((executionDeviceObj.size() > 0 ) && (params?.rerun)){
					htmlData = reRunOnFailure(request.getRealPath('/'),filePath,execName,executionName)
					output.append(htmlData)
				}
			}			
			}finally{
				deleteOutputFile(executionName)
			}
			htmlData = output.toString()	
					
        }
		render htmlData
    }

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
	 * Re run the tests if the status of script execution is not failure
	 * @param realPath
	 * @param filePath
	 * @param execName
	 * @return
	 */
	def reRunOnFailure(final String realPath, final String filePath, final String execName,final String uniqueExecutionName){
		Thread.sleep(10000)
		Execution executionInstance = Execution.findByName(execName)
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
						executionSaveStatus = executionService.saveExecutionDetails(newExecName, scriptName, deviceName, scriptGroupInstance)
						cnt++
						rerunExecutionInstance = Execution.findByName(newExecName)
					}				
					if(executionSaveStatus){
						
						ExecutionDevice executionDevice = new ExecutionDevice()
						executionDevice.execution = rerunExecutionInstance
						executionDevice.device = deviceInstance?.stbName
						executionDevice.deviceIp = deviceInstance?.stbIp
						executionDevice.dateOfExecution = new Date()
						executionDevice.status = UNDEFINED_STATUS
						executionDevice.save(flush:true)
						executionService.executeVersionTransferScript(realPath, filePath, newExecName, executionDevice?.id, deviceInstance.stbIp, deviceInstance?.logTransferPort)
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
							if(executionService.validateScriptBoxType(scriptInstance,deviceInstance)){
								htmlData = executeScript(newExecName, executionDevice, scriptInstance, deviceInstance, getApplicationUrl(), filePath, getRealPath(),"false","false",uniqueExecutionName,isMultiple)
							}
						}
					}
				}
			}	
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

        String scriptData = executionService.convertScriptFromHTMLToPython(scriptInstance.scriptContent)

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
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
			}
			executionService.updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff)
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
							"true"
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
		if(isBenchMark.equals("true") || isSystemDiagnostics.equals("true")){
			new File("${request.getRealPath('/')}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
			performanceFilePath = "${request.getRealPath('/')}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}//"
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
    
	def showLogFiles(){		
		def logFileNames = executionService.getLogFileNames(request.getRealPath('/'), params?.execId, params?.execDeviceId)
		render(template: "logFileList", model: [execId : params?.execId, execDeviceId : params?.execDeviceId, logFileNames : logFileNames])
	}
	
	def showCrashLogFiles(){
		def crashlogFileNames = executionService.getCrashLogFileNames(request.getRealPath('/'), params?.execId, params?.execDeviceId)
		render(template: "crashLogFileList", model: [execId : params?.execId, execDeviceId : params?.execDeviceId, logFileNames : crashlogFileNames])
	}
						
    /**
     * Method to display the script execution details in the popup.
     * @return
     */
    def showLog(){
        Execution executionInstance = Execution.findById(params?.id) 
		if(!executionInstance.isPerformanceDone){
			executionService.setPerformance(executionInstance,request.getRealPath('/'))
		}
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
        def device = Device.findByStbName(executionInstance?.device)
        def testGroup
		
		def executionResultMap = [:]
		
		executionDeviceList.each {executionDevice->
			ArrayList executionList = new ArrayList(executionDevice.executionresults);
			executionResultMap.put(executionDevice, executionList)
		}
		
        if(executionInstance?.script){
            def script = Script.findByName(executionInstance?.script)
            testGroup = script?.primitiveTest?.module?.testGroup
        }
		
		
        [executionInstance : executionInstance, executionDeviceInstanceList : executionDeviceList, testGroup : testGroup,executionresults:executionResultMap]
    }

    /**
     * Method to display the script execution details in the popup.
     * @return
     */
     def showResult(final String execName,final String scrGrp){
		 Execution executionInstance = Execution.findByName(execName)
		 def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
		 def device = Device.findByStbName(executionInstance?.device)
		 def testGroup
		 if(executionInstance?.script){
			 def script = Script.findByName(executionInstance?.script)
			 testGroup = script?.primitiveTest?.module?.testGroup
		 }
		// String xmlwriter = utilityService.writexml(executionInstance)
		 
		/*executionDevice.each{ execDevice ->
			executionResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
			def executionResultStatus = ExecutionResult.findAllByExecutionAndExecutionOutputIsNotNull(executionInstance, execDevice)
			if((executionResultStatus.size() >= 0) && (executionResultStatus.size() < scriptGrp.scripts.size())){
				scriptStatus = scriptStatus + " [${execDevice?.device}] :: Script Execution in Progress. ${executionResultStatus.size()} out of ${scriptGrp.scripts.size()} scripts executed"
			}
		}
		*/
		[executionInstance : executionInstance, executionDeviceInstanceList : executionDevice, testGroup : testGroup ]
		
	//	[scriptStatus :scriptStatus]			
    }
	 	   
    /**
     * Show the log files
     * @return
     */
    def showExecutionLog()  {
        try {
            String fileName = params?.id
            int index = fileName.indexOf( UNDERSCORE )
            def executionId = fileName.substring( 0, index )
            String filePath = "${request.getRealPath('/')}//logs//${executionId}//${params?.execDeviceId}//"+params?.id
            def file = new File(filePath)
            response.setContentType("html/text")
            response.setHeader("Content-disposition", "attachment;filename=${file.getName()}")
            response.outputStream << file.newInputStream()
        } catch (FileNotFoundException fnf) {
            response.sendError 404
        }
    }
    

	/**
	 * Show the log files
	 * @return
	 */
	def showCrashExecutionLog()  {
		try {
			String fileName = params?.id
			int index = fileName.indexOf( UNDERSCORE )
			def executionId = fileName.substring( 0, index )
			String filePath = "${request.getRealPath('/')}//logs//crashlogs//"+params?.id
			def file = new File(filePath)
			response.setContentType("html/text")
			response.setHeader("Content-disposition", "attachment;filename=${file.getName()}")
			response.outputStream << file.newInputStream()
		} catch (FileNotFoundException fnf) {
			response.sendError 404
		}
	}
	
    /**
     * TO DO : Remove this once the device status checking is done.
     * Reset the device status to FREE.
     * Called only when the user is sure that the test execution ended
     * without giving any result or the device is not reachable
     * @param id
     * @return
     */
    def resetDevice(Long id) {
        def deviceInstance = Device.get(id)
        if (!deviceInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'device.label', default: 'Device'), deviceInstance.stbName])
            redirect(action: "list")
            return
        }      
        else{
            Device.withTransaction { status ->
                try {
                    deviceInstance.deviceStatus = Status.FREE
                    deviceInstance.save(flush:true)
                    status.flush()
                }
                catch(Throwable th) {
                    status.setRollbackOnly()
                }
            }
        }
    }  
	
	/**
	 * REST API : To save the load module status
	 * @param executionId
	 * @param resultData
	 * @return
	 */
	def saveLoadModuleStatus(final String execId, final String statusData, final String execDevice, final String execResult){
		Execution execution = Execution.findById(execId,[lock: true])
		if(!execution.result.equals( FAILURE_STATUS )){
			execution.result = statusData.toUpperCase().trim()
			execution.save(flush:true)
		}		
		ExecutionDevice execDeviceInstance = ExecutionDevice.findByExecutionAndId(execution,execDevice)		
		if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
			execDeviceInstance.status = statusData.toUpperCase().trim()
			execDeviceInstance.save(flush:true)
		}
		ExecutionResult executionResult = ExecutionResult.findById(execResult,[lock: true])
		if(!executionResult.status.equals( FAILURE_STATUS )){
			executionResult.status = statusData.toUpperCase().trim()
			executionResult.save(flush:true)
		}
	}
	
	/**
	 * REST API : To save the result details
	 * @param executionId
	 * @param resultData
	 * @return
	 */
   def saveResultDetails(final String execId, final String resultData, final String execResult,
	   final String expectedResult, final String resultStatus, final String testCaseName, final String execDevice)
   {
		try{
			def slurper = new JsonSlurper()
			if(resultData){
				
				//def jsonResult = slurper.parseText(resultData)
				
				String actualResult = resultData//jsonResult?.result

				if(actualResult){
					ExecutionResult executionResult = ExecutionResult.findById(execResult,[lock: true])

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

					Execution execution = Execution.findById(execId,[lock: true])
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
			else{
				Execution execution = Execution.findById(execId,[lock: true])
				execution.result = FAILURE_STATUS
				execution.save(flush:true)
			}
		}catch(Exception ex){
		}
	}

    /**
     * Search execution list based on the execution name
     * @return
     */
    def searchExecutionList(){
        def executionList = []
        def execution = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${params?.searchName}%' and (b.script like '%Multiple%' or b.script like '%${params?.searchName}%' ) ")
        execution.each{
            executionList.add(it[INDEX_ZERO])
        }
        render(template: "searchList", model: [executionInstanceList : executionList])
    }
  
    /**
     * Search execution list based on different search criterias of
     * script, device, and execution from and to dates.
     * @return
     */
    def multisearch(){
        def executionList = executionService.multisearch( params?.toDate, params?.fromDate, params?.deviceName, params?.resultStatus,
        params?.scriptType, params?.scriptVal )
        render(template: "searchList", model: [executionInstanceList : executionList])
    }
    
    
    
    /**
     * TO DO : Remove this once the port forwarding is automated via config file during reboot.
     * It is caled during free state
     * Called only when the user is want to reset all rules.
     * 
     * @param id
     * @return
     */
    def resetIPRule(Long id) {
        def device = Device.get(id)
        if (!device) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'device.label', default: 'Device'),
                device.stbName
            ])
            redirect(action: "list")
            return
        }
        else{
			def executionResult
            List existingDevices = []
            List newDevices = []
            List deletedDevices = []
            def boxType
            List macIdList = []
            File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//calldevicestatus_cmndline.py").file
            def absolutePath = layoutFolder.absolutePath
            def deviceStatus
            def deviceId
            List childDeviceList = []
            List devicesTobeDeleted = []

            Device.withTransaction {
                try {

                    boxType = device?.boxType?.type?.toLowerCase()
                    if(boxType == "gateway"){

                        macIdList.removeAll(macIdList)
                        executionResult =  executionService.executeGetDevices(device)   // execute callgetdevices.py

                        macIdList = executionService.parseExecutionResult(executionResult)

                        int childStbPort
                        int childStatusPort
                        int childLogTransferPort

                        childDeviceList.removeAll(childDeviceList)


                        if(macIdList.size() > 0 ){
                            macIdList.each{ macId ->
                                Device deviceObj = Device.findByMacId(macId)

                                Random rand = new Random()
                                int max = 100
                                def randomIntegerList = []
                                int randomVal
                                (1..100).each {
                                    randomVal =  rand.nextInt(max+1)
                                }


                                if(deviceObj){
                                    deviceObj.childDevices.each { childDevice -> devicesTobeDeleted << childDevice }


                                    devicesTobeDeleted.each { childDevice ->

                                        childDevice.delete(flush:true)
                                    }
                                }

                            }
                            existingDevices = device.childDevices
                            device.childDevices = childDeviceList
                            deletedDevices = existingDevices - childDeviceList
                            deletedDevices.each{ stbDevice ->

                                stbDevice.delete(flush:true)
                            }
                        }
                        else{
                            if(executionResult.contains(FOUND_MACID)){

                                existingDevices = device.childDevices
                                device.childDevices = childDeviceList
                                deletedDevices = existingDevices - childDeviceList
                                deletedDevices.each{ stbDevice ->

                                    stbDevice.delete(flush:true)
                                }
                            }
                        }

                    }
                }
                catch(Throwable th) {
                }
            }
        }
    }

	/**
	 * Method export the execution details to excel format.
	 * This method will be called upon clicking excel export button in execution page.
	 * The method will parse all the child attributes of the execution object to corresponding maps.
	 * Finally all this data will be pushed to excel sheet at a particular format.
	 * The resulting excel sheet will be available in downloads folder of running browser.
	 * 
	 * @param id - Id of execution object.
	 * 
	 */
	def exportToExcel = {

		if(!params.max) params.max = 100000
		List executionResultInstanceList = []
		List executionMethodResultInstanceList = []
		List executionReportData = []
		List dataList = []
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList = []
		columnWidthList = [0.35, 0.5]
		String deviceDetails

		Execution executionInstance = Execution.findById(params.id)
		if(executionInstance){

			int j = 0
			String fileContents = ""
			def deviceName = executionInstance?.device
			Device deviceInstance = Device.findByStbName(deviceName)
			def deviceIp = deviceInstance?.stbIp
			def executionTime = executionInstance?.executionTime
			
			String filePath = "${request.getRealPath('/')}//logs//version//${executionInstance.id}_version.txt"

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

			Map mapDevice 			= ["C1":EXPORT_DEVICE_LABEL,"C2":deviceName]
			Map mapIpAddress 		= ["C1":EXPORT_IPADDRESS_LABEL, "C2": deviceIp]
			Map mapExecutionTime 	= ["C1":EXPORT_EXECUTION_TIME_LABEL,"C2":executionTime]
			Map deviceDetailsMap    = ["C1":EXPORT_DEVICE_DETAILS_LABEL,"C2":deviceDetails]
			Map blankRowMap 		= ["C1":"     ","C2":"     "]
			dataList.add(blankRowMap)
			dataList.add(mapDevice)
			dataList.add(mapIpAddress)
			dataList.add(mapExecutionTime)
			dataList.add(deviceDetailsMap)
			dataList.add(blankRowMap)

			executionResultInstanceList =  ExecutionResult.findAllByExecution(executionInstance)
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

				fieldMap = ["C1":"     ", "C2":"     "]
				int functionCount = functionList.size()
				for(int i=0;i<functionCount;i++){

					int index
					index = i + 1
					def functionDetails
					functionDetails = EXPORT_EXPECTED_RESULT_LABEL+expectedResultList[i] + NEW_LINE +
							EXPORT_ACTUAL_RESULT_LABEL+actualResultList[i] + NEW_LINE + EXPORT_FUNCTION_STATUS_LABEL+functionStatusList[i] + NEW_LINE

					Map functionDetailsMap = ["C1":EXPORT_FUNCTION_LABEL+functionList[i],"C2":functionDetails]
					dataList.add(functionDetailsMap)

				}
				dataList.add(logDataMap)
				dataList.add(blankRowMap)
			}

			parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList ]
		}
		else{
			log.error "Invalid excution instance......"

		}

		params.format = EXPORT_EXCEL_FORMAT
		params.extension = EXPORT_EXCEL_EXTENSION
		response.contentType = grailsApplication.config.grails.mime.types[params.format]
		response.setHeader("Content-disposition", "attachment; filename="+EXPORT_FILENAME+ executionInstance.name +".${params.extension}")
		exportService.export(params.format, response.outputStream,dataList, null,fieldMap,[:], parameters)
		log.info "Completed excel export............. "


		/*********** csv support***************************/                                //TODO Use this if csv support needed
		def type = params.type
		if(type){
			params.format = "csv"
			response.contentType = 'text/csv'

			def filName = "ExecutionReport-"+ executionInstance.name + ".csv"
			response.setHeader("Content-disposition", "attachment; filename="+filName+";sheetname=MySheet")
			exportService.export(params.format, response.outputStream,dataList, fieldLabels,fieldMap,[:], [:])
		}

	}
	
	
	/**
	 * Method to perform delete operation for marked results.
	 * This method will be invoked by an ajax call.
	 * It removes all the child objects of given execution instance.
	 * 
	 * @param - Ids of checked execution results.
	 * @return - JSON message
	 * 
	 */
	def deleteExecutioResults = {
		
		List executionResultList = []
		List executionMethodResultInstanceList = []
		def selectedRows
		List returnMsg = []
		int deleteCount = 0
		String message

		if(params?.checkedRows != UNDEFINED && params?.checkedRows != BLANK_SPACE && params?.checkedRows != null){

			selectedRows = params?.checkedRows.split(COMMA_SEPERATOR)
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
						
						String filePath = "${request.getRealPath('/')}//logs"
						
						 
						 */
						
					}
					else{
						log.info "Invalid executionInstance"
						message = "Delete failed"
					}
				}
			}

			if(deleteCount == 1){
				message = deleteCount+" Result Deleted"
			}
			else if (deleteCount > 1){
				message =  deleteCount+" Results Deleted"
			}
			else{
				message = "Delete failed"
			}

			returnMsg.add( message)
			render returnMsg as JSON
		}
		else{
			log.info "Invalid marking of results for deletion"
		}
	}

	/**
	 * Ajax call to update the isMarked status of execution instance.
	 * This will be called during mark operation of corresponding checkbox of execution results.
	 */
	def updateMarkStatus = {
		int markStatus
		markStatus = Integer.parseInt(params?.markStatus)
		Execution executionInstance = Execution.findById(params?.id)
		if(executionInstance){
			executionInstance.isMarked = markStatus
			executionInstance.save(flush:true)
		}
	}

	def writexmldata(){
		Execution executionInstance = Execution.findByName(params?.execName)
		def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)		
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")		
		xml.executionResult(name: executionInstance?.name.toString(), status: executionInstance?.result.toString()) {			
			executionDevice.each{ executionDeviceInstance ->
				device(name:executionDeviceInstance?.device.toString(), ip1:executionDeviceInstance?.deviceIp, exectime:executionDeviceInstance?.executionTime, status:executionDeviceInstance?.status)
				{
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
							def systemDiagList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,"CPUMEMORY")
							SystemDiagnostics{
								systemDiagList?.each{ sdInstance ->
									Process(Name:sdInstance?.processName,CpuUtilization:sdInstance?.processValue,MemoryUtilization:sdInstance?.processValue1)									
								}
							}
						}
					}
				}
			}
		}		
		response.setHeader "Content-disposition", "attachment; filename=${params?.execName}.xml"
		response.contentType = 'text/xml'
		response.outputStream << writer.toString()
		response.outputStream.flush()
	
	}
	
	def readOutputFileData(String executionName){
		String output = "";
		try{
			String pathName = Constants.SCRIPT_OUTPUT_FILE_PATH+executionName+Constants.SCRIPT_OUTPUT_FILE_EXTN
			File opFile = grailsApplication.parentContext.getResource(pathName).file
			List opList ;
			if(opFile.exists()){
				opList = opFile.readLines();
			}else{
			opList = []
				String opFolderName = Constants.SCRIPT_OUTPUT_FILE_PATH
				File opFolder = grailsApplication.parentContext.getResource(opFolderName).file
				if(opFolder.exists()){
					File[] files = opFolder.listFiles(new CustomFileNameFilter(executionName));
					for (int i=0; i< files.length;i++) {
						List opList1 = files[i].readLines();
						if(opList1 != null && opList1.size() > 0){
							opList.addAll(opList1);
						}						
					}
				}
			}
			
			for (var in opList) {
				output = output + var
			}
		}catch(Exception e){
			//println "Error in reading output file for "+executionName
		}
		render output as String
	}

	
	def getDetailedTestResult(final String execResId){

		JsonObject resultNode = new JsonObject()
		if(execResId){
			ExecutionResult executionResult = ExecutionResult.findById(execResId)
			JsonArray jsonArray = new JsonArray()
			JsonObject functionNode = new JsonObject()
			
			resultNode.addProperty("ExecutionName",executionResult?.execution?.name.toString())
			resultNode.addProperty("Device",executionResult?.device.toString())
			resultNode.addProperty("Script",executionResult?.script.toString())
			resultNode.addProperty("Status",executionResult?.status.toString())
			executionResult?.executemethodresults.each{ execMethdRslt ->
				functionNode = new JsonObject()
				functionNode.addProperty("FunctionName", execMethdRslt?.functionName.toString()) 
				functionNode.addProperty("ExpectedResult", execMethdRslt?.expectedResult.toString())
				functionNode.addProperty("ActualResult", execMethdRslt?.actualResult.toString())
				functionNode.addProperty("Status", execMethdRslt?.status.toString())
				jsonArray.add(functionNode)
			}	
			resultNode.add("Functions",jsonArray)
			resultNode.addProperty("LogData",executionResult?.executionOutput.toString())			
		}	
		render resultNode
	}
}
