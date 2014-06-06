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
 * Class represents RDK Versions.
 */
class RDKVersions {
    
    /**
     * Name of the RDK Version
     */
	String buildVersion

	/**
	 * Indicates the group name which the box belongs
	 */
	Groups groups
    
    static constraints = {
		buildVersion(unique:true, blank:false, nullable:false)
		groups(nullable:true, blank:true)
    }

	@Override
	String toString() {
		return buildVersion ?: 'NULL'
	}
	
	static mapping = {
		sort buildVersion : "asc"
		datasource 'ALL'
	}
}
