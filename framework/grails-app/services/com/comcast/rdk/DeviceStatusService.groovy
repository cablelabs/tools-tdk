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
package com.comcast.rdk;

import static com.comcast.rdk.Constants.*

public class DeviceStatusService {
	def executionService
	

	/**
	 * Method to update the current status of device in DB.
	 * After device status updation, it will check for moca device availability.
	 * @param device
	 * @param outData
	 */
	public void updateDeviceStatus(final Device device, final String outData ){
		String deviceStatus
		def deviceInstance
		def deviceId
		Device.withTransaction {
		deviceInstance = Device.findByStbName(device?.stbName)
	//	deviceInstance = Device.findByStbName(device?.stbName,[lock:true])
		if(deviceInstance){
			deviceId = deviceInstance?.id
			if(outData.equals( Status.BUSY.toString() )){
				deviceStatus = Status.BUSY
			}
			else if(outData.equals( Status.FREE.toString() )){
				deviceStatus = Status.FREE
			}
			else if(outData.equals( Status.NOT_FOUND.toString() )){
				deviceStatus = Status.NOT_FOUND
			}
			else if(outData.equals( Status.HANG.toString() )){
				deviceStatus = Status.HANG
			}
			else{
				deviceStatus = Status.NOT_FOUND
			}
			try{
				deviceInstance.deviceStatus = deviceStatus
				deviceInstance.save(flush:true)

				updateMocaDevices(deviceInstance,deviceInstance.boxType)
			}catch(Exception e){
			}
		}
		}
	}


	/**
	 * Method to check moca device availability for a device.
	 * Will invoke Port forwading during  for Gateway devices.
	 * Port forwarding has 2 phases.
	 *	1) Get macId of connected devices.
	 *	2) Set routing rules for child devices.
	 *  Get devices will be called every 30 sec and if any new child device connected it will be saved in DB.
	 *  For every new devices, unique execution port, status port and log transfer port will be generated dynamically.
	 *  Routing will be called only once for a device with particular mac id.
	 *  
	 * @param device
	 * @param boxType
	 */
	public void updateMocaDevices(def device, def boxType ){

		def executionResult
		List existingDevices = []
		List newDevices = []
		List deletedDevices = []
		List macIdList = []

		int childStbPort
		int childStatusPort
		int childLogTransferPort
		int childAgentMonitorPort
		def macIdAppender
		List childDeviceList = []

		try{
			if(boxType?.type?.toLowerCase() == GATEWAY_BOX){

				macIdList.removeAll(macIdList) 
				executionResult =  executionService.executeGetDevices(device)   // execute callgetdevices.py

				macIdList = executionService.parseExecutionResult(executionResult)

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
						macIdAppender = macId.substring(macId.length() - 5, macId.length())
						if(!deviceObj){


							childStbPort = customStbPort +  randomVal
							childStatusPort = customStatusPort +  randomVal
							childLogTransferPort = customLogTransferPort +  randomVal
							childAgentMonitorPort = customAgentMonitorPort +  randomVal
							
							Device childDevice = new Device()
							childDevice.macId = macId
							childDevice.stbName = device.stbName+HYPHEN+BoxType.findByName(XI3_BOX).name+HYPHEN+macIdAppender
							childDevice.stbIp =device.stbIp
							childDevice.boxType = BoxType.findByName(XI3_BOX)
							childDevice.boxManufacturer = BoxManufacturer.findByName(DEFAULT_BOX_MANUFACTURER)
							childDevice.soCVendor = SoCVendor.findByName(DEFAULT_SOCVENDOR)
							childDevice.gatewayIp = device.stbIp
							childDevice.recorderId = device.recorderId

							childDevice?.stbPort = childStbPort
							childDevice?.statusPort = childStatusPort
							childDevice?.logTransferPort = childLogTransferPort
							childDevice?.agentMonitorPort = childAgentMonitorPort
							childDevice?.isChild = 1

							childDevice.save(flush:true)
							//devicegroupService.saveToDeviceGroup(childDevice)

							childDeviceList << childDevice

							executionService.executeSetRoute(device, childDevice)   //execute callsetroute.py
						}
						else{
							if(!(deviceObj.gatewayIp?.equals(device?.stbIp))){
								deviceObj.stbIp =device?.stbIp
								deviceObj.gatewayIp = device?.stbIp
								deviceObj.recorderId = device?.recorderId
								deviceObj.save(flush:true)
								executionService.executeSetRoute(device, deviceObj)
							}
							childDeviceList << deviceObj
						}
					}
					existingDevices = device.childDevices
					device.childDevices = childDeviceList
					// device.save(flush:true)
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
		catch(Exception e){
		}
	}
}
