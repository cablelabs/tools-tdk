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
 * Object to hold the script data
 *
 */
class ScriptData {

	String scriptName
	
	String moduleName
	
	@Override
	String toString() {
		return (scriptName != null ) ? (scriptName) : 'NULL'
	}
	
	public boolean equals(Object data){
		if(data instanceof ScriptData){
			return (scriptName.equals(((ScriptData)data)?.scriptName))
		}
		return false;
	}
	
	
}
