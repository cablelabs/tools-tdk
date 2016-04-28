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
 * Domain class for saving the ExecuteMethodResult of each script execution details
 * @author sreejasuma
 *
 */

import com.comcast.rdk.Category

class ExecuteMethodResult {
    
    /**
     * ExecutionResult object 
     */
    ExecutionResult executionResult
    
    /**
     * Test function name
     */
    String functionName
    
    /**
     * Expected result of the script execution
     */
    String expectedResult
    
    /**
     * Actual result after the script execution
     */
    String actualResult
    
    /**
     * Status of the string
     */
    String status
	Category category
   
       
    static constraints = {  
        executionResult(nullable:false)
        expectedResult(nullable:true, blank:true)
        actualResult(nullable:true, blank:true)    
        status(nullable:true, blank:true)
        functionName(nullable:true, blank:true)
		category(nullable:false, blank:false)
    }
    
    static mapping = {
        cache true
        sort id : "desc"
		datasource 'ALL'
    }
    
}
