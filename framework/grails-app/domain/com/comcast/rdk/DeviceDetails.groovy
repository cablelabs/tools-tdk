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
 * Domain class for holding the details of device
 * @author sreejasuma
 */

class DeviceDetails
{
    
    /**
     * Device Instance
     */
    Device device
    
    /**
     * Device parameter name
     */
    String deviceParameter
    
    /**
     * Device parameter value 
     */	
    String deviceValue
    
    static constraints = {
        device(nullable:false, blank:false)
        deviceParameter(nullable:false, blank:false)
        deviceValue(nullable:true, blank:true)       
    }
	
	static mapping = {
		deviceValue type: 'text'
		datasource 'ALL'
	}

}
