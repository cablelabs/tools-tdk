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
 * Domain object to hold the meta data regarding script
 *
 */
class ScriptFile {

	String scriptName;
	
	String moduleName;
	
	static constraints = {
		scriptName(nullable:false, blank:false)
		moduleName(nullable:true, blank:true)
	}
	
	static mapping = {
		scriptName type: 'text'
		moduleName type: 'text'
		sort scriptName : "asc"
		datasource 'ALL'
	}

	@Override
	String toString() {
		return (scriptName != null ) ? (scriptName) : 'NULL'
	}
	
	public boolean equals( object) {
		if(object instanceof ScriptFile){
			ScriptFile script = object
			return (script.moduleName.equals(moduleName) && script?.scriptName.equals(scriptName));
		}
		
		return false
	};

}