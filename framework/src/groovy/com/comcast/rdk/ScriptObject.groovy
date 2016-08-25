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
 * Class to hold the script related informations
 *
 */
class ScriptObject {
	
	String name
	
	String module
	
	PrimitiveTest primitiveTest
	
	Set boxTypes
	
	Set rdkVersions
	
	Set scriptTags
	ScriptFile scriptFile
	
	boolean longDuration
	Set  testProfile

}
