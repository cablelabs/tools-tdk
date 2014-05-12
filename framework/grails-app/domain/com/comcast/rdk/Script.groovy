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
 * Class that holds script details.
 * @author ajith
 */
class Script {
    
    /**
     * Name of the script.
     * Name shall not be empty.
     */
    String name
    
    /**
     * ScriptContent    
     */
    String scriptContent

    /**
     * Primitive test Name
     */
    PrimitiveTest primitiveTest

    /**
     * Short description about the script
     */
    String synopsis
	
	/**
	 * Boxtypes of script
	 */
    Set boxTypes
	
    /**
     * Status of the script
     * Whether the script is selected for execution 
     */
    Status status =  Status.FREE
	
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	/**
	 * Execution Time
	 */
	int executionTime
	
	/**
	 * true if script needs to be skipped while executing test suite
	 */
	boolean skip = false
	
	/**
	 * Short description about the reason for skipping the script
	 */
	String remarks = ""
	
	
	static hasMany = [boxTypes: BoxType]

    static constraints = {
        name(nullable:false, blank:false, unique:true)
        synopsis(nullable:true, blank:true)
        scriptContent(blank:true)
        status(nullable:true, blank:true)
		groups(nullable:true, blank:true)
		executionTime(nullable:true, blank:true)		
    }
	
    /**
     * ScriptContent can be LongText field.
     */
    static mapping = {
        scriptContent type: 'text'
        synopsis type: 'text'
        sort name : "asc"
		datasource 'ALL'
    }

    @Override
    String toString() {
        return name ?: 'NULL'
    }
 
   
    
}
