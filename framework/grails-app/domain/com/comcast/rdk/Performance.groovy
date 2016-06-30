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

class Performance {

	ExecutionResult executionResult
	
	String performanceType
	
	String processName
	
	String processValue
	
	String processValue1
	
	Category category = Category.RDKV
	
	//static belongsTo = [ executionResult:ExecutionResult ]
	
    static constraints = {
		executionResult(nullable:true, blank:true)
		performanceType(nullable:true, blank:true)
		processName(nullable:true, blank:true)
		processValue(nullable:true, blank:true)
		processValue1(nullable:true, blank:true)
		category(nullable:false, blank:false)
    }
	
	static mapping = {
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
