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
package rdk.test.tool

import java.awt.RadialGradientPaintContext;

import com.comcast.rdk.*
import javax.servlet.http.HttpServletRequest
import static com.comcast.rdk.Constants.*
import org.springframework.web.context.request.RequestContextHolder
import org.codehaus.groovy.grails.validation.routines.InetAddressValidator
import org.hibernate.loader.custom.CustomLoader;

//@DisallowConcurrentExecution
class DeviceStatusJob {
	static triggers = { //simple repeatCount : -1
		simple repeatInterval: 20000l }
	def executionService
	def executescriptService
	def devicegroupService
	def deviceStatusService
	def grailsApplication
	private HttpServletRequest servletRequest;

	def concurrent = false
	
	/**
	 * Method which is invoked based on the schedule time.
	 * Synchonized thread block which will be triggered in every 30 sec(It is configurable - Currently givesn as 30 sec)
	 * It will trigger device status checking for all devices and update the same in DB.
	 * Preform Port forwading for moca devices.
	 * @param context
	 */
	synchronized def execute() {
		try{
			DeviceStatusUpdater.updateDeviceStatus(grailsApplication,deviceStatusService,executescriptService);		
		}catch(Exception e){			
			e.printStackTrace();
		}
	}

}