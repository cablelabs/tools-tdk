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
		String outData =  new ScriptExecutor().executeScript(cmd)
		outData = outData.trim()
		if(outData){
			if(outData.equals(Status.FREE.toString())){
				def executionList = Execution.findAllByExecutionStatusAndDevice("PAUSED",device.getStbName());
				executionList.each{
					Execution execution = it
					def execDevice = ExecutionDevice.findByStatusAndDeviceAndExecution("PAUSED",device.getStbName(),execution);
					if(execDevice){
						executescriptService.restartExecution(execDevice,grailsApplication)
					}
				}
			}
			try{
				deviceStatusService.updateDeviceStatus(device,outData)
			}
			catch(Exception e){
			}
		}
	}

}
