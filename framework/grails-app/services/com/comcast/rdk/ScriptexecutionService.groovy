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

import com.google.gson.JsonArray
import com.google.gson.JsonObject
import com.google.gson.JsonPrimitive
import java.util.List;
import java.util.concurrent.FutureTask
import java.util.regex.Matcher
import java.util.regex.Pattern

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.Executors;
/**
 * Service class for the Asynchronous Execution of Scripts for REST.
 * @author sreejasuma
 */

class ScriptexecutionService {
    /**
     * Injecting executor service.
     */
    static ExecutorService executorService = Executors.newCachedThreadPool()
	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication
	
	def executionService
	
	
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
			if(! execution.save(flush:true)) {
				log.error "Error saving Execution instance : ${execution.errors}"
				executionSaveStatus = false
			}
		}
		catch(Exception th) {
			//th.printStackTrace()			
			executionSaveStatus = false
		}
		return executionSaveStatus
	}
	

    def executeScriptGroup(ScriptGroup scriptGroup, final String boxType,  final String execName, final String execDeviceId,
        Device deviceInstance, final String url, final String filePath, final String realPath, final String callbackUrl ){
        Future<String> future =  executorService.submit( { executeScriptGrp(scriptGroup, boxType, execName, execDeviceId, deviceInstance, 
            url, filePath, realPath, callbackUrl)} as Callable< String > )
  
    }
		
	def String getCurlCommand(final String jsonString, final String callbackUrl){
		String curlCommand
		try{
			File jenkFile = grailsApplication.parentContext.getResource("//fileStore//jenkinscredential.txt").file
			String valueString
			String jenkUser=""
			String jenkPwd=""
			if(jenkFile.exists()){
			jenkFile.eachLine {	
				if (it.startsWith('JENK_USER:')) {
					valueString = it
					valueString = valueString.replaceAll("JENK_USER:", "")
					jenkUser = valueString.trim()
				}
				else if(it.startsWith('JENK_PWD:')){
					valueString = it
					valueString = valueString.replaceAll("JENK_PWD:", "")
					jenkPwd = valueString.trim()
				}
			}
		}
			/*String jsonString = jsonData.toString();
			jsonString = jsonString.replaceAll("\"", "\\\\\"")*/
			
			if(jenkUser && jenkPwd && callbackUrl){
				curlCommand = "curl --fail -X POST --insecure --user ${jenkUser}:${jenkPwd} ${callbackUrl} -F json=\"{\\\"parameter\\\":[{\\\"name\\\":\\\"TDK_DATA\\\",\\\"value\\\":\\\"${jsonString}\\\"}]}\" --verbose"				
				//curlCommand = "curl --fail -X POST --insecure --user ${jenkUser}:${jenkPwd} ${callbackUrl} -F json=\"${jsonString}\" --verbose"						
			}			
		}
		catch(Exception ex){	
			ex.printStackTrace()		
		}
		return curlCommand
	}
        
    def executeScriptGrp(ScriptGroup scriptGroup, final String boxType, final String execName, final String execDeviceId,
        Device deviceInstance, final String url, final String filePath, final String realPath, final String callbackUrl){ 
		try{  
		
			List<Script> validScripts = new ArrayList<Script>()
			scriptGroup.scripts.each { script ->
			
	           if(validateBoxTypeOfScript(script,boxType)){
				   validScripts << script
	           }
			   
	        }
			int scriptGrpSize = validScripts?.size()
			
			int scriptCounter = 0
			def isMultiple = "true"
			validScripts.each{ scriptInstance ->
				scriptCounter++
				if(scriptCounter == scriptGrpSize){
					isMultiple = "false"
				}
				def htmlData = executeScripts(execName, execDeviceId, scriptInstance , deviceInstance , url, filePath, realPath, isMultiple)
				
				if(isMultiple.equals("false")){					
					Execution.withTransaction {
						Execution executionInstance = Execution.findByName(execName)
						executionInstance.executionStatus = "COMPLETED"
						executionInstance.save(flush:true)			
					}				
				}
			}
			
			if(callbackUrl){
			
				String curlCommand = getCurlCommand(thirdPartyJsonResult(execName,url), callbackUrl)
	
				File newFile = new File(filePath, execName+"-curlscript.sh");
				boolean isFileCreated = newFile.createNewFile()
				if(isFileCreated) {
					newFile.setExecutable(true, false )
				}
	
				if(curlCommand){
					PrintWriter fileNewPrintWriter = newFile.newPrintWriter();
					fileNewPrintWriter.print( curlCommand )
					fileNewPrintWriter.flush()
					fileNewPrintWriter.close()
					def absolutePath = newFile.absolutePath
	
					if(absolutePath != null){
			
						String[] cmd = [
							"sh",
							absolutePath
						]
			
						ScriptExecutor scriptExecutor = new ScriptExecutor()
						def outputData = scriptExecutor.executeScript(cmd)
						if(newFile.exists()){
							newFile.delete();
						}
					}
				}	
			}
					
		}
		catch(Exception e){	
			e.printStackTrace()		
		}
    }
    
		
		def String thirdPartyJsonResult(final String execName, final String appurl ){
			JsonArray jsonArray = new JsonArray()
			JsonObject compNode
			JsonObject deviceNode
			JsonObject executionNode
			String appUrl = appurl
			String url
			appUrl = appUrl + "/execution/getDetailedTestResult?execResId="
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

								/*JsonArray failedFunArray = new JsonArray()
								List fun = []
								JsonPrimitive el = new JsonPrimitive("fun1");
								JsonPrimitive el2 = new JsonPrimitive("fun2");
								failedFunArray.add(el)
								failedFunArray.add(el2)
								scriptStatusNode.add("FailedFunctions", failedFunArray)*/
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

							/*	JsonArray failedFunArray = new JsonArray()
								List fun = []
								JsonPrimitive el = new JsonPrimitive("fun1");
								JsonPrimitive el2 = new JsonPrimitive("fun2");
								failedFunArray.add(el)
								failedFunArray.add(el2)
								scriptStatusNode.add("FailedFunctions", failedFunArray)*/
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
					executionNode.add("DEVICES", jsonArray)
				}
			
			
			JsonObject paramObject = new JsonObject();
			
			JsonArray paramArray = new JsonArray();
			JsonArray dataArray = new JsonArray();
			dataArray.add(executionNode)
			
			String dataString = dataArray.toString();
			//dataString  = dataString.replaceAll("\"", "")
			dataString  = dataString.replaceAll("\"", "\\\\\\\\\\\\\"")
			
			
			/*JsonObject tdkObject = new JsonObject();
			tdkObject.addProperty("name", "TDK_DATA")
			tdkObject.addProperty("value", dataString)
			
			paramArray.add(tdkObject);
			
			paramObject.add("parameter", paramArray);
						
			return paramObject*/
			return dataString
			
		}
    
    /**
     * Method to execute the script
     * @param scriptGroupInstance
     * @param scriptInstance
     * @param deviceInstance
     * @param url
     * @return
     */
    def String executeScripts(String executionName, String execDeviceId, Script scriptInstance,
            Device deviceInstance, final String url, final String filePath, final String realPath, final String isMultiple ) {
    
			
        String htmlData = ""

        String scriptData = convertScriptFromHTMLToPython(scriptInstance.scriptContent)
         
        String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES

		def deviceInstance1 = Device.findById(deviceInstance.id,[lock: true])

        def executionInstance = Execution.findByName(executionName,[lock: true])
        def executionId = executionInstance?.id
        Date executionDate = executionInstance?.dateOfExecution
        
        def execStartTime = executionDate?.getTime()

		def executionDeviceInstance = ExecutionDevice.findById(execDeviceId)
		
        def executionResult
        ExecutionResult.withTransaction { resultstatus ->
            try {
                executionResult = new ExecutionResult()
                executionResult.execution = executionInstance
				executionResult.executionDevice = executionDeviceInstance
                executionResult.script = scriptInstance.name
                executionResult.device = deviceInstance.stbName
                if(! executionResult.save(flush:true)) {
                    log.error "Error saving executionResult instance : ${executionResult.errors}"
                }
                resultstatus.flush()
            }
            catch(Throwable th) {
                resultstatus.setRollbackOnly()
            }
        }
		
		String gatewayIp = deviceInstance1?.gatewayIp
        
        def executionResultId = executionResult?.id
        scriptData = scriptData.replace( IP_ADDRESS , stbIp )
        scriptData = scriptData.replace( PORT , deviceInstance?.stbPort )

		scriptData = scriptData.replace( REPLACE_TOKEN, LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath +SINGLE_QUOTES + COMMA_SEPERATOR +
			executionId  + COMMA_SEPERATOR + execDeviceId + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.logTransferPort + COMMA_SEPERATOR + deviceInstance?.statusPort + COMMA_SEPERATOR +
			scriptInstance?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR+ SINGLE_QUOTES + "false" + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + "false" + SINGLE_QUOTES + COMMA_SEPERATOR + 
			SINGLE_QUOTES + isMultiple + SINGLE_QUOTES + COMMA_SEPERATOR )//+ gatewayIp + COMMA_SEPERATOR)
		
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

        String outData = executeScript( file.getPath(), scriptInstance.executionTime )

		
        outData?.eachLine { line ->
            htmlData += (line + HTML_BR )
        }
        
        file.delete()
        String outputData = htmlData
        
        Date execEndDate = new Date()
        def execEndTime =  execEndDate.getTime()

        def timeDifference = ( execEndTime - execStartTime  ) / 60000;
        
        String timeDiff =  String.valueOf(timeDifference)
		
       /* if(outputData) {
			
			executionService.updateExecutionResults(outputData,executionResultId,executionId, executionDeviceInstance?.id, timeDiff)
			
           /* Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime where c.id = :execId",
                [newStatus: outputData, newTime: timeDiff, execId: executionId.toLong()])*/
       // }
		
		if(htmlData.contains(TDK_ERROR)){
			htmlData = htmlData.replaceAll(TDK_ERROR,"")
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
			}
			executionService.updateExecutionResultsError(htmlData,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString())
			Thread.sleep(5000)
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
			Thread.sleep(6000)
		}
		else{
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
				String outputData1 = htmlData				
				executionService.updateExecutionResults(outputData1,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString())
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
						ScriptExecutor scriptExecutor = new ScriptExecutor()
						def resetExecutionData = scriptExecutor.executeScript(cmd)
						htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
						executionService.updateExecutionResults(htmlData,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id)
						Thread.sleep(6000)
				}
			}
		}        
        return htmlData
    }
			
    /**
     * Method to call the script executor to execute the script
     * @param executionData
     * @return
     */
    public String executeScript(final String executionData, final int executeTime) {
        new ScriptExecutor().execute( getCommand( executionData ),executeTime)
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
    public boolean validateBoxTypeOfScript(Script scriptInstance, String boxType){  
        boolean scriptStatus = true
        if(!(scriptInstance.boxTypes.find { (it.name).equalsIgnoreCase( boxType ) })){
            scriptStatus = false
        }
        return scriptStatus
    }
    
    /**
     * Method to execute the versiontransfer.py script stored in filestore folder of webapps
     *
     * @param filePath
     * @param executionName
     * @param stbIp
     * @return
     */
    def executeVersionTransferScript(final String realPath, final String filePath, final String executionName, final String stbIp, final String logTransferPort){
        
        def executionInstance = Execution.findByName(executionName)
        String fileContents = new File(filePath+DOUBLE_FWD_SLASH+VERSIONTRANSFER_FILE).text
        
        fileContents = fileContents.replace(IP_ADDRESS, STRING_QUOTES+stbIp+STRING_QUOTES)
		
		fileContents = fileContents.replace(PORT, logTransferPort)
		
        String versionFilePath = "${realPath}//logs//version//${executionInstance?.id}_version.txt"
        fileContents = fileContents.replace(LOCALFILE, STRING_QUOTES+versionFilePath+STRING_QUOTES)
        
        String versionFile = TEMP_VERSIONFILE_NAME
                       
        File versnFile = new File(filePath, versionFile)
        boolean isVersionFileCreated = versnFile.createNewFile()
        if(isVersionFileCreated) {
            versnFile.setExecutable(true, false )
        }
        PrintWriter versnNewPrintWriter = versnFile.newPrintWriter();
        versnNewPrintWriter.print( fileContents )
        versnNewPrintWriter.flush()
                
        executeScript( versnFile.getPath() )
        versnFile.delete()
    }
	
	
	    

}
