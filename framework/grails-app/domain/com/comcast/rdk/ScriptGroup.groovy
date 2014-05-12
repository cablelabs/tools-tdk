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
 * Domain class for grouping the scripts
 * @author sreejasuma
 *
 */

class ScriptGroup {

    /**
     * Name of the Group.     
     */
    String name

    /**
     * Set of Scripts to the ScriptGroup
     */    
    Set scripts

    /**
     * Status of the scriptgroup
     * Whether the scriptgroup is selected for execution
     */
    Status status = Status.FREE

	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
    /**
     * ScriptGroup can have many scripts.
     */
    static hasMany = [ scripts : Script ]

    static constraints = {
        name(nullable:false, blank:false, unique:true)
        status(nullable:true, blank:true)
		groups(nullable:true, blank:true)
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
