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
 * Domain class for grouping the devices 
 * @author sreejasuma
 *
 */

class DeviceGroup
{
      
    /**
     * Name of the Group.     
     */
    String name
    
   /**
    * Set of Devices to the user
    */    
    Set devices
    
    /**
     * Status of the devicegroup
     * Whether the script is executed on the selected devicegroup
     */
    Status status
    
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
    /**
     * DeviceGroup can have many devices.
     */
    static hasMany = [ devices: Device ]
    
    static constraints = {
        name(nullable:false, blank:false, unique:true)      
        status(nullable:true, blank:true)      
		groups(nullable:true, blank:true)
    }
   
    static mapping = {
        cache true
        sort id : "asc"        
    }

   
  
    @Override
    String toString() {
        return name ?: 'NULL'
    }
    
}
