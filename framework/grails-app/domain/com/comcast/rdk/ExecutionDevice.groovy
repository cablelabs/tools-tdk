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
import java.util.Set;

/**
 * Domain class for saving the device in script Execution
 * @author sreejasuma
 */

class ExecutionDevice {

    Execution execution

    /**
     * Device in which the script is executed
     */
    String device
	
	/**
	 * DeviceIP in which the script is executed
	 */
	String deviceIp
	
	/**
	 * Status of the execution
	 */
    String status = "UNDEFINED"
	
	/**
	 * Date and time in which the script is executed
	 */
	Date dateOfExecution
	
	/**
	 * Start time of execution
	 */
	String executionTime
	
	/**
	 * Set of ExecutionResults to the execution
	 */
	Set executionresults
	 
    /**
	 * Execution can have many execution results.
	 */
	static hasMany = [ executionresults : ExecutionResult ]
    
    static constraints = {             
        device(nullable:false, blank:false)
		execution(nullable:false, blank:false)
		dateOfExecution(nullable:true, blank:true)
		executionTime(nullable:true, blank:true)
		status(nullable:false, blank:false)
		deviceIp(nullable:false, blank:false)
    }
    
    static mapping = {
        cache true
        sort id : "desc"
		executionresults sort: 'id', order: 'asc'
    }
    
}
