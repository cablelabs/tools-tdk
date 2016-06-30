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
 * Domain class to save the pending execution repeat details
 *
 */
class RepeatPendingExecution {
	
	/**
	 * Name of the device for which repeat is pending
	 */
	String deviceName
	
	/**
	 * status of repeat pending execution
	 */
	String status
	
	/**
	 * name of the execution which is to be repeated
	 */
	String executionName
	
	/**
	 * number of complete execution pending
	 */
	int completeExecutionPending = 0
	
	/**
	 * index of the current execution
	 */
	int currentExecutionCount = -1
	
	Category category = Category.RDKV

    static constraints = {
		deviceName(nullable:false, blank:false)
		status(nullable:false, blank:false)
		completeExecutionPending(nullable:true, blank:true)
		currentExecutionCount(nullable:true, blank:true)
		executionName(nullable:false, blank:false)
		category(nullable:false, blank:false)
    }
	
	@Override
	String toString() {
		return (deviceName + " - " + executionName) ?: 'NULL'
	}
	static mapping = {
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
