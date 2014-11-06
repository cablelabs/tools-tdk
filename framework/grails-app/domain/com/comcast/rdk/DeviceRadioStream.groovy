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
 * omain class for holding the details of device- radio stream-ocapid details 
 *
 */
class DeviceRadioStream {

    /**
     * Device Instance
     */
    Device device
    
    /**
     * StreamingDetails Instance
     */
    RadioStreamingDetails stream
	
    /**
     * OcapId corresponding to device and
     * Stream details 
     */
    String ocapId
    
    static constraints = {
        device(nullable:false, blank:false)
        stream(nullable:false, blank:false)
        ocapId(nullable:false, blank:false)       
    }
	
	static mapping = {
		datasource 'ALL'
	}
      
}
