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
 * Domain class for saving the script execution details
 * @author sreejasuma
 *
 */

class Execution {
    
    /**
     * Name of execution
     */
    String name
    
    /**
     * Script that is executed
     */
    String script
    
    /**
     * Devices in which the script is executed
     */
    String device 
    
    /**
     * ScriptGroup that is executed
     */
    String scriptGroup
    
    /**
     * Device Group in which the script 
     * is executed
     */
    String deviceGroup
       
    /**
     * Result of the script execution
     */
    String result
    
    /**
     * The complete data obtained after the
     * execution of the script
     */
    String outputData
    
    /**
     * Date and time in which the script is executed
     */
    Date dateOfExecution
    
    /**
     * time taken for execution
     */
    String executionTime

    /**
     * Set of ExecutionResults to the execution
     */
     Set executionresults
	 
	/**
	 * Flag to identify the whether the given instance is marked for deletion or not.
	 */
	int isMarked = 0;
	
	/**
	 * Flag to mark the execution as aborted
	 */
	boolean isAborted = false
	
	boolean isRerunRequired = false

	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	boolean isPerformanceDone
	
	String executionStatus
	
	/**
	 * application url data
	 */
	String applicationUrl
	
	/**
	 * Flag to mark is bench mark enabled for the execution 
	 */
	boolean isBenchMarkEnabled = false
	
	/**
	 * Flag to mark is SystemDiagnostics enabled for the execution
	 */
	boolean isSystemDiagnosticsEnabled = false
	
	/**
	 * Object to save the third party execution details for the execution(optional)
	 */
	ThirdPartyExecutionDetails thirdPartyExecutionDetails = null
	
	/**
	 * Execution can have many execution results.
	 */
	static hasMany = [ executionresults : ExecutionResult ]
    
    static constraints = {
        name(nullable:false, blank:false,unique:true)
        scriptGroup(nullable:true, blank:true)       
        deviceGroup(nullable:true, blank:true)
        result(nullable:true, blank:true)
        outputData(nullable:true, blank:true)       
        dateOfExecution(nullable:true, blank:true)  
        executionTime(nullable:true, blank:true)
        script(nullable:true, blank:true)
        device(nullable:true, blank:true)
		groups(nullable:true, blank:true)
		isPerformanceDone(nullable:true, blank:true)
		executionStatus(nullable:true, blank:true)
		thirdPartyExecutionDetails(nullable:true, blank:true)
		isBenchMarkEnabled(nullable:true, blank:true)
		isSystemDiagnosticsEnabled(nullable:true, blank:true)
		isAborted(nullable:true, blank:true)
		isRerunRequired(nullable:true, blank:true)
		applicationUrl(nullable:true, blank:true)
    }
    
    static mapping = {
        //cache true
        outputData type: 'text'
        sort id : "desc"
		executionresults sort:'id' , order: 'asc'
		datasource 'ALL'
    }
    
    @Override
    String toString() {
        return name ?: 'NULL'
    }
}
