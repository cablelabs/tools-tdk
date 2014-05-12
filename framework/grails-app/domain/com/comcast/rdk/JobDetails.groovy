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
 * Class to hold the job details 
 * @author Sreeja
 *
 */
class JobDetails {
   
	/**
	 * Name of job
	 */
	String jobName
    
    /**
     * Name of trigger
     */
	String triggerName
    
    /**
     * Type of Schedule
     */
	String scheduleType
	
    /**
     * Script that is executed
     */   
    List script
    
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
    
    String appUrl
    
    String realPath
    
    String filePath
    
    Date startDate
    
    Date endDate
    
    Date oneTimeScheduleDate
    
    String queryString   
	
	
	String isSystemDiagnostics
	
	String isBenchMark
	
	String rerun
	
	int repeatCount = 1
	
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
    static hasMany = [script : String ]

    static constraints = {
        jobName(nullable:false, blank:false)
        triggerName(nullable:false, blank:false)
        scheduleType(nullable:true, blank:true)
        script(nullable:true, blank:true)
        scriptGroup(nullable:true, blank:true)
        device(nullable:true, blank:true)
        deviceGroup(nullable:true, blank:true)
        appUrl(nullable:false, blank:false)
        realPath(nullable:false, blank:false)
        startDate(nullable:true, blank:true)
        endDate(nullable:true, blank:true)
        oneTimeScheduleDate(nullable:true, blank:true)
        queryString(nullable:true, blank:true)
		isSystemDiagnostics(nullable:true, blank:true)
		isBenchMark(nullable:true, blank:true)
		rerun(nullable:true, blank:true)
		repeatCount(nullable:true, blank:true)
		groups(nullable:true, blank:true)
		
    }
    
    @Override
    String toString() {
        return jobName ?: 'NULL'
    }
	
	static mapping = {
		datasource 'ALL'
	}
   
}
