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
 * domain object to save the third party execution details
 *
 */
class ThirdPartyExecutionDetails {
	
	Execution execution
	
	String execName
	
	String url
	
	String callbackUrl
	
	String filePath
	
	long executionStartTime
	
	String imageName
	
	String boxType
	
	Category category = Category.RDKV

    static constraints = {
		execName(nullable:true, blank:true)
		url(nullable:true, blank:true)
		callbackUrl(nullable:true, blank:true)
		filePath(nullable:true, blank:true)
		imageName(nullable:true, blank:true)
		boxType(nullable:true, blank:true)
		executionStartTime(nullable:true, blank:true)
		category(nullable:false, blank:false)
    }
	
	static mapping = {
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
