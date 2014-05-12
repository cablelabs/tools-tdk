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
 * Class represents BoxTypes.
 * @author sreejasuma
 */
class BoxType {

    /**
     * Name of the BoxType
     */
    String name

    /**
     * Type of box
     * Eg: client, gateway
     */
    String type 
	
	/**
	 * Indicates the group name which the box belongs
	 */
	Groups groups
    
    static constraints = {
        name(unique:true, blank:false, nullable:false)
        type(blank:false, nullable:false)
		groups(nullable:true, blank:true)
    }

	@Override
	String toString() {
		return name ?: 'NULL'
	}
	
	static mapping = {
		datasource 'ALL'
	}
}
