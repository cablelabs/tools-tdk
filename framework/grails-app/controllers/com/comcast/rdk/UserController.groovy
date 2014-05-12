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

import grails.converters.JSON
import org.springframework.dao.DataIntegrityViolationException
import static com.comcast.rdk.Constants.KEY_ON
import org.apache.shiro.crypto.hash.Sha256Hash
import org.apache.commons.lang.RandomStringUtils

class UserController {

   def mailService
	
   static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

    def index() {
        redirect(action: "create")
    }

    def create(Integer max) {
        params.max = Math.min(max ?: 10, 100)
        [userInstance: new User(params),userInstanceList: User.list(params), userInstanceTotal: User.count()]
    }

	
    def save(Integer max) {		
        params.max = Math.min(max ?: 10, 100)
        def userInstance = new User(params)
		userInstance.passwordHash = new Sha256Hash(params?.passwordHash).toHex()
        if (!userInstance.save(flush: true)) {
            render(view: "create", model: [userInstance: userInstance, userInstanceList: User.list(params), userInstanceTotal: User.count()])
            return
        }

        flash.message = message(code: 'default.created.message', args: [message(code: 'user.label', default: 'User'), userInstance.username])
        redirect(action: "create", id: userInstance.id)
    }
	
	/**
	 * Method to get the page to register a new user.
	 * @return
	 */
	def registerUser(){
		if(params?.userId){
			[userInstance: User.findById(params?.userId)]
		}
		else{
			[userInstance: new User(params)]
		}
	}

	/**
	 * Method to save the new user from the register user page
	 * @return
	 */
	def saveUser() {
		def userInstance = new User(params)
		/*if( params?.passwordHash!= params?.confirmPassword){
			flash.error = "The passwords you entered has a mismatch"
			render(view: "registerUser", model: [userInstance: userInstance])
			return
		}*/
		userInstance.passwordHash = new Sha256Hash(params?.passwordHash).toHex()
		if (!userInstance.save(flush: true)) {
			render(view: "registerUser", model: [userInstance: userInstance])
			return
		}
		Role role = Role.findByName("ADMIN")
		def userCriteria = User.createCriteria()
		def results = userCriteria.list {
			roles {
				eq('name', "ADMIN")
			}
		}
		println results.email.toArray()
		try {
			mailService.sendMail {
				to results.email.toArray()
				subject "New User Registration"
				body ' [RDK Tool] : User '+userInstance.name+' is registed with username '+userInstance.username
			}

		} catch (Exception e) {
			e.printStackTrace()
		}
		flash.message = message(code: 'default.created.message', args: [message(code: 'shiroUser.label', default: 'User'), userInstance.name])
		redirect(action: "registerUser", params: [userId: userInstance?.id])
	}
	
	def changePassword = {
		if(!(params?.username).trim()){
			flash.error =  "Please enter valid username"
		}
		else {
			def userInstance = User.findByUsername(params?.username)
		
			if (!userInstance || userInstance == null) {
				flash.error =  "Please enter valid username"
			}
			else {
				if((userInstance.roles).empty){
					flash.error="Your approval is pending.Please contact admin for approval"
				}
				else {
					def oldPasswordByUser =new Sha256Hash (params?.oldPassword).toHex()
					
					if(oldPasswordByUser != userInstance.passwordHash){
						flash.error = "Invalid username or password"
					}
					else {
			
						if((!(params?.newPassword).trim())&&(!(params?.confirmPassword).trim())) {
							flash.error = "Enter valid new password"
						}
						else {
							if( params?.newPassword!= params?.confirmPassword){
								flash.error = "The passwords you entered has a mismatch"
							}
							else {
								userInstance.passwordHash =new Sha256Hash(params?.newPassword).toHex()
								if (!userInstance.save(flush: true)) {
									flash.error  ="Password updation failed"
								}
								else {
									flash.message = "Password is updated successfully"
								}
							}
						}
					}
				}
			}
		}
		render(template: "resultMessage", model: [params : params])
	}
	
    def update(Long id, Long version, Integer max) {
        def userInstance = User.get(id)
		params.max = Math.min(max ?: 10, 100)
        if (!userInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'user.label', default: 'User'), id])
            render(view: "create", model: [userInstance: userInstance, userInstanceList: User.list(params), userInstanceTotal: User.count()])
            return
        }

        if (version != null) {
            if (userInstance.version > version) {
                userInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                          [message(code: 'user.label', default: 'User')] as Object[],
                          "Another user has updated this User while you were editing")
                render(view: "create", model: [userInstance: userInstance, userInstanceList: User.list(params), userInstanceTotal: User.count()])
                return
            }
        }
		def oldRole = userInstance.roles
		def oldpassword=userInstance.passwordHash
		def passwrd = userInstance.passwordHash
		userInstance.properties = params
		if(params?.passwordHash){
			def updatedPassword = params?.passwordHash
			if(updatedPassword.equals(passwrd)){
				userInstance.passwordHash = params?.passwordHash
			}
			else{
				userInstance.passwordHash = new Sha256Hash(params?.passwordHash).toHex()
			}
		}
		else{
			userInstance.passwordHash = passwrd
		}
        if (!userInstance.save(flush: true)) {
            render(view: "create", model: [userInstance: userInstance, userInstanceList: User.list(params), userInstanceTotal: User.count()])
            return
        }

        flash.message = message(code: 'default.updated.message', args: [message(code: 'user.label', default: 'User'), userInstance.username])
        redirect(action: "create")
    }
	
	def populateFields(){
		def valueList = []
		User user = User.findById(params?.id)
		valueList.add( user?.id )
		valueList.add( user?.name )
		valueList.add( user?.email )
		valueList.add( user?.username )
		valueList.add( user?.groupName?.id )
		if(user?.passwordHash){
			valueList.add( user?.passwordHash )
		}
		else{
			valueList.add("null")
		}
		user?.roles.each{rol ->
			valueList.add( rol?.id )
		}
		render valueList as JSON
	}
	
    def deleteUser(){
        def countVariable = 0
        def userInstance
        if(params?.listCount){ // to delete record(s) from list.gsp
            for (iterateVariable in params?.listCount){
                countVariable++
                if(params?.("chkbox"+countVariable) == KEY_ON){
                    def idDb = params?.("id"+countVariable).toLong()
                    userInstance = User.get(idDb)
                    if (userInstance) {
                         if (!userInstance.delete(flush: true)) { 
                             
                         }   
                    }
                }
            }
        }
        redirect(action: "create")
    }
	
	
}
