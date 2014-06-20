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
import org.springframework.dao.DataIntegrityViolationException
import java.util.concurrent.Executors


class DeviceGroupController {

    static allowedMethods = [save: "POST", update: "POST", delete: "POST", updateDevice : "POST"]
    /**
     * Injecting devicegroupService
     */
    def devicegroupService
	def utilityService
	
	private static final String DEVICESTREAM_QUERY = "delete DeviceStream d where d.device = :instance1"
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
            def result = [url: getApplicationUrl(), streamingDetailsInstanceList: StreamingDetails.list(), streamingDetailsInstanceTotal: StreamingDetails.count()]
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
        
        /**
         * Check whether streams are present
         * and there is no duplicate OcapIds
         */
        if((params?.streamid)){
			if(checkDuplicateOcapId(params?.ocapId)){
                flash.message = message(code: 'duplicate.ocap.id')
				render(flash.message)
                return
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
		
        def deviceStream = DeviceStream.findAllByDevice(deviceInstance)

        [url : getApplicationUrl(),deviceInstance: deviceInstance, flag : flag, gateways : devices, deviceStreams : deviceStream, editPage : true, uploadBinaryStatus: deviceInstance.uploadBinaryStatus, id: id]
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
			
			String currentBoxType = deviceInstance?.boxType?.type.toLowerCase()
			
			BoxType boxType = BoxType.findById(params?.boxType?.id)
			
			String newBoxType = boxType.type.toLowerCase()

            deviceInstance.properties = params

            if(currentBoxType.equals( BOXTYPE_CLIENT )){
                if(newBoxType.equals( BOXTYPE_CLIENT )){
                    deviceInstance.gatewayIp = params?.gatewayIp
                    deviceInstance.recorderId = ""
                    DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
                }
                else{
                    deviceInstance.gatewayIp = ""
                    deviceInstance.recorderId = params?.recorderId
                }
            }
            else{
                if(currentBoxType.equals( BOXTYPE_GATEWAY )){
                    if(newBoxType.equals( BOXTYPE_CLIENT )){
                        deviceInstance.gatewayIp = params?.gatewayIpedit
                        deviceInstance.recorderId = ""
                        DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
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
                if(newBoxType.equals( BOXTYPE_GATEWAY )){
					
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
                if(deviceInstance.boxType.type.toLowerCase().equals( BOXTYPE_GATEWAY )){
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

    /**
     * Save device specific stream details
     * @return
     */
    def saveDeviceStream(final def streamIdList, final def ocapIdList, final Device deviceInstance){
		
		def deviceStreamList = DeviceStream.findAllByDevice(deviceInstance)		
		if(deviceStreamList?.size() > 0){
			DeviceStream.executeUpdate("delete DeviceStream d where d.device = :instance1",[instance1:deviceInstance])
		}
				
        DeviceStream deviceStream
        StreamingDetails streamingDetails

        for(int i = 0; i < streamIdList?.size() ; i++){
			
            streamingDetails = StreamingDetails.findByStreamId(streamIdList[i].toString())
            deviceStream = new DeviceStream()
            deviceStream.device = deviceInstance
            deviceStream.stream = streamingDetails
            deviceStream.ocapId = ocapIdList[i]
            if(!(deviceStream.save(flush:true))){							
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
				devicegroupService.updateExecDeviceReference(deviceInstance)
				//DeviceGroup.executeUpdate("delete DeviceGroup d where d.device = :instance1",[instance1:deviceInstance])

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
        boxTypes.add( boxType.type.toLowerCase().trim() )
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
}


