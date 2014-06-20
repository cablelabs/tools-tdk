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

/**
 * Executor class for executing the script
 */
import static com.comcast.rdk.Constants.EXEC_EXITCODE_SUCCESS
import static com.comcast.rdk.Constants.NEW_LINE
import java.util.concurrent.Callable
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.FutureTask


class ScriptExecutor {
	
	String outputFileName = null;
	
	public ScriptExecutor(){
	}
	
	public ScriptExecutor(String outputFileName){
		this.outputFileName = outputFileName;
	}
    
    static ExecutorService executorService = Executors.newCachedThreadPool()
    
    /**
     * Execute the script
     * @param executionScript
     * @return
     * @author ajith
     */
    public String execute(final String executionScript, final int waittime) {
        Process process = Runtime.getRuntime().exec( executionScript )
		StringBuilder dataRead = new StringBuilder( "" )
        StreamReaderJob dataReader = new StreamReaderJob(process.getInputStream(),outputFileName,dataRead);
        StreamReaderJob errorReader = new StreamReaderJob(process.getErrorStream(),outputFileName,dataRead);
        
        FutureTask< String > dataReaderTask = new FutureTask< String > (dataReader);
        FutureTask< String > errorReaderTask = new FutureTask< String > (errorReader);
        executorService.execute(dataReaderTask);
        executorService.execute(errorReaderTask);
		if(waittime == 0){
			int exitCode = process.waitFor()
		}
		else{
			process.waitForOrKill(waittime*60000)
		}
		String outputData = null
		outputData = dataReaderTask.get()
		if(!outputData){
			outputData = errorReaderTask.get()
		}
		process.destroy()
	    return outputData
    }
	
	
	public String execute(final String executionScript) {
		Process process = Runtime.getRuntime().exec( executionScript )
		StreamReaderJob dataReader = new StreamReaderJob(process.getInputStream(),outputFileName);
		StreamReaderJob errorReader = new StreamReaderJob(process.getErrorStream(),outputFileName);
		
		FutureTask< String > dataReaderTask = new FutureTask< String > (dataReader);
		FutureTask< String > errorReaderTask = new FutureTask< String > (errorReader);
		executorService.execute(dataReaderTask);
		executorService.execute(errorReaderTask);
		int exitCode = process.waitFor()
		String outputData = null
		if(EXEC_EXITCODE_SUCCESS == exitCode) {
			outputData = dataReaderTask.get()
		}
		else{
			outputData = errorReaderTask.get()
		}
		process.destroy()
		log.info(" Script Executor Exit code :: "+exitCode)
		return outputData
	}
	
	
	/**
	 * Execute the script
	 * @param executionScript
	 * @return
	 */
	public String executeCommand(final String[] command, final Device deviceInstance) {

		Process process = Runtime.getRuntime().exec( command )
		StreamReaderJob dataReader = new StreamReaderJob(process.getInputStream())
		StreamReaderJob errorReader = new StreamReaderJob(process.getErrorStream())

		FutureTask< String > dataReaderTask = new FutureTask< String > (dataReader)
		FutureTask< String > errorReaderTask = new FutureTask< String > (errorReader)
		executorService.execute(dataReaderTask)
		executorService.execute(errorReaderTask)
		deviceInstance.uploadBinaryStatus = UploadBinaryStatus.INPROGRESS
		deviceInstance.save(flush:true)
		process.waitForOrKill(1200000) 				// 20 mins timeout
		String outputData = dataReaderTask.get()
		process.destroy()
		return outputData
	}

	
	/**
	 * Method to execute a script. 
	 * This method executes a particular command with specified arguments.
	 * @param command
	 * @return
	 */
	def executeScript(final String[] command) {
		
		Process process = Runtime.getRuntime().exec( command )
		StreamReaderJob dataReader = new StreamReaderJob(process.getInputStream())
		StreamReaderJob errorReader = new StreamReaderJob(process.getErrorStream())

		FutureTask< String > dataReaderTask = new FutureTask< String > (dataReader)
		FutureTask< String > errorReaderTask = new FutureTask< String > (errorReader)
		executorService.execute(dataReaderTask)
		executorService.execute(errorReaderTask)		
		process.waitFor()//OrKill(120000) 				// 2 mins timeout
		String outputData = dataReaderTask.get()
		String errorData = errorReaderTask.get()
		if(errorData && (errorData.length() > 0 )){
			//println "errorData :: "+errorData
		}
		process.destroy()
		return outputData
	}
	
	/**
	 * Method to execute a script.
	 * This method executes a particular command with specified arguments.
	 * @param command
	 * @return
	 */
	def executeScript(final String[] command, final int waittime) {
		
		Process process = Runtime.getRuntime().exec( command )
		StreamReaderJob dataReader = new StreamReaderJob(process.getInputStream())
		StreamReaderJob errorReader = new StreamReaderJob(process.getErrorStream())

		FutureTask< String > dataReaderTask = new FutureTask< String > (dataReader)
		FutureTask< String > errorReaderTask = new FutureTask< String > (errorReader)
		executorService.execute(dataReaderTask)
		executorService.execute(errorReaderTask)
		if(waittime == 0){
			int exitCode = process.waitFor()
		}
		else{
			process.waitForOrKill(waittime*60000)
		}
		String outputData = dataReaderTask.get()
		String errorData = errorReaderTask.get()
		if(errorData && (errorData.length() > 0 )){
			//println "errorData :: "+errorData
		}
		process.destroy()
		return outputData
	}
}


class StreamReaderJob implements Callable< String > {
    /**
     * Holds the input stream. Can be data/error.
     */
    InputStream inputStream = null
	String outputFileName = null
	String intialData = ""
	StringBuilder dataRead = new StringBuilder( "" )
    /**
     * Constructor that takes the input stream.
     * @param inputStream
     *      The input stream of data.
     */
    public StreamReaderJob(InputStream inputStream) {
        this.inputStream = inputStream
    }
	public StreamReaderJob(InputStream inputStream , String outputFileName) {
		this.inputStream = inputStream
		this.outputFileName = outputFileName;
	}
	public StreamReaderJob(InputStream inputStream , String outputFileName,StringBuilder dataRead) {
		this.inputStream = inputStream
		this.outputFileName = outputFileName;
		this.dataRead = dataRead
	}
	
    /**
     * This method will be called by the invoking thread.
     * Reads the data from the input stream and adds the content to a String buffer.
     * On the end of the stream, the string buffer is returned.
     * @return
     *      Data read from the stream.
     */
    @Override
    public String call() throws Exception {

        InputStreamReader inputStreamReader = new InputStreamReader(inputStream)
        BufferedReader bufferedReader = new BufferedReader(inputStreamReader)
        try {
            String data = ""
            while((data = bufferedReader.readLine()) != null) {
                dataRead.append(data)
                dataRead.append(NEW_LINE)
				if(outputFileName != null){
					writeToOutputFile(outputFileName, data + NEW_LINE)
				}
            }
        }
        catch ( IOException e ) {
            e.printStackTrace();
        }
        finally {
            try {
                bufferedReader?.close()
                inputStreamReader?.close()
                inputStream?.close()
            }
            catch (IOException e) {
                e.printStackTrace()
            }
        }
        return dataRead.toString()
    }
	
	public void writeToOutputFile(String fileName, String data){
		try{
			
			if(data == null || fileName == null){
				return
			}
			
			File opFile = new File(fileName);
			
			if(data.contains("SCRIPTEND#!@~")){
				data = data.replace("SCRIPTEND#!@~","")
			}
			
			if(data.contains(Constants.TDK_ERROR)){
				data = data.replace(Constants.TDK_ERROR,"")
			}
			
			
			String htmlData = ""
			data?.eachLine { line ->
				htmlData += (line + "<br/>" )
			}

			for(int i=0; i< 2; i++) {
				try {
					boolean append = true
					FileWriter fileWriter = new FileWriter(opFile, append)
					BufferedWriter buffWriter = new BufferedWriter(fileWriter)
					buffWriter.write(htmlData);
					buffWriter.flush()
					buffWriter.close()
					break;
				} catch(FileNotFoundException ex) {
					Thread.sleep(1000);
				}
			}
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	
	public void deleteOutputFile(String fileName){
		try{
			File opFile = new File(fileName);
			if(opFile.exists()){
				opFile.delete();
			}
		}catch(Exception e){
			e.printStackTrace();
		}
	}
}

