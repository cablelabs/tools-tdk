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
 * A service class for DeviceGroup domain
 * @author sreejasuma
 */

class DevicegroupService {
	static datasource = 'DEFAULT'
    
    /**
     * Method to save the device to a DeviceGroup, according to the box chosen for execution
     * If the device group exists then add the device to that group.
     * Else create a Device group and add the device to the group.     
     * @param deviceInstance
     * @return
     */
    def saveToDeviceGroup(final Device deviceInstance){
        String boxType = deviceInstance.boxType.name
        def deviceGrpInstance = DeviceGroup.findByName(boxType)
        if(!deviceGrpInstance){   
            deviceGrpInstance = new DeviceGroup()     
            deviceGrpInstance.name = boxType
        }        
            
        deviceGrpInstance?.addToDevices(deviceInstance)
        deviceGrpInstance?.save(flush:true)

    }
    
    /**
     * Checking the status of the device or the device is present in a 
     * device group which is selected to execute, 
     * and if device is free, delete device from the device group to make the
     * fresh update of device. 
     * @author sreejasuma
     */
   
    public boolean checkDeviceStatus(final Device device){
        
        boolean deviceInUse = false
        boolean isAllocatedDeviceGrp = false
        if(device.deviceStatus.equals( Status.BUSY)){
            deviceInUse = true
        }
        else{
            /**
             * Selecting deviceGroups based on whether selected device exists
             * in the device group's and status of the DeviceGroup is Busy.
             * In this case the device cannot be deleted.
             */
            def deviceAllocated = DeviceGroup.where {
                devices { id == device.id } && status == Status.BUSY
            }
            deviceAllocated?.each{
                isAllocatedDeviceGrp = true
                return true
            }
            if(isAllocatedDeviceGrp){
                deviceInUse = true
            }
            else{
                /**
                 * Selecting deviceGroups where the given device is present
                 * And removing the device from the devicegroup
                 */
                def deviceGroups = DeviceGroup.where {
                    devices { id == device.id }
                }
                def deviceInstance
                deviceGroups?.each{ deviceGrp ->
                    deviceInstance = deviceGrp.devices.find { it.id == device.id }
                    if(deviceInstance){
                        deviceGrp?.removeFromDevices(deviceInstance)
                    }
                }
            }
        }
        return deviceInUse
    }
	
	/**
	 * Returns name of selected boxType 
	 * @param boxTypeId
	 * @return
	 */
	public String  getBoxType(boxTypeId){

		BoxType boxType = BoxType.findById(boxTypeId)
		String boxName = boxType.name
		return boxName
	}

	/**
	 * Method to remove the  device reference from execution result objects while deleting the device
	 */
	def updateExecDeviceReference(def device){

		try {
			def exResultList = ExecutionResult.findAllByExecDevice(device)
			exResultList.each {exResult ->
				ExecutionResult.withTransaction{ tran ->
					try {
						ExecutionResult.executeUpdate("update ExecutionResult c set c.execDevice = null  where c.id = :execResultId",
								[execResultId: exResult?.id?.toLong()])
						
					} catch (Exception e) {
						e.printStackTrace()
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
}
