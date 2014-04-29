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

/**
 * Represents the status of the Device. 
 * FREE status indicates device is free and currently no script is running on this device 
 * ALLOCATED status indicates currently a script is running on this device
 * @author sreejasuma
 */

public enum DeviceStatus
{
    FREE,
    ALLOCATED
}
