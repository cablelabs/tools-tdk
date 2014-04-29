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
	
	def getLogFileNames(final String realPath, final String executionId, final String executionDeviceId){
		def mapVals = [:]
		def summaryFilePath = "${realPath}//logs//${executionId}//${executionDeviceId}"//_TestSummary"
		try{
			File directory = new File(summaryFilePath);
			List<File> foundFiles = new ArrayList<File>()
			
			directory.eachFile {
				if (it.isFile()) {
					String fileName = it.getName()
					if(fileName.startsWith( "${executionId}_TestSummary" )){
						foundFiles << new File("${realPath}//logs//${executionId}//${executionDeviceId}//${fileName}")
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
			  String filePath = "${realPath}//logs//${executionId}//${executionDeviceId}"
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

	
	
	def getCrashLogFileNames(final String realPath, final String executionId, final String executionDeviceId){
		def mapVals = [:]
		try{
			  String filePath = "${realPath}//logs//crashlogs"
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
        new ScriptExecutor().execute( getCommand( executionData ))
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
        }
		catch(Exception ex){
			
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
		def outputData
		def macIdList = []
		def absolutePath
		def boxIp = device?.stbIp
		def port = device?.statusPort

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callgetdevices.py").file
		absolutePath = layoutFolder.absolutePath

		if(boxIp != null && port != null ){
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				boxIp,
				port
			]

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			outputData = scriptExecutor.executeScript(cmd)
			//	 outputData = "DEVICES=<incomplete>,bb:cc:EE:dd:24,bb:cc:EE:dd:26,"  // Dummy data for testing purpose
		}

		return outputData
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
			outputData = scriptExecutor.executeScript(cmd)
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
	public void updateExecutionResults(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId, final String timeDiff){
		ExecutionResult executionResult = ExecutionResult.findById(executionResultId)
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput  where c.id = :execId",
				[newOutput: outputData, execId: executionResultId])
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
	public void updateExecutionResults(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId){

		ExecutionResult executionResult = ExecutionResult.findById(executionResultId)
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput , c.status = :newStatus  where c.id = :execId",
				[newOutput: outputData, newStatus: "SCRIPT TIME OUT", execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.result = :newStatus where c.id = :execId",
				[newStatus: outputData, newStatus: "FAILURE", execId: executionId.toLong()])
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
	public void updateExecutionResultsError(final String resultData,final long executionResultId, final long executionId, final long executionDeviceId,final String timeDiff){

		ExecutionResult executionResult = ExecutionResult.findById(executionResultId)
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput , c.status = :newStatus  where c.id = :execId",
				[newOutput: resultData, newStatus: "FAILURE", execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime, c.result = :newStatus where c.id = :execId",
				[newStatus: resultData, newTime: timeDiff, newStatus: "FAILURE", execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat where c.id = :execDevId",
				[newStat: "FAILURE", execDevId: executionDeviceId.toLong()])
		
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
	 ScriptGroup scriptGroupInstance){
		def executionSaveStatus = true
		try {
			Execution execution = new Execution()
			execution.name = execName
			execution.script = scriptName
			execution.device = deviceName
			execution.scriptGroup = scriptGroupInstance?.name
			execution.result = UNDEFINED_STATUS
			execution.dateOfExecution = new Date()
			execution.groups = getGroup()
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
	 
	 
	public void setPerformance(final Execution executionInstance, final String filePath){
		try{
		Execution execution = executionInstance
		def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
		def executionResult
		def benchmarkPerformanceFile
		def cpuPerformanceFile
		def sysStatFile
		Performance performanceInstance
		def stringArray
		executionDevice.each{ executiondevice ->
			executionResult = ExecutionResult.findAllByExecutionDevice(executiondevice)
			executionResult.each { executionresult ->
				benchmarkPerformanceFile = new File(filePath+"//logs//performance//${executionInstance?.id}//${executiondevice?.id}//${executionresult?.id}//benchmark.log")
				cpuPerformanceFile = new File(filePath+"//logs//performance//${executionInstance?.id}//${executiondevice?.id}//${executionresult?.id}//systemDiagnostics.log")
				sysStatFile = new File(filePath+"//logs//performance//${executionInstance?.id}//${executiondevice?.id}//${executionresult?.id}//sysStat.log")
				
				if(benchmarkPerformanceFile.exists() || cpuPerformanceFile.exists()){
					execution.isPerformanceDone = true
					execution.save(flush:true)
				}
				if(benchmarkPerformanceFile.exists()){
					int count = 0
					benchmarkPerformanceFile.eachLine { line ->
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
				}
				benchmarkPerformanceFile.delete()	
				
				
				
					boolean beginOfSysstat = false
					cpuPerformanceFile.eachLine { line ->
						if(!line?.isEmpty()){
						
							if(line.startsWith("ENDOFTOPCOMMAND_!")){
								beginOfSysstat = true
							}
							if(beginOfSysstat){
								if(line.startsWith("%cpu;")){
									stringArray = line?.split(";")
									performanceInstance = new Performance()
									performanceInstance.executionResult = executionresult
									performanceInstance.performanceType = "SYSTEMDIAGNOSTICS"
									performanceInstance.processName = "%CPU"
									performanceInstance.processValue = stringArray[1]?.trim()
									performanceInstance.save(flush:true)
									executionresult.addToPerformance(performanceInstance)
								}
								if(line.startsWith("%memused")){
									stringArray = line?.split(";")
									performanceInstance = new Performance()
									performanceInstance.executionResult = executionresult
									performanceInstance.performanceType = "SYSTEMDIAGNOSTICS"
									performanceInstance.processName = "%MEMORY"
									performanceInstance.processValue = stringArray[1]?.trim()
									performanceInstance.save(flush:true)
									executionresult.addToPerformance(performanceInstance)
								}
								else if( line.startsWith("%swpused")){
									stringArray = line?.split(";")
									performanceInstance = new Performance()
									performanceInstance.executionResult = executionresult
									performanceInstance.performanceType = "SYSTEMDIAGNOSTICS"
									performanceInstance.processName = "SWAPING"
									performanceInstance.processValue = stringArray[1]?.trim()
									performanceInstance.save(flush:true)
									executionresult.addToPerformance(performanceInstance)
								}
								else if(line.startsWith("ldavg-1;")){
									stringArray = line?.split(";")
									performanceInstance = new Performance()
									performanceInstance.executionResult = executionresult
									performanceInstance.performanceType = "SYSTEMDIAGNOSTICS"
									performanceInstance.processName = "LOAD AVERAGE"
									performanceInstance.processValue = stringArray[1]?.trim()
									performanceInstance.save(flush:true)
									executionresult.addToPerformance(performanceInstance)
								}
								else if(line.startsWith("pgpgin/s")){
									stringArray = line?.split(";")
									performanceInstance = new Performance()
									performanceInstance.executionResult = executionresult
									performanceInstance.performanceType = "SYSTEMDIAGNOSTICS"
									performanceInstance.processName = "PAGING : pgpgin/s"
									performanceInstance.processValue = stringArray[1]?.trim()
									performanceInstance.save(flush:true)
									executionresult.addToPerformance(performanceInstance)
								}
								else if(line.startsWith("pgpgout/s")){
									stringArray = line?.split(";")
									performanceInstance = new Performance()
									performanceInstance.executionResult = executionresult
									performanceInstance.performanceType = "SYSTEMDIAGNOSTICS"
									performanceInstance.processName = "PAGING : pgpgout/s"
									performanceInstance.processValue = stringArray[1]?.trim()
									performanceInstance.save(flush:true)
									executionresult.addToPerformance(performanceInstance)
								}
								
							}	
						}
				}
					
				}
				cpuPerformanceFile.delete()				
		}
		new File(filePath+"//logs//performance//${executionInstance?.id}").deleteDir()
		}catch(Exception e){	
			try{			
				new File(filePath+"//logs//performance//${executionInstance?.id}").deleteDir()
			}catch(Exception ex){
			}
				
		}
	}	
	
	
	
}
