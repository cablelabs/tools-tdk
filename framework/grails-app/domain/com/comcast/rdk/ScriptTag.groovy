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

class ScriptTag {
	
	/**
	 * Name of the BoxType
	 */
	String name

    /**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
    static constraints = {
        name(unique:true, blank:false, nullable:false)
		groups(nullable:true, blank:true)
    }
	
	@Override
	String toString() {
		return name ?: 'NULL'
	}
	
	static mapping = {
		sort id : "asc"
		datasource 'ALL'
	}
}
