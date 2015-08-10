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
 * This file has been changed from code generated by Grails
 */
package com.comcast.rdk

/**
 * Generated by the Shiro plugin. This filters class protects all URLs
 * via access control by convention.
 */
class SecurityFilters {
    def publicActions = [     
		user: ['changePassword','registerUser','saveUser'],
		primitiveTest : ['getJson','getStreamDetails'],
		execution : ['saveLoadModuleStatus','saveResultDetails','getDeviceStatusList','getDeviceStatus','thirdPartyJsonResult','thirdPartyTest','showResult','getDetailedTestResult','getClientPort','stopThirdPartyTestExecution','getAgentConsoleLog','getRealtimeDeviceStatus','getExecutionOutput'],
		deviceGroup : ['uploadAgentBinaries'],
    ];

    private boolean findAction(actionMap, controllerName, actionName) {
        def c = publicActions[controllerName]
        return (c) ? c.find { (it == actionName || it == '*')} != null : false
    }

    def filters = {
        publica(controller: '*', action: '*') {
            before = {

                if (!controllerName) return true
                
                // Check for public controller/actions
                def isPublic = findAction(publicActions, controllerName, actionName)

                if (isPublic){
                    return true
                }
                
                return accessControl()
            }
        }
    }
}
