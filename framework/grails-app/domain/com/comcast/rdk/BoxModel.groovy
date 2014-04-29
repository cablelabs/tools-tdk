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
 * Class represents a BoxModel.
 * @author sreejasuma
 */
class BoxModel {

    /**
     * Name of the BoxModel
     */
    String name
	
	Groups groups
	
    static constraints = {
        name(unique:true, blank:false, nullable:false)
		groups(nullable:true, blank:true)
    }
    
	@Override
	String toString() {
		return name ?: 'NULL'
	}
}
