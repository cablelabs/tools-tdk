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
 * Default AuthController class generated as part of shiro plugin
 * for user authentication
 *
 */
import org.apache.shiro.SecurityUtils
import org.apache.shiro.authc.AuthenticationException
import org.apache.shiro.authc.UsernamePasswordToken
import org.apache.shiro.web.util.SavedRequest
import org.apache.shiro.web.util.WebUtils
import org.apache.shiro.grails.ConfigUtils
import org.apache.shiro.crypto.hash.Sha256Hash
import org.apache.commons.lang.RandomStringUtils

class AuthController {
    def shiroSecurityManager

	def mailService
	
    def index = { redirect(action: "login", params: params) }

    def login = {
        return [ username: params.username, rememberMe: (params.rememberMe != null), targetUri: params.targetUri ]
    }

    def signIn = {
        def authToken = new UsernamePasswordToken(params.username, params.password as String)

        // Support for "remember me"
        if (params.rememberMe) {
            authToken.rememberMe = true
        }
        
        // If a controller redirected to this page, redirect back
        // to it. Otherwise redirect to the root URI.
        def targetUri = params.targetUri ?: "/"
        
        // Handle requests saved by Shiro filters.
        def savedRequest = WebUtils.getSavedRequest(request)
        if (savedRequest) {
            targetUri = savedRequest.requestURI - request.contextPath
            if (savedRequest.queryString) targetUri = targetUri + '?' + savedRequest.queryString
        }
        
        try{
            // Perform the actual login. An AuthenticationException
            // will be thrown if the username is unrecognised or the
            // password is incorrect.
            SecurityUtils.subject.login(authToken)

            log.info "Redirecting to '${targetUri}'."
            redirect(controller : "execution", action : "create")
        }
        catch (AuthenticationException ex){
            // Authentication failed, so display the appropriate message
            // on the login page.
            log.info "Authentication failure for user '${params.username}'."
            flash.message = message(code: "login.failed")

            // Keep the username and "remember me" setting so that the
            // user doesn't have to enter them again.
            def m = [ username: params.username ]
            if (params.rememberMe) {
                m["rememberMe"] = true
            }

            // Remember the target URI too.
            if (params.targetUri) {
                m["targetUri"] = params.targetUri
            }

            // Now redirect back to the login page.
            redirect(action: "login", params: m)
        }
    }

    def signOut = {
        SecurityUtils.subject?.logout()      
        redirect(uri: "/")              
    }

    def unauthorized = {
        render "You do not have permission to access this page."
    }
	
	/**
	 * Method to get new password if the user forgot the old password
	 * @param username
	 * @return
	 */
	def forgotPassword= {
		if(!(params?.username).trim()){
			flash.error =  "Please enter valid username"
		}
		else {
				User userInstance = User.findByUsername(params?.username)
				if (!userInstance || userInstance == null ) {
					flash.error = "User not found with Username "+params?.username
				}
				else {
						if((userInstance.roles).empty){
							flash.error="Your approval is pending.Please contact admin for approval"
						}
						else {
							String charset = (('A'..'Z') + ('0'..'9')).join()
							Integer length = 9
							String password = RandomStringUtils.random(length, charset.toCharArray())
						
							mailService.sendMail {
								to userInstance.email
								subject "New password of RDK Tool for UserName "+params?.username
								body "New password is "+password
							}
	   
							userInstance.passwordHash =new Sha256Hash(password).toHex()
							if (!userInstance.save(flush: true)) {
								flash.error="Password updation failed"
		   
							}
							else {
								flash.message="New Password send to users mail Id"
							}
						}
					}
			}
			   redirect(controller:"auth", action: "login")
	}
	
	
}
