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

import org.apache.shiro.SecurityUtils
import org.codehaus.groovy.grails.web.json.JSONObject
import org.junit.After;
import grails.converters.JSON
import java.util.List;
import java.util.concurrent.FutureTask
import java.util.regex.Matcher
import java.util.regex.Pattern


/**
 * Service class for the Execution domain.
 * @author sreejasuma, praveenkp
 */

class ExecutionService {
    
    /**
     * Injects the grailsApplication.
     */
    def grailsApplication
	
	/**
	 * transient variable to keep the list of execution to be aborted
	 */
	public static volatile List abortList = []
	
	public static volatile List deviceAllocatedList = []
	
	
    
    /**
     * Get the name of the day from the number used in cronschedule
     * to denote days
     * @param day
     * @return
     */
    def String getDayName(final String day){
        String dayName
        switch(day){
            case "1":
                dayName = "Sunday"
                break
            case "2":
                dayName = "Monday"
                break
            case "3":
                dayName = "Tuesday"
                break
            case "4":
                dayName = "Wednesday"
                break
            case "5":
                dayName = "Thursday"
                break
            case "6":
                dayName = "Friday"
                break
            case "7":
                dayName = "Saturday"
                break
            default:
                dayName = "Invalid day"
                break
        }        
    }
    
    /**
     * Get the option name from the number used in cronschedule for 
     * monthly options
     * @param day
     * @return
     */
    def String getOptionName(final String optionVal){
        String optionName
        switch(optionVal){
            case "1":
                optionName = "First"
                break
            case "2":
                optionName = "Second"
                break
            case "3":
                optionName = "Third"
                break
            case "4":
                optionName = "Fourth"
                break         
            default:
                optionName = "Invalid option"
                break
        }
        
    }
	
	def getAgentConsoleLogData(final String realPath, final String executionId, final String executionDeviceId, final String execResId){
		def summaryFilePath = "${realPath}//logs//consolelog//${executionId}//${executionDeviceId}//${execResId}"
		String fileContents = ""
		try{
			File directory = new File(summaryFilePath)
			directory.eachFile { file ->
				if (file.isFile()) {
					String fileName = file.getName()
					if(fileName.startsWith( "AgentConsole" )){
						file.eachLine { line ->
							fileContents = fileContents + "<br>"+ line
						}						
					}
				}
			}
		}
		catch(Exception ex){
		}
		return fileContents
	}
	
	
	def getLogFileNames(final String realPath, final String executionId, final String executionDeviceId, final String executionResId){
		def mapVals = [:]
		def summaryFilePath = "${realPath}//logs//${executionId}//${executionDeviceId}//${executionResId}"//_TestSummary"
		try{
			File directory = new File(summaryFilePath);
			List<File> foundFiles = new ArrayList<File>()
			
			directory.eachFile {
				if (it.isFile()) {
					String fileName = it.getName()
					if(fileName.startsWith( "${executionId}_TestSummary" )){
						foundFiles << new File("${realPath}//logs//${executionId}//${executionDeviceId}//${executionResId}//${fileName}")
					}
				}
			}
		
			if(foundFiles?.size() > 0){
			   def fileAppendTimestamp
			   def summaryFileName
				
			   for (File filename : foundFiles) {
				   summaryFileName = filename.getName()
				   int index = summaryFileName.lastIndexOf( UNDERSCORE )
				   fileAppendTimestamp = summaryFileName.substring( index )
				   String[] lineArray
				   filename.eachLine { line ->
					   lineArray = null
					   lineArray = line.split( SEMI_COLON );
					   if(lineArray.length >= INDEX_TWO){
						   if(lineArray[INDEX_TWO] != null){
							   String fileNameString = lineArray[INDEX_TWO]
							   int indexFlag = fileNameString.lastIndexOf( URL_SEPERATOR )
							   String fileName = fileNameString.substring( ++indexFlag )
							   mapVals.put( fileName.trim()+fileAppendTimestamp, lineArray[INDEX_ONE] )
						   }
					   }
				   }
			   }
			}
			else{
			  String filePath = "${realPath}//logs//${executionId}//${executionDeviceId}//${executionResId}"
				def dir = new File(filePath)
				dir.eachFile {
					if (it.isFile()) {
						String fileName = it.getName()
						if(fileName.startsWith( executionId )){
							fileName = fileName.replaceFirst( executionId+UNDERSCORE, "" )
							mapVals.put( fileName.trim(), "" )
						}
					}
				}
			}
		}catch(FileNotFoundException fnf){
			mapVals = []
		}
		catch(Exception ex){
			mapVals = []
		}
		return mapVals
	}

	
	
	def getCrashLogFileNames(final String realPath, final String executionId, final String executionDeviceId, final String executionResId){
		def mapVals = [:]
		try{
			  String filePath = "${realPath}//logs//crashlogs//${executionId}//${executionDeviceId}//${executionResId}"
				def dir = new File(filePath)
				dir.eachFile {
					if (it.isFile()) {
						String fileName = it.getName()
						if(fileName.startsWith( "${executionId}_${executionDeviceId}" )){
							fileName = fileName.replaceFirst( executionId+UNDERSCORE+executionDeviceId+UNDERSCORE, "" )
							mapVals.put( fileName.trim(), "" )
						}
					}
				}
			
		}catch(FileNotFoundException fnf){
			mapVals = []
		}
		catch(Exception ex){
			mapVals = []
		}
		return mapVals
	}
	
    
    /**
     * Get the list of log file names generated after the
     * script execution
     * @param executionId
     * @return
     */
    def getLogFileNames(final String realPath, final String executionId){
        def mapVals = [:]
        def summaryFilePath = "${realPath}//logs//${executionId}"//_TestSummary"
        try{
            File directory = new File(summaryFilePath);
            List<File> foundFiles = new ArrayList<File>()
            
            directory.eachFile {
                if (it.isFile()) {
                    String fileName = it.getName()
                    if(fileName.startsWith( "${executionId}_TestSummary" )){
                        foundFiles << new File("${realPath}//logs//${executionId}//${fileName}")
                    }
                }
            }
        
            if(foundFiles?.size() > 0){
               def fileAppendTimestamp
               def summaryFileName
                
               for (File filename : foundFiles) {
                   summaryFileName = filename.getName()
                   int index = summaryFileName.lastIndexOf( UNDERSCORE )
                   fileAppendTimestamp = summaryFileName.substring( index )
                   String[] lineArray
                   filename.eachLine { line ->
                       lineArray = null
                       lineArray = line.split( SEMI_COLON );
                       if(lineArray.length >= INDEX_TWO){
                           if(lineArray[INDEX_TWO] != null){
                               String fileNameString = lineArray[INDEX_TWO]
                               int indexFlag = fileNameString.lastIndexOf( URL_SEPERATOR )
                               String fileName = fileNameString.substring( ++indexFlag )
                               mapVals.put( fileName.trim()+fileAppendTimestamp, lineArray[INDEX_ONE] )
                           }
                       }
                   }
               }
            }
            else{
              String filePath = "${realPath}//logs//${executionId}"
                def dir = new File(filePath)
                dir.eachFile {
                    if (it.isFile()) {
                        String fileName = it.getName()
                        if(fileName.startsWith( executionId )){
                            fileName = fileName.replaceFirst( executionId+UNDERSCORE, "" )
                            mapVals.put( fileName.trim(), "" )
                        }
                    }
                }
            }
        }catch(FileNotFoundException fnf){
            mapVals = []
        }
        catch(Exception ex){
            mapVals = []
        }
        return mapVals
    }

    
    
    /**
     * Method to call the script executor to execute the script
     * @param executionData
     * @return
     */
    public String executeScript(final String executionData) {
        new ScriptExecutor().execute( getCommand( executionData ),1)
    }
	
	public String executeScript(final String executionData , final String executionName, final String scriptName) {
		String opFile = prepareOutputfile(executionName, scriptName)
		String output = NEW_LINE+"Executing script : "+scriptName+NEW_LINE
		output += "======================================="+NEW_LINE
		output += new ScriptExecutor(opFile).execute( getCommand( executionData ))
		return output
	}
	
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
     * Method to call the script executor to execute the script
     * @param executionData
     * @return
     */
    public String executeScript(final String executionData, int execTime, final String executionName, final String scriptName) {
		String opFile = prepareOutputfile(executionName, scriptName)
		String output = NEW_LINE+"Executing script : "+scriptName+NEW_LINE;
		output += "======================================="+NEW_LINE
		output += new ScriptExecutor(opFile).execute( getCommand( executionData ), execTime)
		return output
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
//    public boolean validateScriptBoxType(final Script scriptInstance, final Device deviceInstance){
//        boolean scriptStatus = true
//		Script.withTransaction { trns ->
//			def scriptInstance1 = Script.findById(scriptInstance?.id)			
//			def deviceInstance1 = Device.findById(deviceInstance?.id)
//	        if(!(scriptInstance1?.boxTypes?.find { it?.id == deviceInstance1?.boxType?.id })){   
//	            scriptStatus = false
//	        }
//		}
//        return scriptStatus
//    }
	
	public boolean validateScriptBoxTypes(final Map script, final Device deviceInstance){
		boolean scriptStatus = true
		def deviceInstance1 = Device.findById(deviceInstance?.id)
		if(!(script?.boxTypes?.find { it?.id == deviceInstance1?.boxType?.id })){
			scriptStatus = false
		}
		return scriptStatus
	}
	
	/**
	 * Validates whether the RDK version of device is same as that
	 * of the RDK versions specified in the script
	 * @param scriptInstance
	 * @param device rdkVersion
	 * @return
	 */
//	public boolean validateScriptRDKVersion(final Script scriptInstance, final String rdkVersion){
//		boolean scriptStatus = true
//		String versionText = rdkVersion
//		if(rdkVersion){
//			versionText = rdkVersion.trim()
//		}
//		if(versionText && !(versionText?.equals("NOT_AVAILABLE") || versionText?.equals("NOT_VALID") || versionText?.equals("")) ){
//			Script.withTransaction { trns ->
//				def scriptInstance1 = Script.findById(scriptInstance?.id)
//				if(scriptInstance1?.rdkVersions?.size() > 0 && !(scriptInstance1?.rdkVersions?.find { 
//					it?.buildVersion?.equals(versionText) 
//					})){
//					scriptStatus = false
//				}
//			}
//		}
//		return scriptStatus
//	}
	
	public boolean validateScriptRDKVersions(final Map script, final String rdkVersion){
		boolean scriptStatus = true
		String versionText = rdkVersion
		if(rdkVersion){
			versionText = rdkVersion.trim()
		}
		if(versionText && !(versionText?.equals("NOT_AVAILABLE") || versionText?.equals("NOT_VALID") || versionText?.equals("")) ){
				if(script?.rdkVersions?.size() > 0 && !(script?.rdkVersions?.find {
					it?.buildVersion?.equals(versionText)
					})){
					scriptStatus = false
				}
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
    public boolean validateBoxTypeOfScript(final Script scriptInstance, final String boxType){
        boolean scriptStatus = true
        if(!(scriptInstance.boxTypes.find { (it.name).equalsIgnoreCase( boxType ) })){
            scriptStatus = false
        }
        return scriptStatus
    }
    
	
	/**
	 * TO DO : Create a folder with executionDevice name when transfering script
	 * 
	 * Method to execute the versiontransfer.py script stored in filestore folder of webapps
	 * @param realPath
	 * @param filePath
	 * @param executionName
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
	        executeScript( versnFile.getPath() )
	        versnFile.delete()
			
			Device device = Device.findByStbIp(stbIp)
			def devName
			ExecutionDevice.withTransaction {
				devName = ExecutionDevice.get(exectionDeviceId)?.device
	        }
			def dev = device
			if(devName){
				dev = Device.findByStbName(devName)
			}
			if(dev?.boxType?.type?.equalsIgnoreCase(BOXTYPE_CLIENT)){
				getDeviceDetails(dev,logTransferPort,realPath)
			}
			
        }
		catch(Exception ex){			
		}		
    }
	
	
	def getDeviceDetails(Device device, def logTransferPort, def realPath){
		
		try {
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
		} catch (Exception e) {
			e.printStackTrace()
		}		
	}
    
	
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

	
    /**
     * Search execution list based on different search criterias of
     * script, device, and execution from and to dates.
     * @return
     */
    public List multisearch(final String toDate, final String fromDate, final String deviceName, final String resultStatus,
        final String scriptType, final String scriptVal){
        
        def executionList = []
        def executionResult
        if( toDate && fromDate ){
           
            if((!deviceName) && (!resultStatus) && (!scriptType)){
                executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' ")
            }
            else{
             if((scriptType)){
                
                if((scriptType).equals( TEST_SUITE )){
                    if(scriptVal){
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.scriptGroup like '%${scriptVal}%' ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.scriptGroup like '%${scriptVal}%' and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.scriptGroup like '%${scriptVal}%' and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.scriptGroup like '%${scriptVal}%' and b.device like '%${deviceName}%'")
                        }
                    }
                    else{
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.scriptGroup is not null ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.scriptGroup is not null and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.scriptGroup is not null and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.scriptGroup is not null and b.device like '%${deviceName}%'")
                        }
                    }
                }
                else{
                    if(scriptVal){
                        if((!deviceName) && (!resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and (b.script like '%Multiple%' or b.script like '%${scriptVal}%' ) ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and (b.script like '%Multiple%' or b.script like '%${scriptVal}%' ) and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and (b.script like '%Multiple%' or b.script like '%${scriptVal}%' ) and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and (b.script like '%Multiple%' or b.script like '%${scriptVal}%' ) and b.device like '%${deviceName}%'")
                        }
                        executionResult.each{
                            executionList.add(it[INDEX_ZERO])
                        }
                    }
                    else{
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.script is not null ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.script is not null and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.script is not null and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.script is not null and b.device like '%${deviceName}%'")
                        }
                    }
                }
            }
            else{
                if((deviceName) && (resultStatus)){
                    executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                }
                else if((deviceName) && (!resultStatus)){
                    executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.device like '%${deviceName}%'")
                }
                else if((!deviceName) && (resultStatus)){
                    executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${fromDate}' and '${toDate}' and b.result='${resultStatus}'")
                }
            }
            
          }
        }
        else{
            if((scriptType)){
                
                if((scriptType).equals( TEST_SUITE )){
                    if(scriptVal){
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup like '%${scriptVal}%' ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup like '%${scriptVal}%' and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup like '%${scriptVal}%' and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup like '%${scriptVal}%' and b.device like '%${deviceName}%'")
                        }
                    }
                    else{
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup is not null ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup is not null and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup is not null and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup like is not null and b.device like '%${deviceName}%'")
                        }
                    }
                }
                else{
                    if(scriptVal){
                        if((!deviceName) && (!resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and (b.script like '%Multiple%' or b.script like '%${scriptVal}%' ) ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and (b.script like '%Multiple%' or b.script like '%${scriptVal}%' ) and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and (b.script like '%Multiple%' or b.script like '%${scriptVal}%' ) and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and (b.script like '%Multiple%' or b.script like '%${scriptVal}%' ) and b.device like '%${deviceName}%' ")
                        }
                        executionResult.each{
                            executionList.add(it[INDEX_ZERO])
                        }
                    }
                    else{
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.script is not null ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.script is not null and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.script is not null and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionList =  Execution.findAll("from Execution as b where b.script is not null and b.device like '%${deviceName}%'")
                        }
                    }
                }
            }
            else {
                    if((deviceName) && (resultStatus)){
                        executionList = Execution.findAll("from Execution as b where b.device like '%${deviceName}%' and b.result='${resultStatus}' ")
                    }
                    else if((!deviceName) && (resultStatus)){
                        executionList = Execution.findAllByResult( resultStatus )
                    }
                    else if((deviceName) && (!resultStatus)){
                        executionList = Execution.findAllByDeviceIlike( deviceName )
                    }
                }
        }
        return executionList
    }
		
	/**
	 * Method to execute callgetdevices.py script with required parameters.
	 * eg: python callgetdevices.py 192.168.160.130 8088
	 * It will return execution result of callgetdevices.py.
	 * 
	 * @param device
	 * @return outputData
	 */
	def executeGetDevices(Device device){
		def outputArray
		def executionResult
		def outputData = ""
		def macIdList = []
		def absolutePath
		def boxIp = device?.stbIp
		def port = device?.statusPort

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callgetdevices.py").file
		absolutePath = layoutFolder.absolutePath

		try {
			if(boxIp != null && port != null ){
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				boxIp,
				port
			]

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			outputData = scriptExecutor.executeScript(cmd,1)
			//	 outputData = "DEVICES=<incomplete>,bb:cc:EE:dd:24,bb:cc:EE:dd:26,"  // Dummy data for testing purpose
		}

		} catch (Exception e) {
			e.printStackTrace()
		}

		return outputData
	}
	
	/**
	 * Method to fetch the RDK version of the device
	 * @param device
	 * @return
	 */
	def getRDKBuildVersion(Device device){
		
		def outputData
		def absolutePath
		def boxIp = device?.stbIp
		def port = device?.agentMonitorPort

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callGetRDKVersion.py").file
		absolutePath = layoutFolder.absolutePath

		try {
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
		} catch (Exception e) {
			e.printStackTrace()
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


	/**
	 * Method to parse the results obtained after the execution of callgetdevices.py script.
	 * @param executionResult
	 * @return macIdList - List of valid macIds if exists.
	 */
	def parseExecutionResult(final String executionResult){

		List macIdList = []
		def outputData
		def deviceResponse
		def outputArray		
		macIdList.removeAll(macIdList)

		outputData = executionResult.toString().trim()
		if(outputData){
			if( outputData != NO_DEVICES_MSG && outputData != "AGENT_NOT_FOUND"  && outputData != "FAILURE" && outputData != "" && outputData != " " && outputData != null){
				deviceResponse = outputData.split("=")
				if(deviceResponse.length > 1){
					if(deviceResponse[1]){
						outputArray =  deviceResponse[1].split(',')
						if(outputArray.length > 0 ){
							for(int i=0; i<outputArray.length; i++){
								if(outputArray[i] != "<incomplete>" && outputArray[i] != "" && outputArray[i] != " "){									
									if(outputArray[i] != "\""){
										macIdList << outputArray[i]
									}																										
								}
							}
						}
					}
				}
			}
		}		
		return macIdList
	}


	/**
	 * Method to execute callsetroute.py script with required parameters.
	 * It will return execution result of callsetroute.py.
	 * 
	 * eg: python callsetroute.py 192.168.160.130 8088 b4:f2:e8:de:1b:0e 10001 20001 30001
	 * @param device
	 * @return outputData
	 */
	def executeSetRoute(final Device parentDevice, final Device childDevice){

		def outputData
		def absolutePath
		def deviceIP = parentDevice?.stbIp
		def devicePort = parentDevice?.statusPort
		def clientMAC
		def clientAgentPort
		def clientStatusPort
		def clientLogTransferPort
		def clientAgentMonitorPort

		clientMAC = childDevice?.macId
		clientAgentPort = childDevice?.stbPort
		clientStatusPort = childDevice?.statusPort
		clientLogTransferPort = childDevice?.logTransferPort
		clientAgentMonitorPort = childDevice?.agentMonitorPort

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callsetroute.py").file
		absolutePath = layoutFolder.absolutePath

		try {
			if(clientMAC != null && clientAgentPort != null && clientStatusPort != null && clientLogTransferPort != null && 
					clientAgentMonitorPort  != null ){
				String[] cmd = [
				                PYTHON_COMMAND,
				                absolutePath,
				                deviceIP,
				                devicePort,
				                clientMAC,
				                clientAgentPort,
				                clientStatusPort,
				                clientLogTransferPort,
				                clientAgentMonitorPort
				                ]
				                		
				                		ScriptExecutor scriptExecutor = new ScriptExecutor()
				outputData = scriptExecutor.executeScript(cmd,1)
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
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
	public void updateExecutionResults(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId, 
		final String timeDiff, final String singleScriptExecTime){
		ExecutionResult executionResult = ExecutionResult.findById(executionResultId)
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput, c.executionTime = :newTime  where c.id = :execId",
				[newOutput: outputData, newTime: singleScriptExecTime, execId: executionResultId])		
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime where c.id = :execId",
				[newStatus: outputData, newTime: timeDiff, execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.executionTime = :newTime where c.id = :execDevId",
				[newTime: timeDiff, execDevId: executionDeviceId.toLong()])		
	}
	
	public void updateExecutionStatus(final String status, final long executionId){
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus where c.id = :execId",
				[newStatus: status, execId: executionId.toLong()])
	}
	
	public void updateExecutionSkipStatusWithTransaction(final String status, final long executionId){
		Execution.withTransaction {
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.result = :reslt where c.id = :execId",
				[newStatus: status, reslt: status, execId: executionId.toLong()])
		}
	}
	
	public void updateExecutionDeviceSkipStatusWithTransaction(final String status, final long executionId){
		ExecutionDevice.withTransaction {
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat where c.id = :execDevId",
				[newStat: status, execDevId: executionId])
		}
	}
	
	
	public void updateExecutionStatusData(final String status, final long executionId){
		Execution.withTransaction {
		Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus where c.id = :execId",
				[newStatus: status, execId: executionId.toLong()])
		}
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
		try{
		ExecutionResult executionResult = ExecutionResult.findById(executionResultId)
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput , c.status = :newStatus, c.executionTime = :newTime where c.id = :execId",
				[newOutput: outputData, newStatus: "SCRIPT TIME OUT", newTime: singleScriptExecTime, execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus,  c.result = :newStatus, c.executionTime = :newTime where c.id = :execId",
				[newStatus: outputData, newStatus: "FAILURE", newTime: timeDiff, execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat, c.executionTime = :newTime where c.id = :execDevId",
				[newStat: "FAILURE", newTime: timeDiff, execDevId: executionDeviceId.toLong()])
		}
		catch(Exception e){
			e.printStackTrace()
		}
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

		ExecutionResult executionResult = ExecutionResult.findById(executionResultId)
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput, c.status = :newStatus, c.executionTime = :newTime where c.id = :execId",
				[newOutput: resultData, newStatus: "FAILURE", newTime: singleScriptExecTime, execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime, c.result = :newStatus where c.id = :execId",
				[newStatus: resultData, newTime: timeDiff, newStatus: "FAILURE", execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat, c.executionTime = :newTime where c.id = :execDevId",
				[newStat: "FAILURE", newTime: timeDiff, execDevId: executionDeviceId.toLong()])
		
	}
	
	def Groups getGroup(){
		def user = User.findByUsername(SecurityUtils.subject.principal)
		def group = Groups.findById(user.groupName?.id)
		return group
	}
	
	/**
	 * Method to save details of execution in Execution Domain
	 * @param execName
	 * @param scriptName
	 * @param deviceName
	 * @param scriptGroupInstance
	 * @return
	 */
	public boolean saveExecutionDetails(final String execName, String scriptName, String deviceName,
	 ScriptGroup scriptGroupInstance , String appUrl,String isBenchMark , String isSystemDiagnostics,String rerun){
		def executionSaveStatus = true
		int scriptCnt = 0
		if(scriptGroupInstance?.scriptList?.size() > 0){
			scriptCnt = scriptGroupInstance?.scriptList?.size()
		}
		
		try {
			Execution execution = new Execution()
			execution.name = execName
			execution.script = scriptName
			execution.device = deviceName
			execution.scriptGroup = scriptGroupInstance?.name
			execution.result = UNDEFINED_STATUS
			execution.executionStatus = INPROGRESS_STATUS
			execution.dateOfExecution = new Date()
			execution.groups = getGroup()
			execution.applicationUrl = appUrl
			execution.isRerunRequired = rerun?.equals("true")
			execution.isBenchMarkEnabled = isBenchMark?.equals("true")
			execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals("true")
			execution.scriptCount = scriptCnt
			if(! execution.save(flush:true)) {				
				log.error "Error saving Execution instance : ${execution.errors}"
				executionSaveStatus = false
			}
		}
		catch(Exception th) {
			th.printStackTrace()
			executionSaveStatus = false
		}
		return executionSaveStatus
	}
	 
	 public void saveRepeatExecutionDetails(String execName , String deviceName , int currentExecutionCount, int pending){
		 
		try {
			Execution exe = Execution.findByName(execName)
			RepeatPendingExecution.withTransaction{
				RepeatPendingExecution rExecution = new RepeatPendingExecution()
				rExecution.deviceName = deviceName
				rExecution.completeExecutionPending = pending
				rExecution.currentExecutionCount = currentExecutionCount
				rExecution.executionName = execName
				rExecution.status = "PENDING"
				if(!rExecution.save(flush:true)){
				}
			}

		} catch (Exception e) {
		
			 e.printStackTrace()
		 }
	 }
	 
	public void setPerformance(final Execution executionInstance, final String filePath){
		try{
			Execution execution = executionInstance
			def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
			def executionResult
			def benchmarkPerformanceFile
			def memoryPerfomanceFile
			def cpuPerformanceFile
			Performance performanceInstance
			def stringArray
			executionDevice.each{ executiondevice ->
				executionResult = ExecutionResult.findAllByExecutionDevice(executiondevice)
				executionResult.each { executionresult ->
					benchmarkPerformanceFile = new File(filePath+"//logs//performance//${executionInstance?.id}//${executiondevice?.id}//${executionresult?.id}//benchmark.log")
					cpuPerformanceFile = new File(filePath+"//logs//performance//${executionInstance?.id}//${executiondevice?.id}//${executionresult?.id}//cpu.log")
					memoryPerfomanceFile = new File(filePath+"//logs//performance//${executionInstance?.id}//${executiondevice?.id}//${executionresult?.id}//memused.log")
					if(memoryPerfomanceFile.exists() || cpuPerformanceFile.exists() || benchmarkPerformanceFile.exists()){
						execution.isPerformanceDone = true
						execution.save(flush:true)
					}
					if(benchmarkPerformanceFile.exists()){
						int count = 0
						benchmarkPerformanceFile?.eachLine { line ->
							if(!line?.isEmpty()){
								if(count < 6){
									stringArray = line.split("~")
									if(stringArray.size() >= 2){
										if(stringArray[0] && stringArray[1]){
											performanceInstance = new Performance()
											performanceInstance.executionResult = executionresult
											performanceInstance.performanceType = "BENCHMARK"
											performanceInstance.processName = stringArray[0].trim()
											performanceInstance.processValue = stringArray[1].trim()
											performanceInstance.save(flush:true)
											executionresult.addToPerformance(performanceInstance)
										}
									}
								}
								count++;
							}
						}
						benchmarkPerformanceFile.delete()
					}
					if(cpuPerformanceFile.exists()){
						
						List cpuValue = []
						cpuPerformanceFile?.eachLine { line ->
							if(!line?.isEmpty()){
								String input = line?.trim() 
								try {
									float val = Float.parseFloat(input)
									cpuValue.add(100.00 - val)
								} catch (Exception e) {
									e.printStackTrace()
								}
							}
						}
						
						float starting = cpuValue.first()
						float ending = cpuValue.last()
						float sumVal = cpuValue.sum()
						float avg = sumVal / cpuValue.size()
						cpuValue = cpuValue?.sort()
						float peak = cpuValue?.last() 
						
						addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_CPU, Constants.CPU_STARTING, starting)
						addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_CPU, Constants.CPU_ENDING, ending)
						addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_CPU, Constants.CPU_AVG, avg)
						addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_CPU, Constants.CPU_PEAK, peak)
						
						cpuPerformanceFile?.delete()
					}
					if(memoryPerfomanceFile?.exists()){
						memoryFileParser(memoryPerfomanceFile,executionresult)
						memoryPerfomanceFile?.delete()
					}
				}
				
				

			}
			new File(filePath+"//logs//performance//${executionInstance?.id}")?.deleteDir()
		}catch(Exception e){
				e.printStackTrace()
			try{
				new File(filePath+"//logs//performance//${executionInstance?.id}")?.deleteDir()
			}catch(Exception ex){
			}

		}
	}	
	
	public void saveSkipStatus(def executionInstance , def executionDevice , def scriptInstance , def deviceInstance){
		ExecutionResult.withTransaction { resultstatus ->
			try {
				ExecutionResult executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance.name
				executionResult.device = deviceInstance.stbName
				executionResult.dateOfExecution = new Date()
				executionResult.status = SKIPPED_STATUS
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
	
	public void saveNotApplicableStatus(def executionInstance , def executionDevice , def scriptInstance , def deviceInstance, String reason){
		try{
		ExecutionResult.withTransaction { resultstatus ->
			try {
				ExecutionResult executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance?.name
				executionResult.device = deviceInstance?.stbName
				executionResult.status = Constants.NOT_APPLICABLE_STATUS
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
	
	public boolean isAborted(def executionName){
		Execution.withTransaction {
			def ex = Execution.findByName(executionName)
			if(ex){
				return ex?.isAborted
			}
		}
		return false;
	}
	
	public void abortExecution(def executionId){
		Long exId = Long.parseLong(""+executionId)
		try {
			Execution.withTransaction {
				Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus , c.isAborted = :abort where c.id = :execId",
						[newStatus: ABORTED_STATUS, abort: true, execId: exId?.toLong()])
			}
		} catch (Exception e) {
		}

	}
	
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
	
	public void saveExecutionDeviceStatus(boolean isAborted, def exDevId){

		String status = ""
		if(isAborted){
			status = ABORTED_STATUS
		}else{
			status = COMPLETED_STATUS
		}
		try {
			ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStatus  where c.id = :execId",
					[newStatus: status, abort: isAborted, execId: exDevId?.toLong()])

		} catch (Exception e) {
			e.printStackTrace()
		}

}
	
	public void savePausedExecutionStatus(def exId){
		try {
			Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus where c.id = :execId",
					[newStatus: "PAUSED", execId: exId?.toLong()])

		} catch (Exception e) {
			e.printStackTrace()
		}

}
	
	public void saveExecutionDeviceStatusData(String status, def exDevId){
		
				try {
					ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStatus  where c.id = :execId",
							[newStatus: status, execId: exDevId?.toLong()])
		
				} catch (Exception e) {
					e.printStackTrace()
				}
		
		}
	
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def resetAgent(def deviceInstance,String hardReset){
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
		def absolutePath = layoutFolder.absolutePath
		String[] cmd = [
			PYTHON_COMMAND,
			absolutePath,
			deviceInstance?.stbIp,
			deviceInstance?.agentMonitorPort,
			hardReset
		]
		ScriptExecutor scriptExecutor = new ScriptExecutor()
		def resetExecutionData = scriptExecutor.executeScript(cmd,1)
		callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		Thread.sleep(4000)
	}
	
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def resetAgent(def deviceInstance){
		try {
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
		} catch (Exception e) {
			e.printStackTrace()
		}
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
		println "Reboot Box "+deviceInstance
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
	
	def memoryFileParser(File memFile, def executionresult){
		def memUsed = []
		def memAvailable = []
		def memPer = []
		
		memFile?.eachLine { line ->
			StringTokenizer st = new StringTokenizer(line)
			if(st.countTokens() == 3){
				memAvailable.add(getLongValue(st?.nextToken()))
				memUsed.add(getLongValue(st?.nextToken()))
				memPer.add(getFloatValue(st?.nextToken()))
			}
		}
		
		try {
			
			
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_USED_START, memUsed.first())
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_USED_END, memUsed.last())
			memUsed = memUsed?.sort()
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_USED_PEAK, memUsed.last())
			
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_AVAILABLE_START, memAvailable.first())
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_AVAILABLE_END, memAvailable.last())
			memAvailable = memAvailable?.sort()
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_AVAILABLE_PEAK, memAvailable.last())
			
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_PERC_START, memPer.first())
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_PERC_END, memPer.last())
			memPer = memPer?.sort()
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_PERC_PEAK, memPer.last())
			
		} catch (Exception e) {
		println " ERROR >>> "+e.getMessage() + "ee "+e.getCause()
			e.printStackTrace()
		}
		
		
		
	}
	
	def getLongValue(String val){
		try {
			return Long.parseLong(val)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return 0
	}
	
	def getFloatValue(String val){
		try {
			return Float.parseFloat(val)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return 0.0
	}
	
	def addPerformanceParam(def executionresult , def performanceType , def processName , def value){
		Performance performanceInstance = new Performance()
		performanceInstance.executionResult = executionresult
		performanceInstance.performanceType = performanceType
		performanceInstance.processName = processName
		performanceInstance.processValue = value
		performanceInstance.save(flush:true)
		executionresult.addToPerformance(performanceInstance)
	}
	
	
}
