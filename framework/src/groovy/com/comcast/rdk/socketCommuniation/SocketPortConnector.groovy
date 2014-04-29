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
package com.comcast.rdk.socketCommuniation

import static com.comcast.rdk.Constants.COMMA_SEPERATOR
import static com.comcast.rdk.Constants.UNDERSCORE
import com.comcast.rdk.Device
import com.comcast.rdk.Script
import com.comcast.rdk.ScriptExecutor

public class SocketPortConnector extends Thread
{

    private static ServerSocket serverSocket;

	private static String fileTransferPath
	private static String destinationCrashFile
	private static final String CRASH_TOKEN = "CRASH_"
	public SocketPortConnector(){
		
	}

    public SocketPortConnector(int port, String filePath, String destFile) throws IOException
    {
	   fileTransferPath = filePath
	   destinationCrashFile = destFile
       serverSocket = new ServerSocket(port);	   
       //serverSocket.setSoTimeout(10000);	 		   
    }
	
	public static closeServerSocket(){
	//	println "closeServerSocket ---------------------------------- "
		serverSocket.close()		
	}

    public void run()
    {
       while(!(serverSocket.closed))
       {
          try
          {
			//  println " BEGIN "		
             Socket server = serverSocket.accept()
             BufferedReader br = new BufferedReader(new InputStreamReader(server.getInputStream(), "UTF8"))             
             String dataFromSocket = br.readLine()
			 if(dataFromSocket.toString().startsWith(CRASH_TOKEN)){
				 String[] dataArray1 = dataFromSocket.split( UNDERSCORE )
				 String details = dataArray1[1]
				 String[] detailsArray = details.split( COMMA_SEPERATOR )
				 String execId = detailsArray[0]
				 String deviceId = detailsArray[1]
				 String scriptId = detailsArray[2]
				 String execDeviceId = detailsArray[3]

				 def devStbIp
				 def devLogTransferPort
				 Device.withTransaction{
					 Device device = Device.findById(deviceId)
					 devStbIp = device?.stbIp
					 devLogTransferPort = device?.logTransferPort					 
				 }
				 Script.withTransaction {
					 Script script = Script.findById(scriptId)
					 String filePath = ""
					 int cnt = 0
					 script?.primitiveTest?.module?.logFileNames?.each{ logfilename ->
						 
						 String logFileName  = logfilename.toString()
						 int lastIndex = logFileName.lastIndexOf('/')
						 int stringLength = logFileName.length()
						 String extractedFileName = logFileName.substring(lastIndex+1, stringLength)
						 
						 cnt++
						 if((logFileName) && !(logFileName.isEmpty())){
							 filePath = destinationCrashFile.replace("execId_logdata.txt", "${execId}_${execDeviceId}_${cnt}${extractedFileName}")
							 
							  String[] cmd = [
								  "python",
								  fileTransferPath,
								  devStbIp,
								  devLogTransferPort,
								  logFileName,
								  filePath
							  ]
													  
							 ScriptExecutor scriptExecutor = new ScriptExecutor()
							 def outputData = scriptExecutor.executeScript(cmd)
						 }				     
					 }
				  }
			 }	 
			 else{
	             String[] dataArray = dataFromSocket.split( COMMA_SEPERATOR )
	             if(dataArray){
	                 if(dataArray[0] && dataArray[1]){
	                     String stbName = dataArray[0]
	                     String stbIp = dataArray[1]
	                     Device device = Device.findByStbName(stbName.trim())
	                     if(device){
	                         Device.executeUpdate("update Device c set c.stbIp = :newStatus where c.id = :devId",[newStatus: stbIp,  devId: (device?.id)])                         
	                     }
	                 }
	             }  
			 }     
             server.close();
          }catch(IOException e)
          {
             e.printStackTrace()           
          }
          catch(Exception ex)
          {
             ex.printStackTrace()         
          }
       }
    }    
}
