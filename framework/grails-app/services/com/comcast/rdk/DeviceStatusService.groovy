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
import org.hibernate.StaleObjectStateException

import groovy.sql.Sql
import java.util.Map;

public class DeviceStatusService {
	static datasource = 'DEFAULT'
	def executionService
	def dataSource
	def grailsApplication
	def mocaDeviceService
	
	static transactional = false
	
	public static List deviceResetList = []

	/**
	 * Method to update the current status of device in DB.
	 * After device status updation, it will check for moca device availability.
	 * @param device
	 * @param outData
	 */
	public void updateDeviceStatus(final Device device, final String outData ) throws StaleObjectStateException  {
		def deviceStatus
		def deviceInstance
		def deviceId
		def deviceName = ""
		def boxtype
		Device.withTransaction { deviceStat ->
			deviceInstance = Device.findByStbName(device?.stbName)
			deviceId = deviceInstance?.id
			deviceName = deviceInstance?.stbName.toString()
			boxtype = deviceInstance?.boxType
		}
			if(deviceInstance){
				
				if(executionService.deviceAllocatedList.contains(deviceId)){
					deviceStatus = Status.BUSY
				}
				else{
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
				}				
				try {		
					def sql = new Sql(dataSource)					
					def status = sql.executeUpdate("update device set device_status = ? where stb_name = ? ",[deviceStatus.toString(),deviceName])

				} catch (Exception e) {			
				}				
				mocaDeviceService.updateMocaDevices(deviceInstance,boxtype)
			}
	}
	
	public void updateOnlyDeviceStatus(final Device device, final String outData ){
		String deviceStatus
		def deviceInstance
		def deviceId
		def deviceName
		Device.withTransaction {
			deviceInstance = Device.findByStbName(device?.stbName)
			deviceId = deviceInstance?.id
			deviceName = deviceInstance.stbName.toString()
		}
		if(deviceInstance){
			
			if(executionService.deviceAllocatedList.contains(deviceId)){
				deviceStatus = Status.BUSY
			}
			else{
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
			}

			try{	
				Device.withTransaction{
					Device dev = Device.findById(deviceId)
					dev?.deviceStatus = deviceStatus
					dev?.save(flush:true)
				}			
//				def sql = new Sql(dataSource)
//				def status = sql.executeUpdate("update device set device_status = ? where stb_name = ? ",[deviceStatus.toString(),deviceName])
			}catch(Exception e){
			}
		}
	}

	
	def resetIPRule(final Device device){
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
