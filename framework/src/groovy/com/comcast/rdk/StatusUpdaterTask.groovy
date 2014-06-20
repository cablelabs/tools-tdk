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
 * Runnable task to update the device status of one device.
 *
 */
class StatusUpdaterTask implements Runnable {
	
	String[] cmd;
	Device device;
	def deviceStatusService
	def executescriptService
	def executionService
	def grailsApplication
	
	public StatusUpdaterTask(String[] cmd,Device device,def deviceStatusService,def executescriptService,def grailsApplication){
		this.cmd = cmd;
		this.device = device;
		this.deviceStatusService = deviceStatusService;
		this.executescriptService = executescriptService
		this.grailsApplication = grailsApplication
	}

	@Override
	public void run() {
		String outData = ""
		
		try {
			outData = new ScriptExecutor().executeScript(cmd,1)
		} catch (Exception e) {
			e.printStackTrace()
		}
		outData = outData.trim()
		if(outData){
			if(outData.equals(Status.FREE.toString())){
				String status = Status.FREE.toString()
				
				def executionList = Execution.findAllByExecutionStatusAndDevice("PAUSED",device.getStbName());
				if(executionList.size() > 0){
				executionList.each{
					Execution execution = it
					def execDevice = ExecutionDevice.findByStatusAndDeviceAndExecution("PAUSED",device.getStbName(),execution);
					boolean paused = false
						if(execDevice){
							
							synchronized (ExecutionController.lock) {
								if(ExecutionService.deviceAllocatedList.contains(device?.id)){
									status = "BUSY"
								}else{
									if(!ExecutionService.deviceAllocatedList.contains(device?.id)){
										ExecutionService.deviceAllocatedList.add(device?.id)
									}
								}
							}
							if(status.equals(Status.FREE.toString())){
							Thread.start {
								try{
									deviceStatusService.updateDeviceStatus(device,"BUSY")
								}
								catch(Exception e){
								}
							}
							try{
								paused = executescriptService.restartExecution(execDevice,grailsApplication)
							}finally{
								if(ExecutionService.deviceAllocatedList.contains(device?.id)){
									ExecutionService.deviceAllocatedList.remove(device?.id)
								}
							}
							}
						}
					if(!paused){
						RepeatPendingExecution rExecution = RepeatPendingExecution.findByDeviceNameAndStatus(device.getStbName(),"PENDING")
						if(rExecution){
						runCompleteRepeat(device)
						}
					}
				}
				}else{
					def executionList11 = Execution.findAllByExecutionStatusAndDevice(Constants.INPROGRESS_STATUS,device.getStbName());
					if(executionList.size() == 0 && executionList11.size() < 1){
						RepeatPendingExecution rExecution = RepeatPendingExecution.findByDeviceNameAndStatus(device.getStbName(),"PENDING")
						if(rExecution){
							runCompleteRepeat(device)
						}
					}
				}
			}
			callStatusUpdater(device,outData)
			
		}
	}
	
	def callStatusUpdater(device,outData) throws Exception{
		try{
			deviceStatusService.updateDeviceStatus(device,outData) 
		}
		catch(Exception e){
		}
	}
	
	
	
	/**
	 * Method to restart a complete repeat once device is free
	 * @param device
	 */
	private void runCompleteRepeat(def device){
		RepeatPendingExecution rExecution = RepeatPendingExecution.findByDeviceNameAndStatus(device.getStbName(),"PENDING")
		Execution execution = Execution.findByName(rExecution?.executionName)
		boolean paused = false
		try{
			if(execution != null && rExecution?.completeExecutionPending > 0){

				if(!ExecutionService.deviceAllocatedList.contains(device?.id)){
					ExecutionService.deviceAllocatedList.add(device?.id)
				}

				def th = Thread.start {
					try{
						deviceStatusService.updateDeviceStatus(device,"BUSY")
					}
					catch(Exception e){
					}
				}

				try{
					RepeatPendingExecution.withTransaction{
						RepeatPendingExecution rEx = RepeatPendingExecution.findById(rExecution?.id)
						rEx?.status = "IN-PROGRESS"
						rEx.save(flush:true)
					}

					int count = 0
					String exName= execution.name
					if(rExecution?.currentExecutionCount > 0){
						count = (rExecution?.currentExecutionCount)
						try {
							if(exName.contains("_")){
								exName = exName.substring(0,exName.lastIndexOf("_"));
							}
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
					int pendingExecutions = rExecution?.completeExecutionPending
					for(int i = 1 ; i <= pendingExecutions && !paused; i++){
						RepeatPendingExecution.withTransaction{
							rExecution = RepeatPendingExecution.findById(rExecution?.id)
						}
						try {
							String newExName = exName+"_"+(count+i)
							try {
								paused = executescriptService.triggerRepeatExecution(execution,newExName,grailsApplication,device?.getStbName())
							} catch (Exception e) {
								e.printStackTrace()
							}
							RepeatPendingExecution.withTransaction{
								RepeatPendingExecution rEx = RepeatPendingExecution.findById(rExecution?.id)
								rEx?.currentExecutionCount = (rExecution?.currentExecutionCount + 1)
								rEx?.completeExecutionPending = (rExecution?.completeExecutionPending - 1)
								rEx.save(flush:true)
							}
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
					saveRepeatExecutionStatus(paused, rExecution)
				}finally{
					if(ExecutionService.deviceAllocatedList.contains(device?.id)){
						ExecutionService.deviceAllocatedList.remove(device?.id)
					}
				}
			}else{
				if(rExecution?.completeExecutionPending == 0){
					saveRepeatExecutionStatus(false, rExecution)
				}
			}
		}finally{
			if(ExecutionService.deviceAllocatedList.contains(device?.id)){
				ExecutionService.deviceAllocatedList.remove(device?.id)
			}
		}
	}
	
	private void saveRepeatExecutionStatus(boolean paused , def rExecution){
		String status = ""
		if(!paused){
			status = "COMPLETED"
		}else{
			status = "PENDING"
		}
		
		RepeatPendingExecution.withTransaction{
			RepeatPendingExecution rEx = RepeatPendingExecution.findById(rExecution?.id)
			rEx?.status = status
			rEx.save(flush:true)
		}
	}

}
