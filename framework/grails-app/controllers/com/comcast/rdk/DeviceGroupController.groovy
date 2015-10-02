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
 * A class that handles the device creation and device group creation
 * @author sreejasuma
 */
import static com.comcast.rdk.Constants.*
import grails.converters.JSON
import java.sql.Timestamp
import java.util.concurrent.ExecutorService

import org.apache.shiro.SecurityUtils;
import org.apache.shiro.subject.Subject
import org.springframework.dao.DataIntegrityViolationException

import com.google.gson.JsonArray
import com.google.gson.JsonObject;

import java.util.concurrent.Executors


class DeviceGroupController {

    static allowedMethods = [save: "POST", update: "POST", delete: "POST", updateDevice : "POST"]
    /**
     * Injecting devicegroupService
     */
    def devicegroupService
	def utilityService
	
	private static final String DEVICESTREAM_QUERY = "delete DeviceStream d where d.device = :instance1"
	private static final String DEVICERADIOSTREAM_QUERY = "delete DeviceRadioStream d where d.device = :instance1"
	private static final String GATEWAY = "Gateway"
	
    static ExecutorService executorService = Executors.newCachedThreadPool()
    def executionService
	def grailsApplication
	
	def index(){
		redirect(action: "list")
	}

    /**
     * Method to list the device groups.
     * When list method is called as ajax from devicegrp_resolver.js with the 
     * params?.streamtable value only the streamlist page will be rendered.
     */    
    def list = {	
		/**
		 * Invoked from 
		 */
        if(params?.streamtable) {
            def result = [url: getApplicationUrl(), streamingDetailsInstanceList: StreamingDetails.list(),radioStreamingDetails : RadioStreamingDetails.findAll(), streamingDetailsInstanceTotal: StreamingDetails.count(), streamingDetailsInstanceTotal: RadioStreamingDetails.count()]
			 render view:"streamlist", model:result
            return
        }		
		def groupsInstance = utilityService.getGroup()
		def deviceInstanceList = Device.findAllByGroupsOrGroupsIsNull(groupsInstance,[order: 'asc', sort: 'stbName'])
		def deviceGrpInstanceList = DeviceGroup.findAllByGroupsOrGroupsIsNull(groupsInstance)
        [url: getApplicationUrl(), deviceGroupsInstance : params?.deviceGroupsInstance, deviceInstanceList : deviceInstanceList, deviceInstanceTotal : deviceInstanceList.size(), deviceGroupsInstanceList : deviceGrpInstanceList, deviceGroupsInstanceTotal : deviceGrpInstanceList.size(), deviceId: params.deviceId, deviceGroupId: params.deviceGroupId]
    }

    /**
     * Method to create a device group.
     */
    def create() {
        [deviceGroupsInstance: new DeviceGroup(params)]
    }

    /**
     * Method to save a device group.
     */
    def save() {
        def deviceGroupsInstance = new DeviceGroup(params)
        if(DeviceGroup.findByName(params?.name)){
            flash.message = flash.message = message(code: 'devicegrp.already.exists') 
            redirect(action: "list")
            return
        }
		deviceGroupsInstance.groups = utilityService.getGroup()
		if(params?.devices != null)
		{
        if (!deviceGroupsInstance.save(flush: true)) {
            log.info("Device Group Not Created "+deviceGroupsInstance?.name)
            log.error( deviceGroupsInstance.errors)
            redirect(action: "list")
            return
        }
        log.info("Device Group Saved "+deviceGroupsInstance?.name)
        flash.message = message(code: 'default.created.message', args: [
            message(code: 'deviceGroups.label', default: 'DeviceGroups'),
            deviceGroupsInstance.name
        ])
		}
		else
		{
			/*flash.message =message(code: 'default.not.created.message', args: [
            message(code: 'deviceGroups.label', default: 'DeviceGroups'),
            deviceGroupsInstance.name
        ])*/
			flash.message = "Please select the devices to save DeviceGroup"
		}
		
        redirect(action: "list")
    }

    /**
     * Method to show a device group.
     */
    def show(Long id) {
        def deviceGroupsInstance = DeviceGroup.get(id)
        if (!deviceGroupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                id
            ])
            redirect(action: "list")
            return
        }
        [deviceGroupsInstance: deviceGroupsInstance]
    }

    /**
     * Method to edit a device group.
     */
    def edit(Long id) {
        def deviceGroupsInstance = DeviceGroup.get(id)
        if (!deviceGroupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                id
            ])
            redirect(action: "list")
            return
        }
        [deviceGroupsInstance: deviceGroupsInstance]
    }

    /**
     * Method to update a device group.
     */
    def update(Long id, Long version) {
        def deviceGroupsInstance = DeviceGroup.get(id)

        if (!deviceGroupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                id
            ])
            redirect(action: "list")
            return
        }
        if (version != null) {
            if (deviceGroupsInstance.version > version) {
                deviceGroupsInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                        [
                            message(code: 'deviceGroups.label', default: 'DeviceGroup')] as Object[],
                        "Another user has updated this DeviceGroups while you were editing")
                redirect(action: "list")
                return
            }
        }
        deviceGroupsInstance.name = params?.name
        deviceGroupsInstance.devices = []
        if (!deviceGroupsInstance.save(flush: true)) {
            redirect(action: "list", params : [deviceGroupsInstance: deviceGroupsInstance])
            return
        }
        else{
            log.info("Device Group Updated "+deviceGroupsInstance?.name)
            def device
            if((params?.devices) instanceof String ){
                device = Device.findByStbName(params?.devices)
                deviceGroupsInstance.addToDevices(device)
            }
            else{
                params.devices.each{ name ->
                    device = Device.findByStbName(name)
                    deviceGroupsInstance.addToDevices(device)
                }
            }
        }

        flash.message = message(code: 'default.updated.message', args: [
            message(code: 'deviceGroups.label', default: 'DeviceGroup'),
            deviceGroupsInstance.name
        ])
		redirect(action: "list", params: [deviceGroupId: params.id])
    }

	/**
	 * Method to delete a device group
	 * @return
	 */
    def delete() {
        def deviceGroupsInstance = DeviceGroup.get(params?.id)
        if (!deviceGroupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                params?.id
            ])
            redirect(action: "list")
            return
        }

        try {
            deviceGroupsInstance.delete(flush: true)
            flash.message = message(code: 'default.deleted.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                deviceGroupsInstance?.name
            ])
            redirect(action: "list")
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                deviceGroupsInstance?.name
            ])
            redirect(action: "list")
        }
    }

	/**
	 * Method to delete a device group
	 * @return
	 */
    def deleteDeviceGrp() {

        Long id = params.id as Long
        def deviceGroupsInstance = DeviceGroup.get(id)
        if (!deviceGroupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                deviceGroupsInstance?.id
            ])
            redirect(action: "list")
            return
        }
        try {
            deviceGroupsInstance.delete(flush: true)
            flash.message = message(code: 'default.deleted.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                deviceGroupsInstance?.name
            ])
            render("success")
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                deviceGroupsInstance?.name
            ])
            redirect(action: "list")
        }
    }

    /**
     * Create a new device
     * @return
     */
    def createDevice() {
        def devices = Device.where { boxType { type == GATEWAY } }
        [url : getApplicationUrl() ,deviceInstance: new Device(params), gateways : devices, editPage : false]
    }

    /**
     * Save a new device
     * @return
     */
    def saveDevice() {
        if(Device.findByStbName(params?.stbName)){
            flash.message = message(code: 'stbname.already.exists')
			render(flash.message)
            return
        }
		
		def stbIps = Device.findAllByStbIpAndIsChild(params?.stbIp, 0)
		
		if(stbIps){
			flash.message = message(code: 'stbip.already.exists')
			render(flash.message)
			return
		}
		

		/*if(Device.findByMacId(params?.macId)){
			flash.message = "Mac Id already in use. Please use a different Name."
			render("Mac Id already in use. Please use a different Name.")
			return
		}*/
		
		BoxType boxType = BoxType.findById(params?.boxType?.id)
		
		String newBoxType = boxType?.type?.toLowerCase()
		
		if (newBoxType.equals( BOXTYPE_GATEWAY ) || newBoxType.equals( BOXTYPE_STANDALONE_CLIENT )){
			String recId =  params?.recorderId
			if(recId?.trim()?.length() ==  0 ){
				flash.message = "Recorder id should not be blank"
				render(flash.message)
			    return
			}
		}
        
        /**
         * Check whether streams are present
         * and there is no duplicate OcapIds
         */
		if(newBoxType.equals( BOXTYPE_GATEWAY ) || newBoxType.equals(BOXTYPE_STANDALONE_CLIENT))
		{
        if((params?.streamid)){
			
			if(checkDuplicateOcapId(params?.ocapId)){
                flash.message = message(code: 'duplicate.ocap.id')
				render(flash.message)
                return
            }
        }
		}
		def deviceInstance = new Device(params)
		deviceInstance.groups = utilityService.getGroup()
        if (deviceInstance.save(flush: true)) {
            devicegroupService.saveToDeviceGroup(deviceInstance)
            saveDeviceStream(params?.streamid, params?.ocapId, deviceInstance)
        }
        else{
            flash.message = message(code: 'default.not.created.message', args: [
            message(code: 'device.label', default: 'Device')])			
			render(flash.message)
            return
        }

      flash.message = message(code: 'default.created.message', args: [
            message(code: 'device.label', default: 'Device'),
            deviceInstance.stbName
        ])
		render(message(code: 'default.created.message', args: [
            message(code: 'device.label', default: 'Device'),
            deviceInstance.stbName
        ]))
		
    }

    /**
     * Edit device
     * @return
     */
    def editDevice(Long id, final String flag) {
        def devices = Device.where { boxType { type == GATEWAY } }

        def deviceInstance = Device.get(id)
        if (!deviceInstance) {           
            return
        }
		def blankList = []
        def deviceStream = DeviceStream.findAllByDevice(deviceInstance)
		def radiodeviceStream = DeviceRadioStream.findAllByDevice(deviceInstance)
		boolean showBlankRadio = (radiodeviceStream ==null || radiodeviceStream?.size() == 0)
		if(showBlankRadio){
			def all = RadioStreamingDetails.findAll()
			all.each {
				blankList.add(it)
			}
		}
        [url : getApplicationUrl(),deviceInstance: deviceInstance, flag : flag, showBlankRadio:showBlankRadio,blankList:blankList,gateways : devices, deviceStreams : deviceStream,radiodeviceStreams:radiodeviceStream, editPage : true, uploadBinaryStatus: deviceInstance.uploadBinaryStatus, id: id]
    }

    /**
     * Update device
     * @return
     */
    def updateDevice(Long id, Long version) {
		
        def deviceInstance = Device.get(id)

        if (!deviceInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'device.label', default: 'Device'),
                id
            ])
            redirect(action: "list")
            return
        }

        if (version != null) {
            if (deviceInstance.version > version) {
                deviceInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                        [
                            message(code: 'device.label', default: 'Device')] as Object[],
                        "Another user has updated this Device while you were editing")
				redirect(action: "list")
                return
            }
        }
		
		
		
		
        boolean deviceInUse = devicegroupService.checkDeviceStatus(deviceInstance)
        if(deviceInUse){
			flash.message = message(code: 'device.not.update', args: [deviceInstance.stbIp])
            redirect(action: "list")
            return
        }
        else{
			
			String currentBoxType = deviceInstance?.boxType?.type?.toLowerCase()
			
			BoxType boxType = BoxType.findById(params?.boxType?.id)
			
			String newBoxType = boxType?.type?.toLowerCase()
		   String recId=""
			if (newBoxType.equals( BOXTYPE_GATEWAY ) || newBoxType.equals(BOXTYPE_STANDALONE_CLIENT)){
				if(currentBoxType.equals( BOXTYPE_GATEWAY) || currentBoxType.equals( BOXTYPE_STANDALONE_CLIENT)){
					recId =  params?.recorderIdedit
				}else if(currentBoxType.equals(BOXTYPE_CLIENT) && newBoxType.equals( BOXTYPE_GATEWAY ) ){
				recId =  params?.recorderIdedit
				}else{
					recId = ""
				}
				if(recId?.trim()?.length() ==  0 ){
					flash.message = "Recorder id should not be blank"
					redirect(action: "list", params: [deviceId: params.id])
					return
				}
			}
			

            deviceInstance.properties = params

            if(currentBoxType.equals( BOXTYPE_CLIENT )){
                if(newBoxType.equals( BOXTYPE_CLIENT )){
                    deviceInstance.gatewayIp = params?.gatewayIp
                    deviceInstance.recorderId = ""
                    DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
					DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
					
                }
                else{
                    deviceInstance.gatewayIp = ""
                    deviceInstance.recorderId = params?.recorderIdedit
                }
            }
            else{
                if(currentBoxType.equals( BOXTYPE_GATEWAY ) || currentBoxType.equals( BOXTYPE_STANDALONE_CLIENT )){
                    if(newBoxType.equals( BOXTYPE_CLIENT )){
                        deviceInstance.gatewayIp = params?.gatewayIpedit
                        deviceInstance.recorderId = ""
                        DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
						DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
                    }else  if(currentBoxType.equals( BOXTYPE_STANDALONE_CLIENT ) && newBoxType.equals( BOXTYPE_STANDALONE_CLIENT )){
                        deviceInstance.gatewayIp = params?.gatewayIp
						deviceInstance.recorderId = params?.recorderIdedit
                    }
                    else{
                        deviceInstance.gatewayIp = ""
                        deviceInstance.recorderId = params?.recorderIdedit
                    }
                }
            }
			
			
            if (!deviceInstance.save(flush: true)) {
                devicegroupService.saveToDeviceGroup(deviceInstance)
                redirect(action:"list")
                return
            }
           
           DeviceStream deviceStream

            if(currentBoxType.equals( BOXTYPE_CLIENT )){
                if(newBoxType.equals( BOXTYPE_GATEWAY) || newBoxType.equals( BOXTYPE_STANDALONE_CLIENT )){
					/**
					 * Check whether streams are present
					 * and there is no duplicate OcapIds
					 */
					if((params?.streamid)){
						
						if(checkDuplicateOcapId(params?.ocapId)){
							flash.message = message(code: 'duplicate.ocap.id')
							redirect(action:"list")
							return
						}
					}
					
                    saveDeviceStream(params?.streamid, params?.ocapId, deviceInstance)        
                }
            }
            else{    
                if(deviceInstance.boxType.type.toLowerCase().equals( BOXTYPE_GATEWAY ) || deviceInstance.boxType.type.toLowerCase().equals( BOXTYPE_STANDALONE_CLIENT )  ){
						/**
					 * Check whether streams are present
					 * and there is no duplicate OcapIds
					 */
					if((params?.streamid)){
						
						if(checkDuplicateOcapId(params?.ocapId)){
							flash.message = message(code: 'duplicate.ocap.id')
							redirect(action:"list")
							return
						}
					}
					saveDeviceStream(params?.streamid, params?.ocapId, deviceInstance)
                }
            }

            devicegroupService.saveToDeviceGroup(deviceInstance)
            flash.message = message(code: 'default.updated.message', args: [
                message(code: 'device.label', default: 'Device'),
                deviceInstance.stbName
            ])
        }

		redirect(action: "list", params: [deviceId: params.id])
    }
	
	/**
	 * Check for duplicate ocapid's
	 * @param ocapIdList
	 * @return
	 */
	def boolean checkDuplicateOcapId(def ocapIdList){
		boolean isDuplicate = false
		int ocapIdSize = ocapIdList.size()
		Set setOcapId =  ocapIdList
		int setSize = setOcapId.size()
		if(setSize < ocapIdSize){
			isDuplicate = true
		}
		return isDuplicate
	}
	
	def boolean validateOcapIds(def streams, def ocapIdList){
		boolean valid = true
		int streamSize = StreamingDetails?.list().size()
		streamSize += RadioStreamingDetails?.list().size()
		if(streams?.size() == streamSize){
			int ocapIdSize = streams.size()
			Set setOcapId =  streams
			int setSize = setOcapId.size()
			if(setSize < ocapIdSize){
				valid = false
			}else{
				valid =  true
			}
		}else{
			valid = false
		}
		return valid
	}

    /**
     * Save device specific stream details
     * @return
     */
    def saveDeviceStream(final def streamIdList, final def ocapIdList, final Device deviceInstance){
		def deviceStreamList = DeviceStream.findAllByDevice(deviceInstance)		
		if(deviceStreamList?.size() > 0){
			DeviceStream.executeUpdate("delete DeviceStream d where d.device = :instance1",[instance1:deviceInstance])
		}
		
		def deviceRadioStreamList = DeviceRadioStream.findAllByDevice(deviceInstance)
		if(deviceRadioStreamList?.size() > 0){
			DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
		}
				
        DeviceStream deviceStream
        StreamingDetails streamingDetails

		for(int i = 0; i < streamIdList?.size() ; i++){

			def streamIdListIToString = streamIdList[i].toString()
			if(streamIdListIToString.startsWith("R")){
				def rStreamingDetails = RadioStreamingDetails.findByStreamId(streamIdListIToString)
				def rDeviceStream = new DeviceRadioStream()
				rDeviceStream.device = deviceInstance
				rDeviceStream.stream = rStreamingDetails
				rDeviceStream.ocapId = ocapIdList[i]
				if(!(rDeviceStream.save(flush:true))){
				}
			}else{
				streamingDetails = StreamingDetails.findByStreamId(streamIdListIToString)
				deviceStream = new DeviceStream()
				deviceStream.device = deviceInstance
				deviceStream.stream = streamingDetails
				deviceStream.ocapId = ocapIdList[i]
				if(!(deviceStream.save(flush:true))){
				}
			}
		}
    }
	
    /**
     * Delete device
     * @return
     */
	def deviceDelete(Long id) {
		List devicesTobeDeleted = []

		def deviceInstance = Device.get(id)
		if (!deviceInstance) {

			redirect(action: "list")
			return
		}
		boolean deviceInUse = devicegroupService.checkDeviceStatus(deviceInstance)
		if(deviceInUse){
			flash.message = message(code: 'device.not.update', args: [deviceInstance.stbIp])
			redirect(action: "list")
		}
		else{
			try {

				def deviceDetailsList = DeviceDetails.findAllByDevice(deviceInstance)

				if(deviceDetailsList?.size() > 0){
					DeviceDetails.executeUpdate("delete DeviceDetails d where d.device = :instance1",[instance1:deviceInstance])
				}

				deviceInstance.childDevices.each { childDevice ->
					devicesTobeDeleted << childDevice?.id
				}

				DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
				def list1 = DeviceRadioStream.findAllByDevice(deviceInstance)
				if(list1?.size()>0){
					DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
				}
				devicegroupService.updateExecDeviceReference(deviceInstance)
				//DeviceGroup.executeUpdate("delete DeviceGroup d where d.device = :instance1",[instance1:deviceInstance])

				if(deviceInstance?.isChild == 1){
					try {
						def devices = Device.findAll()
						devices?.each{ device ->
							def devInstance = device.childDevices.find { it.id == deviceInstance.id }
							if(devInstance){
								Device.withTransaction {
									Device parentDevice = Device.findById(device?.id)
									parentDevice.removeFromChildDevices(deviceInstance)
								}
							}
						}
					} catch (Exception e) {
						e.printStackTrace()
					}

				}

				try {
					if(!deviceInstance.delete(flush: true)){
							Device.withTransaction {
								Device dev = Device.findById(deviceInstance?.id)
								if(dev){
									dev?.delete(flush: true)
								}
							}
					}
				} catch (Exception e) {
					Device.withTransaction {
						Device dev = Device.findById(deviceInstance?.id)
						if(dev){
							dev?.delete(flush: true)
						}
					}
				}
				devicesTobeDeleted.each { childDeviceId ->

					Device childDevice = Device.findById(childDeviceId)
					devicegroupService.updateExecDeviceReference(childDevice)

					try {
						def status
						Device.withTransaction {
							status = childDevice.delete(flush: true)
						}

						if(!status){
								Device.withTransaction {
									Device dev = Device.findById(childDevice?.id)
									if(dev){
										dev?.delete(flush: true)
									}
								}
						}
					} catch (Exception e) {
						Device.withTransaction {
							Device dev = Device.findById(childDevice?.id)
							if(dev){
								dev?.delete(flush: true)
							}
						}
					}
				}

				flash.message = message(code: 'default.deleted.message', args: [
					message(code: 'device.label', default: 'Device'),
					deviceInstance.stbName
				])
				redirect(action: "list")
			}
			catch (DataIntegrityViolationException e) {
				flash.message = message(code: 'default.not.deleted.message', args: [
					message(code: 'device.label', default: 'Device'),
					deviceInstance.stbName
				])
				redirect(action: "list")
			}
		}
	}
	def deleteDeviceWithName(final String device1)
	{
		def deviceName=Device?.findByStbName(device1)
		try
			{
				def deviceList = Device.list()
				deviceList?.each{ device ->
					if(device1 == device)
					{
					
					}
					else
					{
						def deviceList1 = DeviceGroup.list()
						deviceList1.each{device12 ->
							
						}
					}				
					
				}
			
			}
			catch(Exception e)
			{
					e.printStackTrace()
			}
		
		render "deleteDevice"
		
	}
	

    /**
     * Delete device
     * @return
     */
    def deleteDevice() {
        Long id = params.id as Long
        def deviceInstance = Device.get(id)
		List devicesTobeDeleted = []

        boolean deviceInUse = devicegroupService.checkDeviceStatus(deviceInstance)
        if(deviceInUse){
			flash.message = message(code: 'device.not.update', args: [deviceInstance.stbIp])
            render(flash.message)
        }
        else{
			try {
				
				def deviceDetailsList = DeviceDetails.findAllByDevice(deviceInstance)
				
				if(deviceDetailsList?.size() > 0){
					DeviceDetails.executeUpdate("delete DeviceDetails d where d.device = :instance1",[instance1:deviceInstance])
				}
				

				deviceInstance.childDevices.each { childDevice -> devicesTobeDeleted << childDevice?.id }
				

				DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
				DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
				devicegroupService.updateExecDeviceReference(deviceInstance)
				
				if(deviceInstance.isChild == 1){
					try {
						def devices = Device.findAll()
					devices?.each{ device ->
						def devInstance = device.childDevices.find { it.id == deviceInstance.id }
						if(devInstance){
							Device.withTransaction {
								Device parentDevice = Device.findById(device?.id)
								parentDevice.removeFromChildDevices(deviceInstance)
							}
						}
					}
					} catch (Exception e) {
						e.printStackTrace()
					}
					
				}
				try {
					if(!deviceInstance.delete(flush: true)){
							Device.withTransaction {
								Device dev = Device.findById(deviceInstance?.id)
								if(dev){
										if(!dev?.delete(flush: true)){
											
										}
								}
							}
					}
				} catch (Exception e) {

						Device.withTransaction {
							Device dev = Device.findById(deviceInstance?.id)
							if(dev){
								if(!dev?.delete(flush: true)){

								}
							}
						}

				}
					devicesTobeDeleted.each { childDeviceId ->

						Device childDevice = Device.findById(childDeviceId)
						devicegroupService.updateExecDeviceReference(childDevice)

						try {
							def status
							Device.withTransaction {
								status = childDevice.delete(flush: true)
							}
							if(!status){
									Device.withTransaction {
										Device dev = Device.findById(childDevice?.id)
										if(dev){
											dev?.delete(flush: true)
										}
									}
							}
						} catch (Exception e) {
								Device.withTransaction {
									Device dev = Device.findById(childDevice?.id)
									if(dev){
										dev?.delete(flush: true)
									}
								}
						}
					}

				flash.message = message(code: 'default.deleted.message', args: [
					message(code: 'device.label', default: 'Device'),
					deviceInstance.stbName
				])
				render("success")
			}
            catch (DataIntegrityViolationException e) {
                flash.message = message(code: 'default.not.deleted.message', args: [
                    message(code: 'device.label', default: 'Device'),
                    deviceInstance.stbName
                ])
                render("Exception")
            }
        } 
    }

    /**
     * Method to get the current url and to create
     * new url upto the application name
     * @return
     */
    def String getApplicationUrl(){
        String currenturl = request.getRequestURL().toString();
        String[] urlArray = currenturl.split( URL_SEPERATOR );
        String url = urlArray[INDEX_ZERO] + DOUBLE_FWD_SLASH + urlArray[INDEX_TWO] + URL_SEPERATOR + urlArray[INDEX_THREE]
        return url
    }
    
    /**
     * Get the type of box from the box selected
     * @return
     */
    def getBoxType(){
        List boxTypes = []
        BoxType boxType = BoxType.findById(params?.id)
        boxTypes.add( boxType?.type?.toLowerCase()?.trim() )
        render boxTypes as JSON
    }

	/**
	 * Method to upload binary files to box.
	 * Invoked by an ajax call.
	 * Executes expect script with required parameters.
	 *  
	 * @return
	 */
	def uploadBinary(){

		String boxIp = params?.boxIp
		String username = params?.username
		String password = params?.password
		String systemPath = params?.systemPath
		String systemIP = params?.systemIP
		String boxpath = params?.boxpath

		List uploadResult = uploadBinaries(boxIp, username, password, systemPath, systemIP, boxpath)
		render uploadResult as JSON
	}

	
	def uploadBinaries(final String boxIp, final String username, final String password, final String systemPath,
		final String systemIP, final String boxpath){
		
		String outputData = null
		List uploadResult = []
		String EXPECT_COMMAND = KEY_EXPECT
		String  absolutePath
		
		def device = Device.findByStbIp(boxIp)
		String boxType = device?.boxType?.name
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//uploadbinary.exp").file
		absolutePath = layoutFolder.absolutePath
		try {

			String[] cmd = [
				EXPECT_COMMAND,
				absolutePath,
				boxType,
				boxIp,
				systemIP,
				username,
				password,
				systemPath,
				boxpath
			]

			Device deviceInstance = Device.findByStbIp(boxIp);

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			outputData = scriptExecutor.executeCommand(cmd, deviceInstance)
			uploadResult = Arrays.asList(outputData.split("\\r?\\n"))

			if(uploadResult.contains(KEY_BINARYTRANSFER)){
				deviceInstance.uploadBinaryStatus = UploadBinaryStatus.SUCCESS
			}
			else{
				deviceInstance.uploadBinaryStatus = UploadBinaryStatus.FAILURE
			}

			return uploadResult
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}
	
	
	def uploadAgentBinaries( final String systemIP, final String systemPath, final String username, final String password, 
		final String boxIp, final String boxpath){
		List uploadResult = uploadBinaries(boxIp, username, password, systemPath, systemIP, boxpath)
		List resultList = []
		def cnt = 0
		if(uploadResult){
			cnt = uploadResult?.size()
			resultList = uploadResult[cnt--]
		}
		render resultList as JSON		
	}
	
	
	/**
	 * Method to check whether device with same IP address exist or not. If yes returns the id of device
	 * @return
	 */
	def fetchDevice(){

		List deviceInstanceList = []
		Device deviceInstance = Device.findByStbName(params.stbName)
		if(deviceInstance){
			deviceInstanceList.add(deviceInstance.id)
		}
		render deviceInstanceList as JSON
	}
	
	/** REST method to retrieve the device info
	 * @param boxType
	 * @return
	 */
	def getDeviceList(String boxType){
		JsonObject deviceJson = new JsonObject()
		try {
			JsonArray devArray = new JsonArray()
			def devList
			BoxType bb
			if(boxType){
				bb = BoxType.findByName(boxType)
				if(bb){
					devList = Device.findByBoxType(bb)
				}
			}else{
				devList = Device.list()
			}

			if(boxType && !bb){
				deviceJson.addProperty("status", "failure")
				deviceJson.addProperty("remarks", "no box type found with name "+boxType)
			}else{
				if(devList){
					devList?.each{ dev ->
						JsonObject device = new JsonObject()
						device.addProperty("name", dev?.stbName)
						device.addProperty("boxtype", dev?.boxType?.name)
						if(dev?.boxType?.type?.equals("Client")){
							if(dev?.isChild == 1){
								device.addProperty("macid", dev?.macId)
								device.addProperty("mocachild", "true")
							}else{
								device.addProperty("ip", dev?.stbIp)
								device.addProperty("mocachild", "false")
							}
							device.addProperty("gateway", dev?.gatewayIp)
						}else{
							device.addProperty("ip", dev?.stbIp)
						}
						devArray.add(device)
					}
				}
				deviceJson.add("devices",devArray)
			}
		} catch (Exception e) {
			println " Error getDeviceList "+e.getMessage()
			e.printStackTrace()
		}
		render deviceJson
	}
	
	/**
	 * REST API used to the delete device
	 * @param deviceName
	 * @return
	 */
	
	def deleteDeviceMethod(final String deviceName){
		JsonObject deviceObj = new JsonObject()
		try{
			Subject currentUser = SecurityUtils.getSubject()
			if(currentUser?.hasRole('ADMIN')){
				Device dev1 = Device.findByStbName(deviceName)
				if(dev1){
					def deviceInstance = dev1?.id

					boolean deviceInUse = devicegroupService.checkDeviceStatus(dev1)
					if(deviceInUse){
						deviceObj?.addProperty("STATUS","FAILURE ")
						deviceObj?.addProperty("Remarks", "Device is busy, unable to delete")
					}
					else{
						if(deleteDeviceObject(dev1)){
							deviceObj?.addProperty("status","SUCCESS")
							deviceObj?.addProperty("remarks", "successfully deleted the device ")
						}else{
							deviceObj?.addProperty("status","FAILURE")
							deviceObj?.addProperty("remarks", "failed to delete device")
						}
					}
				}else{
					deviceObj?.addProperty("status","FAILURE")
					deviceObj?.addProperty("remarks", "no device found with name "+deviceName)
				}
			}else{
				deviceObj?.addProperty("status", "FAILURE")
				if(currentUser?.principal){
					deviceObj?.addProperty("remarks","current user ${currentUser?.principal} don't have permission to delete device" )
				}else{
					deviceObj?.addProperty("remarks","login as admin user to perform this operation" )
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}
		render deviceObj
	}
	
	def deleteDeviceObject(Device deviceInstance){
		try {
			List devicesTobeDeleted = []
			def deviceDetailsList = DeviceDetails.findAllByDevice(deviceInstance)
			if(deviceDetailsList?.size() > 0){
				DeviceDetails.executeUpdate("delete DeviceDetails d where d.device = :instance1",[instance1:deviceInstance])
			}
			deviceInstance?.childDevices?.each { childDevice -> devicesTobeDeleted << childDevice?.id }
			DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
			DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
			devicegroupService.updateExecDeviceReference(deviceInstance)

			if(deviceInstance.isChild == 1){
				try {
					def devices = Device.findAll()
					devices?.each{ device ->
						def devInstance = device.childDevices.find { it.id == deviceInstance }
						if(devInstance){
							Device.withTransaction {
								Device parentDevice = Device.findById(device?.id)
								parentDevice.removeFromChildDevices(deviceInstance)
							}
						}
					}
				} catch (Exception e) {
					e.printStackTrace()
				}

			}
			try {
				if(!deviceInstance.delete(flush: true)){
					Device.withTransaction {
						Device dev = Device.findById(deviceInstance?.id)
						if(dev){
							if(!dev?.delete(flush: true)){

							}
						}
					}
				}
			} catch (Exception e) {
				Device.withTransaction {
					Device dev = Device.findById(deviceInstance?.id)
					if(dev){
						if(!dev?.delete(flush: true)){


						}
					}
				}
			}
			devicesTobeDeleted.each { childDeviceId ->
				Device childDevice = Device.findById(childDeviceId)
				devicegroupService.updateExecDeviceReference(childDevice)

				try {
					def status
					Device.withTransaction {
						status = childDevice.delete(flush: true)
					}
					if(!status){
						Device.withTransaction {
							Device dev = Device.findById(childDevice?.id)
							if(dev){
								dev?.delete(flush: true)
							}
						}
					}
				} catch (Exception e) {
					Device.withTransaction {
						Device dev = Device.findById(childDevice?.id)
						if(dev){
							dev?.delete(flush: true)
						}
					}
				}
			}

		}
		catch (DataIntegrityViolationException e) {
			return false
		}
		return true
	}
	
	/**
	 * REST API for add new device
	 */
	def createNewDevice(){
		JsonObject deviceObj = new JsonObject()
		try {
			String deviceStreams , deviceOcapId
			def node
			if(params?.deviceXml){
				def uploadedFile = request.getFile('deviceXml')
				if(uploadedFile){
				if( uploadedFile?.originalFilename?.endsWith(".xml")) {

					InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
					def fileContent = reader?.readLines()
					int indx = 0
					String s = ""
					String xml
					if(fileContent && fileContent.size() > 0){
						try{
							if(fileContent.get(indx))	{
								while(indx < fileContent.size()){
									s = s + fileContent.get(indx)+"\n"
									indx++
								}
							}
							xml = s
							XmlParser parser = new XmlParser();
							node = parser.parseText(xml)
							List<String> streams= new ArrayList<String>()
							List<String> ocapId= new ArrayList<String>()
							def deviceName =  node?.device?.stb_name?.text()?.trim()
							def  deviceIp =node?.device?.stb_ip?.text()?.trim()
							String boxType = node?.device?.box_type?.text()?.trim()
							def recorderId = node?.device?.recorder_id?.text()?.trim()
							def socVendor = node?.device?.soc_vendour?.text()?.trim()
							def boxManufacture = node?.device.box_manufacture?.text()?.trim()
							def gateway = node?.device?.gateway_name?.text()?.trim()
							
							node?.device?.streams?.stream?.each{
								streams.add(it?.@id)
								ocapId.add(it?.text()?.trim())
							}
							
							def boxTypeObj = BoxType.findByName(boxType)
							def boxManufactureObj = BoxManufacturer.findByName(boxManufacture)
							def socVendorObj = SoCVendor.findByName(socVendor)
							if(!boxType){
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","Boxtype shouldnot be empty ")
							}else if(!boxTypeObj){
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","No valid boxtype available with name "+boxType)
							}else if(Device.findByStbName(deviceName)){
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","Device name is already exists " +deviceName)
							}else if(!deviceName){
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","Device name shouldnot be empty")
							}else if(!deviceIp){
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","Device IP name shouldnot be empty")
							}else if(deviceIp && Device.findByStbIp(deviceIp)){
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","Device IP is already exists"+deviceIp)
							}else if(!socVendor){
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","SOC Vendor  shouldnot be empty")
							}else if(socVendor && !SoCVendor.findByName(socVendor)){
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","No valid soc vendor available with name "+socVendor)
							}else if(!boxManufacture){
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","Box Manufacture shouldnot be empty")
							}else if(boxManufacture && !BoxManufacturer.findByName(boxManufacture)){
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","No valid box manufacture available with name "+boxManufacture)
							}else{
								BoxType boxTypeInastnce = BoxType.findByName(boxType)
								boolean valid = true
								if(boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_GATEWAY)
								|| boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_STANDALONE_CLIENT)){

									if(recorderId?.trim()?.length() ==  0){
										valid = false
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","Recorder  id should not blank ")
									}else if(streams){
											if(validateOcapIds(streams,ocapId)){
												if(checkDuplicateOcapId(ocapId)){
													valid = false
													deviceObj.addProperty("STATUS","FAILURE")
													deviceObj.addProperty("Remarks","Duplicate Ocap id ")
												}
											}else{
												valid = false
												deviceObj.addProperty("STATUS","FAILURE")
												deviceObj.addProperty("Remarks","Stream information is not correct")
											}
										}
								}else{
									if(gateway){
										if(!Device.findByStbName(gateway)){
											valid = false
											deviceObj.addProperty("STATUS","FAILURE")
											deviceObj.addProperty("Remarks","No valid gateway device available with name" +gateway)
										}
									}
								}
								if(valid){
								try{

									int status = 0

									Device deviceInstance = new Device()
									deviceInstance.stbName = deviceName
									deviceInstance.stbIp = deviceIp
									deviceInstance.soCVendor = socVendorObj
									deviceInstance.boxType=boxTypeObj
									deviceInstance.boxManufacturer =boxManufactureObj

									if(boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_CLIENT)){
										status = 1
										deviceInstance.gatewayIp =gateway

									}else if(boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_GATEWAY)
									|| boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_STANDALONE_CLIENT)){
									
										status = 2
										deviceInstance.recorderId = recorderId
										deviceInstance.macId =""
									}

									if(status > 0 && deviceInstance.save(flush:true)){
										if(status == 2){
											devicegroupService.saveToDeviceGroup(deviceInstance)
											saveDeviceStream(streams, ocapId, deviceInstance)
										}
										deviceObj.addProperty("STATUS","Success")
										deviceObj.addProperty("Remarks","Device saved successfully ")
									}else{
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","Device not saved ")
									}

								}catch (Exception e){
									println "ERROR"+e.getMessage()
									deviceObj.addProperty("STATUS","FAILURE")
									deviceObj.addProperty("Remarks","Device not saved ")
								}
								}
							}
						}catch(Exception e){
							println "ERROR "+e.getMessage()
							deviceObj.addProperty("STATUS","FAILURE")
							deviceObj.addProperty("Remarks","Device not saved "+e.getMessage())
						}
					}else{
						deviceObj.addProperty("STATUS","FAILURE")
						deviceObj.addProperty("Remarks","XML file is not proper")
					}
				}else {
					deviceObj.addProperty("STATUS","FAILURE")
					deviceObj.addProperty("Remarks","please check the file name ")
				}
				}else{
				deviceObj.addProperty("STATUS","FAILURE")
				deviceObj.addProperty("Remarks","File does not exists  ")
			}
			}else{
				deviceObj.addProperty("STATUS","FAILURE")
				deviceObj.addProperty("Remarks","File does not exists  ")
			}
		} catch (Exception e) {
		println " EE "+e.getMessage()
			deviceObj.addProperty("STATUS","FAILURE")
			deviceObj.addProperty("Remarks","Device not saved "+e.getMessage())
		}
		println " device obj "+deviceObj
		render deviceObj
	}
}


