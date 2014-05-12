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
 * Class represents a RDK module.
 * @author ajith
 */
class Module{

    /**
     * Name of the module
     */
    String name

    /**
     * Group associated with the module
     */
    TestGroup testGroup
    
    /**
     * RDK Version
     */
    String rdkVersion
	
	/**
	 * RDK Version
	 */
	int executionTime
    
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups

	static hasMany = [logFileNames: String]
	
    static constraints = {
        name(unique:true, blank:false, nullable:false)
        testGroup(nullable:false, blank:false)
        rdkVersion(nullable:false, blank:false)
		groups(nullable:true, blank:true)	
		executionTime(nullable:true, blank:true)
    }

	static mapping = {
		cache true
		sort name : "asc"
		datasource 'ALL'
	}
	
	@Override
	String toString() {
		return name ?: 'NULL'
	}
}
