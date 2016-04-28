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
 * Domain class for holding the radio streaming details
 *
 */
class RadioStreamingDetails {
	/**
	 * Stream Id
	 */
	String streamId
	

	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	static constraints = {
		streamId(nullable:false, blank:false, maxSize:64, unique:true)
		groups(nullable:true, blank:true)
	}
	
	
	@Override
	String toString() {
		return streamId ?: 'NULL'
	}

	static mapping = {
		datasource 'ALL'
	}
    
}
