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

import com.comcast.rdk.Category

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
    String rdkVersion = "1"
	
	/**
	 * Time required for executing script
	 */
	int executionTime
    
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	/**
	 * Indicates the category to which the device belongs - RDK-V or RDK-B
	 */
	Category category

	static hasMany = [logFileNames: String , stbLogFiles :String]
	
    static constraints = {
        testGroup(nullable:false, blank:false)
        rdkVersion(nullable:false, blank:false)
		groups(nullable:true, blank:true)	
		executionTime(nullable:true, blank:true)
		category(nullable:false, blank:false)
		name(blank:false, nullable:false,unique:'category' )
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
