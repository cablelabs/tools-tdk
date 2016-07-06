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

class Groups {

	String name
	
    static constraints = {
		name(unique:true, blank:false, nullable:false)
    }
	
	@Override
	String toString() {
		return name ?: 'NULL'
	}
	
	static mapping = {
		datasource 'ALL'
	}
}