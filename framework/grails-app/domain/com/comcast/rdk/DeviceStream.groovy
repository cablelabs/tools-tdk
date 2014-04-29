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
 * Domain class for holding the details of device-stream-ocapid details 
 * @author sreejasuma
 */

class DeviceStream
{
    
    /**
     * Device Instance
     */
    Device device
    
    /**
     * StreamingDetails Instance
     */
    StreamingDetails stream
    
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
      
    
}
