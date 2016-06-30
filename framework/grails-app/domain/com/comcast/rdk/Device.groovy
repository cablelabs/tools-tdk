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
import com.comcast.rdk.Category

/**
 * Domain class for holding the details of devices 
 * @author sreejasuma, praveenkp
 *
 */

class Device
{
    /**
     * IP of the STB.
     */
    String stbIp
	/**
	 * serialNo of the STB.
	 */
	String serialNo
   
   
    /**
     * Name of the STB.     
     */
    String stbName
    
    /**
     * Port of the STB.
     */
    String stbPort = 8087
	
	/**
	 * Port of the STB.
	 */
	String statusPort = 8088
	/**
	 * Port of the STB.
	 */
	String logTransferPort = 69

	/**
	 * Port of the STB.
	 */
	String agentMonitorPort = 8090
	
    /**
     * Type of the stb
     * It denotes the type of the box
     * Eg: X1, Xi3, XG5
     */
    BoxType boxType
             
    /**
     * Manufacturer of the box
     */
    BoxManufacturer boxManufacturer
    
    /**
     * SoC vendors of the box
     */
    SoCVendor soCVendor
    
    /**
     * Status of the device
     */     
    Status deviceStatus = Status.NOT_FOUND
    
    /**
     * RecorderId of the Gateway
     * Will be present only if the box type is
     * XG1 or XG5
     */
    String recorderId

    /**
     * Gateway IP is the same as deviceIP
     * A device is considered as Gateway 
     * based on the BoxTypes associated with the device
     * Client box required a gatewayIP if it is used for testing
     * an end to end scenario.
     */
    String gatewayIp
	
	/**
	 * Status of upload binary operation
	 */
	UploadBinaryStatus uploadBinaryStatus = UploadBinaryStatus.UNKNOWN

	/**
	 * Mac id of device - It will available only for child Xi3 devices in moca networks.
	 */
	String macId

	/**
	 * List of child devices of a Gateway box.
	 */
	List childDevices

	/**
	 * Flag to identify whether a box is a child one or not.
	 */
	int isChild = 0
	
	/**
	 * Indicates the group name which the device belongs 
	 */
	Groups groups
	
	/**
	 * Category of device
	 */
	Category category = Category.RDKV
    
    static constraints = {
        stbIp(nullable:false, blank:false)
        stbName(nullable:false, blank:false, unique:true)
        boxType(nullable:false, blank:false)
        boxManufacturer(nullable:false, blank:false)
        soCVendor(nullable:false, blank:false)
        recorderId(nullable:true, blank:true)
        gatewayIp(nullable:true, blank:true)
		macId(nullable:true, blank:true)
		groups(nullable:true, blank:true)
		category(nullable:false, blank:false)
		serialNo(nullable:true, blank:true)
    }
	
	static hasMany = [childDevices:Device]

    static mapping = {
        cache true
        sort id : "asc"       
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL' 
    }

    @Override
    public String toString()
    {
        return stbName ?: 'NULL'
    }
    
    
}
