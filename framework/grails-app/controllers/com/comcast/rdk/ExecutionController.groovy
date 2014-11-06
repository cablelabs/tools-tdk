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
import static org.quartz.CronScheduleBuilder.*
import static org.quartz.DateBuilder.*
import static org.quartz.JobKey.*
import static org.quartz.TriggerBuilder.*
import static org.quartz.TriggerKey.*
import grails.converters.JSON

import java.text.DateFormat
import java.text.SimpleDateFormat
import java.util.Map;
import java.util.date.*

import org.codehaus.groovy.grails.web.json.JSONObject
import org.custommonkey.xmlunit.*
import org.quartz.JobBuilder
import org.quartz.JobDetail
import org.quartz.Trigger
import org.quartz.impl.triggers.SimpleTriggerImpl

import rdk.test.tool.*

import com.google.gson.JsonArray
import com.google.gson.JsonObject

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
	 * Injects the scriptService.
	 */
	def scriptService
	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication
	
	def utilityService
	
	def exportService   // Export service provided by Export plugin
	
	def deviceStatusService
	
	def primitivetestService
	
	def executedbService
	
	def executescriptService
	
	/**
	 * Injects the excelExportService
	 */
	def excelExportService
	
	public static volatile Object  lock = new Object()
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
	
	
	def deleteJob(){
		def jobDetailsInstance = JobDetails.findById(params?.jobId)
		if (jobDetailsInstance) {
			
			def date = new Date()
			def endDate = jobDetailsInstance?.endDate
			def time
			if(endDate){
				time = date.getTime() - endDate.getTime()
			}
			else{
				time = date.getTime() - jobDetailsInstance?.startDate?.getTime()
			}
			if(time > 0 ){
				jobDetailsInstance.delete(flush: true)
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
        [scripts : params?.scripts, devices : params?.devices, device : params?.deviceId, scriptGroup : params?.scriptGroup, jobDetailList : JobDetails.list(), 
			jobInstanceTotal : JobDetails.count(), isSystemDiagnostics : params?.systemDiagnostics, isBenchMark : params?.benchMarking, rerun : rerun, repeatCount : repeatCount]
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
				DeviceStatusUpdater.updateDeviceStatus(grailsApplication,deviceStatusService,executescriptService);
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
		
		def scripts = scriptService.getScriptNameFileList(getRealPath())
		def sList = scripts.clone()
		sList.sort{a,b -> a?.scriptName <=> b?.scriptName}
		
		def scriptGrp = ScriptGroup.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(),[order: 'asc', sort: 'name'])
		
		DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)		
        Calendar cal = Calendar.getInstance()
        [datetime :  dateFormat.format(cal.getTime()).toString(), device : device, scriptGrpList : scriptGrp, scriptList : sList]
    }
	
	def getScriptList(){
		List scriptList = []
		Map scriptGroupMap = [:]
		List dirList = [
			Constants.COMPONENT,
			Constants.INTEGRATION
		]
		dirList.each{ directory ->
			File scriptsDir = new File( "${request.getRealPath('/')}//fileStore//testscripts//"+directory+"//")
			if(scriptsDir.exists()){
				def modules = scriptsDir.listFiles()
				modules.each { module ->

					File [] files = module.listFiles(new FilenameFilter() {
								@Override
								public boolean accept(File dir, String name) {
									return name.endsWith(".py");
								}
							});


					files.each { file ->
						String name = file?.name?.replace(".py", "")
						scriptList.add(name)
					}

				}
			}
		}

		scriptList.sort();

		return scriptList
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
		String serverAddr = urlArray[INDEX_TWO]
		if(serverAddr.contains("localhost:")){
			String localAddr = request.getProperties().get("localAddr")
			String localPort = request.getProperties().get("localPort")
			if((!localAddr.startsWith("0:0:0:0:0:0:0:1")) && (!localAddr.startsWith("0.0.0.0"))){
				serverAddr = ""+localAddr+":"+localPort
			}
		}
        String url = urlArray[INDEX_ZERO] + DOUBLE_FWD_SLASH + serverAddr + URL_SEPERATOR + urlArray[INDEX_THREE]
        return url
    }

    /**
     * Method to return the real path of the application
     * @return
     */
    def String getRealPath(){           
//       String s = request.getSession().getServletContext().getRealPath("/") 
//       s = s.replace( '\\', '/' )
//       return s
       return request.getSession().getServletContext().getRealPath(URL_SEPERATOR) 
    }     
 
	   
	/**
	 * REST interface to support script execution with the parameters passed.
	 * @param stbName
	 * @param boxType
	 * @param suiteName
	 * @return
	 */
	def thirdPartyTest(final String stbName, final String boxType, final String imageName, final String suiteName, final String test_request, final String callbackUrl ){
		JsonObject jsonOutData = new JsonObject()
		
		try {
			String htmlData = ""
			String outData = ""
			String  url = getApplicationUrl()
			def execName = ""
			String filePath = "${request.getRealPath('/')}//fileStore"

			if(test_request){
				String status = scriptexecutionService.generateResultBasedOnTestRequest(test_request,callbackUrl,filePath, url, imageName, boxType,getRealPath())
				if(status){
					jsonOutData.addProperty("status", "SUCCESS");
					jsonOutData.addProperty("result", "Result will be send with callback url");
				}
				else{
					jsonOutData.addProperty("status", "FAILED");
					jsonOutData.addProperty("result", "Error! Please try again");
				}
			}
			else{

				ScriptGroup scriptGroup = ScriptGroup.findByName(suiteName)
				def scriptStatusFlag
				def scriptVesrionFlag
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
								String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
								scriptGroup?.scriptList?.each{ scrpt ->
									
									def script = scriptService.getScript(getRealPath(), scrpt?.moduleName, scrpt?.scriptName)
									
									if(script){
									/**
									 * Checks whether atleast one script matches with the box type of device.
									 * If so execution will proceed with that one script
									 */
									if(executionService.validateScriptBoxTypes(script,deviceInstance)){
										scriptStatusFlag = true
										if(executionService.validateScriptRDKVersions(script,rdkVersion)){
											scriptVesrionFlag = true
										}
									}
									}
								}
								if(scriptStatusFlag && scriptVesrionFlag){
									String status = ""
									try {
										status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
										
										synchronized (lock) {
											if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
												status = "BUSY"
											}else{
												if((status.equals( Status.FREE.toString() ))){
													if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
														executionService.deviceAllocatedList.add(deviceInstance?.id)
														
														Thread.start{
															deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
														}
													}
												}
											}
										}
									}
									catch(Exception eX){
									}
									status = status.trim()
									if((status.equals( Status.FREE.toString() ))){
										if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
											executionService.deviceAllocatedList.add(deviceInstance?.id)
										}

										def scriptname
										def deviceName
										ExecutionDevice executionDevice
										def execution
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

											try {
												executionSaveStatus = scriptexecutionService.saveExecutionDetails(execName, scriptname, deviceName, scriptGroup,url)
											} catch (Exception e) {
												executionSaveStatus = false
											}
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
												if(executionDevice.save(flush:true)){
													String getRealPathString  = getRealPath()
													executionService.executeVersionTransferScript(getRealPathString,filePath,execName, executionDevice?.id, deviceInstance?.stbIp, deviceInstance?.logTransferPort)
													scriptexecutionService.executeScriptGroup(scriptGroup, boxType, execName, executionDevice?.id.toString(), deviceInstance, url, filePath, getRealPathString, callbackUrl, imageName )
												}
											}
											catch(Exception e){
											}
										}
										else{
											deviceNotExistCnt++
											outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
										}
									}
									else if(status.equals( Status.ALLOCATED.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
									else if(status.equals( Status.NOT_FOUND.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
									else if(status.equals( Status.HANG.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
									else if(status.equals( Status.BUSY.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
									else{
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
								}
								else{
									deviceNotExistCnt++
									if(!scriptStatusFlag){
										outData = outData +" BoxType of Scripts in ScriptGroup is not matching with BoxType of Device ${deviceInstance?.stbName}"
									}else if(!scriptVesrionFlag){
										outData = outData +" RDK Version of Scripts in ScriptGroup is not matching with RDK Version of Device ${deviceInstance?.stbName}"
									}
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
					jsonOutData.addProperty("status", "RUNNING"+outData)
					jsonOutData.addProperty("result", url)
				}
				else{
					url = outData
					jsonOutData.addProperty("status", "FAILURE")
					jsonOutData.addProperty("result", url)
				}
			}
		} catch (Exception e) {
		}
		render jsonOutData
	}

	def getDeviceStatusList(){
		JsonObject devices = new JsonObject()
		try {
			def deviceList = Device.list()		
			deviceList?.each{ device ->
				devices.addProperty(device.stbName.toString()+LEFT_PARANTHESIS+device.stbIp.toString()+RIGHT_PARANTHESIS+LEFT_PARANTHESIS+device.boxType.toString()+RIGHT_PARANTHESIS, device.deviceStatus.toString())
			}
		} catch (Exception e) {
			
		}
		render devices
	}
	
	def getDeviceStatus(final String stbName, final String boxType){
		JsonObject device = new JsonObject()
		try {
			if(stbName && boxType)	{
				def deviceInstance = Device.findByStbName(stbName)//,BoxType.findByName(boxType.trim()))			
				device.addProperty(deviceInstance.stbName.toString()+LEFT_PARANTHESIS+deviceInstance.stbIp.toString()+RIGHT_PARANTHESIS, deviceInstance.deviceStatus.toString())
			}
		} catch (Exception e) {
		}
		render device		
	}
	
	def thirdPartyJsonResult(final String execName, final String appurl ){		
		JsonObject executionNode = scriptexecutionService.thirdPartyJsonResultFromController(execName, getApplicationUrl() ,getRealPath())
		render executionNode
	}
		
		
    /**
     * Execute the script
     * @return
     */
    def executeScriptMethod() {		
		boolean aborted = false
		def exId
        def scriptGroupInstance
        def scriptStatus = true
		def scriptVersionStatus = true
        Device deviceInstance //= Device.findById(params?.id, [lock: true])
        String htmlData = ""
        def deviceId
		def executionName
		def scriptType = params?.myGroup	
		def deviceList = []
		def deviceName
		boolean allocated = false
		boolean singleScript = false
		
		ExecutionDevice executionDevice = new ExecutionDevice()
		if(params?.devices instanceof String){
			deviceList << params?.devices
			deviceInstance = Device.findById(params?.devices, [lock: true])
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

		int repeatCount = 1
		if(params?.repeatNo){
		 repeatCount = (params?.repeatNo)?.toInteger()
		}
		
        def executionInstance = Execution.findByName(executionName)
        if(!(params?.name)){
            htmlData = message(code: 'execution.name.blank')
        }
        else if(executionInstance){
            htmlData = message(code: 'execution.name.duplicate')
        }
		else if(!params?.scriptGrp && !params?.scripts){
			htmlData = message(code: 'execution.noscript.selected')
		}
		else if(!(params?.devices)){
			htmlData = message(code: 'execution.nodevice.selected')
		}
        else if(deviceInstance?.deviceStatus.toString().equals(Status.BUSY.toString())){
            htmlData = message(code: 'execution.device.notfree')
        }
		else if(deviceInstance?.deviceStatus.toString().equals(Status.NOT_FOUND.toString())){
			htmlData = message(code: 'execution.device.notfree')
		}
		else if(deviceInstance?.deviceStatus.toString().equals(Status.HANG.toString())){
			htmlData = message(code: 'execution.device.notfree')
		}		
		else if(repeatCount == 0){
			htmlData = "Give a valid entry in repeat"
		}	
        else{			
        	StringBuilder output = new StringBuilder();
			try{
			def isBenchMark = FALSE
			def isSystemDiagnostics = FALSE
			def rerun = FALSE
			if(params?.systemDiagnostics.equals(KEY_ON)){
				isSystemDiagnostics = TRUE
			}
			if(params?.benchMarking.equals(KEY_ON)){
				isBenchMark = TRUE
			} 
			if(params?.rerun.equals(KEY_ON)){
				rerun = TRUE
			}
            def scriptName
            String url = getApplicationUrl()
            String filePath = "${request.getRealPath('/')}//fileStore"   
			def execName
			def executionNameForCheck
			
			
			Map deviceDetails = [:]
			for(int i = 0; i < repeatCount; i++ ){ 
				executionNameForCheck = null
				deviceList.each{ device ->
					deviceInstance = Device.findById(device)
					boolean validScript = false
						if(scriptType == SINGLE_SCRIPT){
							def scripts = params?.scripts
							if(scripts instanceof String){
								singleScript = true
								def moduleName= scriptService.scriptMapping.get(params?.scripts)
								if(moduleName){
								def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, params?.scripts)
								if(scriptInstance1){
								if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
									String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
									if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
										validScript = true
									}else{
										htmlData = "RDK Version supported by the script is not matching with the RDK Version of selected Device "+deviceInstance?.stbName+"<br>"
									}
								}else{
									htmlData = message(code: 'execution.boxtype.nomatch')
								}
								}else{
									htmlData = "No Script is available with name ${params?.scripts} in module ${moduleName}"
								}
								}else{
									htmlData = "No module associated with script ${params?.scripts}"
								}
							}
							else{
								scripts.each { script ->
									def moduleName= scriptService.scriptMapping.get(script)
									def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, script)
									if(scriptInstance1){
										if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
											String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
											if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
												validScript = true
											}
										}
									}
								}
								
							}
						}else{
							def scriptGroup = ScriptGroup.findById(params?.scriptGrp,[lock: true])

							String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
							
							try{
							scriptGroup?.scriptList?.each{ script ->
								
								def scriptInstance1 = scriptService.getMinimalScript(getRealPath(),script?.moduleName, script?.scriptName)
								/**
								 * Checks whether atleast one script matches with the box type of device.
								 * If so execution will proceed with that one script
								 */
								if(scriptInstance1 && executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
									if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
										validScript = true
										throw new Exception("return from closure") 
									}
								}
							}
							}catch(Exception e ){
								if(e.getMessage() == "return from closure" ){
									
								}else{
									validScript = false
								}
							}

						}
					if(validScript){
					if(deviceList.size() > 1){
						executionNameForCheck = null
					}
					boolean paused = false
					int pending = 0
					int currentExecutionCount = -1
					Map statusMap = deviceDetails.get(device)
					if(statusMap){
						paused = ((boolean)statusMap.get("isPaused"))
						pending = ((int)statusMap.get("pending"))
						currentExecutionCount = ((int)statusMap.get("currentExecutionCount"))
					}
					String status = ""
					
					deviceInstance = Device.findById(device)
					try {
						 status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
					 
						 synchronized (lock) {
							 if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
								 status = "BUSY"
							 }else{
								 if((status.equals( Status.FREE.toString() ))){
									 if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
										 allocated = true
										 executionService.deviceAllocatedList.add(deviceInstance?.id)
										 Thread.start{
											 deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
										 }
									 }
								 }
							 }
						 }
						 
					}
					catch(Exception eX){
					}

				if( !paused && (status.equals( Status.FREE.toString() ))){
					if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						allocated = true
						executionService.deviceAllocatedList.add(deviceInstance?.id)
					}
					
					deviceInstance = Device.findById(device)
					def executionSaveStatus = true
					def execution = null
					def scripts = null
					deviceId = deviceInstance?.id
					if(scriptType == SINGLE_SCRIPT){
						scripts = params?.scripts
						if(scripts instanceof String){
//							scriptInstance = Script.findById(params?.scripts,[lock: true])
							def moduleName= scriptService.scriptMapping.get(params?.scripts)
							def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, params?.scripts)
//							def scriptInstance1 = executionService.getScript(getRealPath(),"ClosedCaption", scripts)
							scriptStatus = executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)
							String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
							scriptVersionStatus = executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)
							scriptName = scripts
						}
						else{
							scriptName = MULTIPLESCRIPT
						}
					}else{
						scriptGroupInstance = ScriptGroup.findById(params?.scriptGrp,[lock: true])
					}
					if(scriptStatus && scriptVersionStatus){
						if(!executionNameForCheck){
							String exName = executionName
							if(deviceList.size() > 1){
								deviceName = deviceInstance?.stbName
								exName = deviceInstance?.stbName +"-"+executionName
							}
							if(i > 0){
								execName = exName + UNDERSCORE +i
							}
							else{
								execName = exName
							}
							executionSaveStatus = executionService.saveExecutionDetails(execName, scriptName, deviceName, scriptGroupInstance,url,isBenchMark,isSystemDiagnostics,rerun)
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
							if(deviceList.size() > 1){
															
								executescriptService.executeScriptInThread(execName, device, executionDevice, params?.scripts, params?.scriptGrp, executionName,
										filePath, getRealPath(), params?.myGroup, url, isBenchMark, isSystemDiagnostics, params?.rerun)
								
							}else{
										htmlData = executescriptService.executescriptsOnDevice(execName, device, executionDevice, params?.scripts, params?.scriptGrp, executionName,
												filePath, getRealPath(), params?.myGroup, url, isBenchMark, isSystemDiagnostics, params?.rerun)
										output.append(htmlData)
										Execution exe = Execution.findByName(execName)
										if(exe){
											def executionList = Execution.findAllByExecutionStatusAndName("PAUSED",execName);
											paused = (executionList.size() > 0)
										}
								}
							
							if(paused){
								currentExecutionCount = i
								statusMap = deviceDetails.get(device)
								if(statusMap == null){
									statusMap = [:]
									deviceDetails.put(device,statusMap)
								}

								if(statusMap != null){
									statusMap.put("isPaused", true)
									statusMap.put("currentExecutionCount", i)
									statusMap.put("pending", pending)
								}

							}
						}
					}
					else{
						def devcInstance = Device.findById(device)
						if(!scriptStatus){
							htmlData = message(code: 'execution.boxtype.nomatch')
						}else{
							htmlData = "RDK Version supported by the script is not matching with the RDK Version of selected Device "+devcInstance?.stbName+"<br>"
						}
						

						if(executionService.deviceAllocatedList.contains(devcInstance?.id)){
							executionService.deviceAllocatedList.remove(devcInstance?.id)
						}

						
						
						output.append(htmlData)
					}
					htmlData = ""				
				}else{
				
						if(paused){
								try {
									pending ++

									statusMap = deviceDetails.get(device)

									if(statusMap != null){
										statusMap.put("pending", pending)
									}

									if(i == repeatCount -1){
										executionService.saveRepeatExecutionDetails(execName, deviceInstance?.stbName,currentExecutionCount, pending)
									}

								} catch (Exception e) {
									e.printStackTrace()
								}
							}else{
								if(i > 0){
									def execName1 = executionName + UNDERSCORE +i
									try {
										Execution execution = new Execution()
										execution.name = execName1
										execution.script = scriptName
										execution.device = deviceName
										execution.scriptGroup = scriptGroupInstance?.name
										execution.result = FAILURE_STATUS
										execution.executionStatus = FAILURE_STATUS
										execution.dateOfExecution = new Date()
										execution.groups = executionService.getGroup()
										execution.applicationUrl = url
										execution.isRerunRequired = rerun?.equals("true")
										execution.isBenchMarkEnabled = isBenchMark?.equals("true")
										execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals("true")
										execution.outputData = "Execution failed due to the unavailability of box"
										if(! execution.save(flush:true)) {
											log.error "Error saving Execution instance : ${execution.errors}"
										}
									}
									catch(Exception th) {
										th.printStackTrace()
									}
								}

								htmlData = message(code: 'execution.device.notfree')
								output.append(htmlData)
							}
				}
				}else{
						if(!singleScript){
							htmlData = "No valid script available to execute."
						}
					output.append(htmlData)
				}
			   }	
			 }			
			}finally{
				if(deviceList.size() == 1){
					deviceList.each{ device ->
						def devInstance = Device.findById(device)
						if(allocated && executionService.deviceAllocatedList.contains(devInstance?.id)){
							executionService.deviceAllocatedList.remove(devInstance?.id)
						}
					}
					
					String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
					Thread.start{
						deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
					}
				}
			}
			htmlData = output.toString()						
        }
		render htmlData
    }

	def showAgentLogFiles(){
		def agentConsoleFileData = executionService.getAgentConsoleLogData( request.getRealPath('/'), params?.execId, params?.execDeviceId,params?.execResId)
		if(agentConsoleFileData.isEmpty()){
			agentConsoleFileData = "Unable to fetch Agent Console Log"
		}		
		render(template: "agentConsoleLog", model: [agentConsoleFileData : agentConsoleFileData])
	}

	def showLogFiles(){		
		def logFileNames = executionService.getLogFileNames(request.getRealPath('/'), params?.execId, params?.execDeviceId, params?.execResId )
		render(template: "logFileList", model: [execId : params?.execId, execDeviceId : params?.execDeviceId, execResId : params?.execResId, logFileNames : logFileNames])
	}
	
	def showCrashLogFiles(){
		def crashlogFileNames = executionService.getCrashLogFileNames(request.getRealPath('/'), params?.execId, params?.execDeviceId, params?.execResId)
		render(template: "crashLogFileList", model: [execId : params?.execId, execDeviceId : params?.execDeviceId, execResId : params?.execResId, logFileNames : crashlogFileNames])
	}
						
    /**
     * Method to display the script execution details in the popup.
     * @return
     */
    def showLog(){
        Execution executionInstance = Execution.findById(params?.id) 
	//	if(!executionInstance.isPerformanceDone){
			executionService.setPerformance(executionInstance,request.getRealPath('/'))
		//}
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
        def device = Device.findByStbName(executionInstance?.device)
        def testGroup
		
		def executionResultMap = [:]
		def statusResultMap = [:]
		
		def listStatusCount = [:]
		
		executionDeviceList.each { executionDevice ->
			ArrayList executionList = new ArrayList(executionDevice.executionresults);
			executionResultMap.put(executionDevice, executionList)
					
			listStatusCount = executedbService.getStatusList(executionInstance,executionDevice,executionList.size().toString())
			
			statusResultMap.put(executionDevice, listStatusCount)
		}
		
        if(executionInstance?.script){
            def script = Script.findByName(executionInstance?.script)
            testGroup = script?.primitiveTest?.module?.testGroup
        }				
        [statusResults : statusResultMap, executionInstance : executionInstance, executionDeviceInstanceList : executionDeviceList, testGroup : testGroup,executionresults:executionResultMap]
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
		[executionInstance : executionInstance, executionDeviceInstanceList : executionDevice, testGroup : testGroup ]		
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
            String filePath = "${request.getRealPath('/')}//logs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+params?.id
		
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
			String filePath = "${request.getRealPath('/')}//logs//crashlogs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+params?.id
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
//		executescriptService.saveLoadModuleStatus(execId, statusData, execDevice, execResult)
		
		try {
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
		} catch (Exception e) {
			e.printStackTrace()
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
		   if(resultData){
			   String actualResult = resultData
			   if(actualResult){				  
				   ExecutionResult.withTransaction {
					   ExecutionResult executionResult = ExecutionResult.findById(execResult)
					   if(executionResult){
						   ExecuteMethodResult executionMethodResult = new ExecuteMethodResult()
						   if(resultStatus?.equals( STATUS_NONE ) || resultStatus == null ){
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
	
						   executionResult?.addToExecutemethodresults(executionMethodResult)
						   executionResult?.save(flush:true)
	
						   Execution execution = Execution.findById(execId)
						   ExecutionDevice execDeviceInstance = ExecutionDevice.findById(execDevice)
						   if(!executionResult?.status.equals( FAILURE_STATUS )){
							   executionResult?.status = resultStatus
							   executionResult?.save(flush:true)
							   if(!execution.result.equals( FAILURE_STATUS )){
								   execution.result = resultStatus
								   execution.save(flush:true)
							   }
							   if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
								   execDeviceInstance?.addToExecutionresults(executionResult)
								   execDeviceInstance?.status = resultStatus
								   execDeviceInstance?.save(flush:true)
							   }
						   }
					   } 
				   }
			   }
		   }
		   else{
			   Execution.withTransaction {
				   Execution execution = Execution.findById(execId)
				   if(execution){
					   execution.result = FAILURE_STATUS
					   execution.save(flush:true)
				   }				   
			   }
		   }
	   }catch(Exception ex){
		   ex.printStackTrace()
	   }
	}

    /**
     * Search execution list based on the execution name
     * @return
     */
    def searchExecutionList(){
        def executionList = []
		def executions = Execution.findAllByNameLike("${params?.searchName.trim()}%")
        executions.each{ execution ->
            executionList.add(execution)
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
     * It is called during free state
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
			deviceStatusService.resetIPRule(device)
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
		List dataList = []
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList =  [0.35, 0.5]

		Execution executionInstance = Execution.findById(params.id)
		try {
			if(executionInstance){			
				dataList = executedbService.getDataForExcelExport(executionInstance, getRealPath())
						fieldMap = ["C1":"     ", "C2":"     "]
								parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList ]
			}
			else{
				log.error "Invalid excution instance......"
			}
		} catch (Exception e) {
		println "ee "+e.getMessage()
			e.printStackTrace()
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
	 * Method to export the consolidated report in excel format.
	 */
	def exportConsolidatedToExcel = {
				if(!params.max) params.max = 100000
				Map dataMap = [:]
				List fieldLabels = []
				Map fieldMap = [:]
				Map parameters = [:]
				List columnWidthList = [0.08,0.4,0.15,0.4,0.15,0.4]
		
				Execution executionInstance = Execution.findById(params.id)
				if(executionInstance){
					dataMap = executedbService.getDataForConsolidatedListExcelExport(executionInstance, getRealPath(),getApplicationUrl())
					fieldMap = ["C1":" Sl.No ", "C2":" Script Name ","C3":" Status ", "C4":" Log Data ","C5":"AgentConsole log","C6":" Date of Execution "]
					parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]
				}
				else{
					log.error "Invalid excution instance......"
				}
		
				params.format = EXPORT_EXCEL_FORMAT
				params.extension = EXPORT_EXCEL_EXTENSION
				response.contentType = grailsApplication.config.grails.mime.types[params.format]
				response.setHeader("Content-disposition", "attachment; filename="+EXPORT_FILENAME+ executionInstance.name +".${params.extension}")
				excelExportService.export(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
				log.info "Completed excel export............. "
		
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
			deleteCount =  executedbService.deleteSelectedRowOfExecutionResult(selectedRows,getRealPath())

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
		try {
			Execution executionInstance = Execution.findById(params?.id)
					if(executionInstance){
						executionInstance.isMarked = markStatus
								executionInstance.save(flush:true)
					}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Download the execution result details in xml format
	 * @return
	 */
	def writexmldata(){
		String writer = executedbService.getExecutionDataInXmlFormat(params?.execName)
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
		}
		render output as String
	}

	/**
	 * REST Api : Get the detailed result based on a execution Result
	 * @param execResId
	 * @return
	 */
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
	
	def getAgentConsoleLog(final String execResId){

		ExecutionResult executionResult = ExecutionResult.findById(execResId)

		def agentConsoleFileData = "No AgentConsoleLog available"

		if(executionResult){

			try {
				agentConsoleFileData = executionService.getAgentConsoleLogData( request.getRealPath('/'), executionResult?.execution?.id?.toString(), executionResult?.executionDevice?.id?.toString(),executionResult?.id?.toString())
				if(agentConsoleFileData){
					agentConsoleFileData =agentConsoleFileData.trim()
					if(agentConsoleFileData.length() == 0){
						agentConsoleFileData = "No AgentConsoleLog available"
					}
				}else{
					agentConsoleFileData = "No AgentConsoleLog available"
				}
				} catch (Exception e) {
				e.printStackTrace()
			}
		}else{
			agentConsoleFileData = "No execution result available with the given execResId"
		}
		render agentConsoleFileData
	}
	
	/**
	 * REST Api : Get the detailed result based on a execution Result
	 * @param execResId
	 * @return
	 */
	
	def getClientPort(final String deviceIP,final String agentPort){
		JsonObject resultNode = null
		if(deviceIP && agentPort){
			Device device = Device.findByStbIpAndStbPort(deviceIP,agentPort)
			if(device){
				resultNode = new JsonObject()
				resultNode.addProperty("logTransferPort",device?.logTransferPort.toString())
				resultNode.addProperty("statusPort",device?.statusPort.toString())
			}
		}
		render resultNode
	}
	
	
	
	/**
	 * method to stop the execution through ui request
	 */
	def stopExecution(){
		Execution execution = Execution.findById(params?.execid)
		def listdate = []
		if(execution?.executionStatus.equals(INPROGRESS_STATUS)){
			def executionId = params?.execid?.toString()
			if(!executionService.abortList.contains(executionId)){
				executionService.abortList.add(executionId)
			}else{
				listdate.add("Request to stop already in progress")
			}
		}else if(execution?.executionStatus.equals("PAUSED")){
			executionService.saveExecutionStatus(true, execution?.id)
		}
		
		render listdate as JSON
	}
	
	/**
	 * REST API to request for stopping the test execution 
	 * @param executionName
	 * @return
	 */
	def stopThirdPartyTestExecution(final String executionName){
		JsonObject result = new JsonObject()
		result.addProperty("ExecutionName", executionName)
		try {
			Execution execution = Execution.findByName(executionName)
			if(execution?.executionStatus.equals(INPROGRESS_STATUS)){
				if(!executionService.abortList.contains(execution?.id?.toString())){
					executionService.abortList.add(execution?.id?.toString())
					result.addProperty("Status", "Requested for abort")
				}else{
					result.addProperty("Status", "Request to stop already in progress")
				}
				
			}else if(execution?.executionStatus.equals("PAUSED")){
				executionService.saveExecutionStatus(true, execution?.id)
				result.addProperty("Status", "Requested for abort")
			} else{
				if(execution != null){
					result.addProperty("Status", "Error. No execution found in this name in IN-PROGRESS / PAUSED state to stop")
				}else{
					result.addProperty("Status", "Error. No execution found in this name")
				}
			}
			render result
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	/**
	 * Method to fetch the device status of the selected device
	 * @return
	 */
	def updateDeviceStatus(){
		def device = Device.get( params?.id )
		try {
			String status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, device)
			deviceStatusService.updateOnlyDeviceStatus(device, status);
			def result1
			def deviceInstanceList = Device.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(),[order: 'asc', sort: 'stbName'])
			result1 = [url: getApplicationUrl(), deviceList : deviceInstanceList, deviceInstanceTotal: deviceInstanceList?.size()]
			render view:"devicelist", model:result1
		} catch (Exception e) {
		}
	}
	
	def getDeviceStatusListData(){
		try {
			def deviceInstanceList = Device.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(),[order: 'asc', sort: 'stbName'])
			def result1 = [url: getApplicationUrl(), deviceList : deviceInstanceList, deviceInstanceTotal: deviceInstanceList?.size()]
			render view:"devicelist", model:result1
		} catch (Exception e) {
		}
	}
	
	def deleteExecutions(){
		def deleteCount = 0
		try {
			
			List<Execution> executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${params?.cleanFromDate}' and '${params?.cleanToDate}' ")
			List executionResultList = []
			List executionMethodResultInstanceList = []
			List performanceList = []
			executionList?.each{ executionInstance ->
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
							executionResultInstance.delete(flush:true)
						}
					}

					def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
					executionDeviceList.each{ executionDeviceInstance ->
						executionDeviceInstance.delete(flush:true)
					}
					
					def execId = executionInstance?.id.toString()
					executionInstance.delete(flush:true)
					deleteCount ++
					log.info "Deleted "+executionInstance
					/**
					 * Deletes the log files, crash files
					 */
					String logFilePath = "${getRealPath()}//logs//"+execId
					def logFiles = new File(logFilePath)
					if(logFiles.exists()){
						logFiles?.deleteDir()
					}
					String crashFilePath = "${getRealPath()}//logs//crashlogs//"
					
					new File(crashFilePath).eachFileRecurse { file->
						if((file?.name).startsWith(execId)){
							file?.delete()
						}		
					}
					String versionFilePath = "${getRealPath()}//logs//version//"+execId
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
							
		} catch (Exception e) {
			e.printStackTrace()
		}				
	
		render deleteCount.toString()+" execution entries deleted"
	}
	

}
