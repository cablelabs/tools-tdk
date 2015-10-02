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

import java.util.Date;

/**
 * Domain class for saving the script execution details
 * @author sreejasuma
 *
 */


class ExecutionResult {

    Execution execution
    
	ExecutionDevice executionDevice	
	
    /**
     * Script that is executed
     */
    String script
    
    /**
     * Devices in which the script is executed
     */
    String device
    
    /**
     * Status of execution of script
     */
    String status = "UNDEFINED"
    
    /**
     * Set of ExecuteMethodResult to the ExecutionResult
     */
    Set executemethodresults
	
	String executionOutput
	
	Set performance
	
	Device execDevice
	
	String deviceIdString
	
	/**
	 * Date and time in which the script is executed
	 */
	Date dateOfExecution
	
	String executionTime
	
	String moduleName
	
	String totalExecutionTime 
	
    /**
     * Execution can have many execution results.
     */
    static hasMany = [ executemethodresults : ExecuteMethodResult, performance :  Performance]
	
    
    static constraints = {             
        script(nullable:false, blank:false)
        device(nullable:false, blank:false)
        status(nullable:true, blank:true)
		executionOutput(nullable:true, blank:true)		
		execDevice(nullable:true, blank:true)
		deviceIdString(nullable:true, blank:true)
		dateOfExecution(nullable:true, blank:true)
		executionTime(nullable:true, blank:true)
		moduleName(nullable:true, blank:true)
		totalExecutionTime(nullable:true, blank:true)
    }
    
    static mapping = {
        cache true
		executionOutput type: 'text'
        sort id : "asc"
		executemethodresults sort: 'id', order: 'asc'
		datasource 'ALL'
    }
    
}
