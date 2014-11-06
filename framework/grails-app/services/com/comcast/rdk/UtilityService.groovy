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

import org.apache.shiro.SecurityUtils
import groovy.xml.MarkupBuilder
import org.custommonkey.xmlunit.*
class UtilityService {
	static datasource = 'DEFAULT'
	
	def scriptService

	def Groups getGroup(){
		def user = User.findByUsername(SecurityUtils.subject.principal)
		def group = Groups.findById(user.groupName?.id)
		return group
	}
	
	
	def String writexmldata(String execName){
		Execution executionInstance = Execution.findByName(execName)
		def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		
		xml.TestExecutionResult(name=executionInstance.name status=executionInstance.result)() {
			
			executionDevice.each{ executionDeviceInstance ->
				Device(name=executionDeviceInstance?.device ip=executionDeviceInstance?.deviceIp exectime=executionDeviceInstance?.executionTime status=executionDeviceInstance?.status)
				
				executionDeviceInstance.executionresults.each{ executionResultInstance ->
					Scripts(name=executionResultInstance?.script status=executionResultInstance?.status)
					executionResultInstance.executemethodresults.each{executionResultMthdsInstance ->
						Function(name:executionResultMthdsInstance?.functionName){												
							ExpectedResult(executionResultMthdsInstance?.expectedResult)
							ActualResult(executionResultMthdsInstance?.actualResult)
							Status(executionResultMthdsInstance?.status)
						}
					}
					LogData(executionResultInstance?.executionOutput)
				}
			}		
		}
	}	

}

