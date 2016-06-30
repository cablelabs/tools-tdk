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

import static com.comcast.rdk.Constants.KEY_ON

import java.util.List;

import org.springframework.dao.DataIntegrityViolationException
import grails.converters.JSON


class ScriptTagController {

	def utilityService
	
    static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

    def index() {
        redirect(action: "create", params: params)
    }
	
    def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		//def scriptTagList = ScriptTag.findAllByGroupsOrGroupsIsNull(groupsInstance,params)		
		//def scriptTagListCnt = ScriptTag.findAllByGroupsOrGroupsIsNull(groupsInstance)
		def scriptTagList = getScriptTagList(groupsInstance,params)
        [scriptTagInstance: new ScriptTag(params) ,scriptTagInstanceList: scriptTagList, scriptTagInstanceTotal: getScriptTagCount(groupsInstance, params), category:params?.category]
    }

    def save(Integer max) {
	
        def scriptTagInstance = new ScriptTag(params)
		params.max = Math.min(max ?: 10, 100)		
		def groupsInstance = utilityService.getGroup()
		//def scriptTagList = ScriptTag.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		//def scriptTagListCnt = ScriptTag.findAllByGroupsOrGroupsIsNull(groupsInstance)
		def scriptTagList = getScriptTagList(groupsInstance,[name:'name',order:'asc'])
		
		scriptTagInstance.groups = groupsInstance
        if (!scriptTagInstance.save(flush: true)) {
            render(view: "create", model: [scriptTagInstance: scriptTagInstance,scriptTagInstanceList: scriptTagList, scriptTagInstanceTotal: getScriptTagCount(groupsInstance, params), category:params?.category])
            return
        }

        flash.message = message(code: 'default.created.message', args: [message(code: 'scriptTag.label', default: 'ScriptTag'), scriptTagInstance.name])
        redirect(action: "create",  params:[category:params?.category])
    }

    def update(Long id, Long version,Integer max) {
        def scriptTagInstance = ScriptTag.get(id)		
		def groupsInstance = utilityService.getGroup()
		//def scriptTagList = ScriptTag.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		//def scriptTagListCnt = ScriptTag.findAllByGroupsOrGroupsIsNull(groupsInstance)
		def scriptTagList = getScriptTagList(groupsInstance,params)
		
		
		
		params.max = Math.min(max ?: 10, 100)
        if (!scriptTagInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'scriptTag.label', default: 'ScriptTag'), id])
            render(view: "create", model: [scriptTagInstance: scriptTagInstance,scriptTagInstanceList: scriptTagList, scriptTagInstanceTotal: scriptTagListCnt.size()])
            return
        }
		
		def scriptTagBasedOnName = ScriptTag?.findByName(params?.name)
		
		if(scriptTagBasedOnName && (scriptTagBasedOnName?.id !=  scriptTagInstance?.id)){
			flash.message = message(code: 'default.not.unique.message', args: [message(code: 'scriptTag.label', default: 'ScriptTag Name')])
			render(view: "create", model: [scriptTagInstance: scriptTagInstance,scriptTagInstanceList: scriptTagList, scriptTagInstanceTotal: scriptTagListCnt.size()])
			return
		}
		
        if (version != null) {
            if (scriptTagInstance.version > version) {
                scriptTagInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                          [message(code: 'scriptTag.label', default: 'ScriptTag')] as Object[],
                          "Another user has updated this ScriptTag while you were editing")
                render(view: "create", model: [scriptTagInstance: scriptTagInstance,scriptTagInstanceList: scriptTagList, scriptTagInstanceTotal: scriptTagListCnt.size()])
                return
            }
        }

        scriptTagInstance.properties = params

        if (!scriptTagInstance.save(flush: true)) {
			render(view: "create", model: [scriptTagInstance: scriptTagInstance,scriptTagInstanceList: scriptTagList, scriptTagInstanceTotal: scriptTagListCnt.size()])
            return
        }

        flash.message = message(code: 'default.updated.message', args: [message(code: 'scriptTag.label', default: 'ScriptTag'), scriptTagInstance.name])
        redirect(action: "create",  params:[category:params?.category])
    }
	
	def deleteScriptTag(){
		def countVariable = 0
		int deleteCount = 0
		def scriptTagInstance
		if(params?.listCount){ // to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					scriptTagInstance = ScriptTag.get(idDb)
					if (scriptTagInstance) {
						try{
							 scriptTagInstance.delete(flush: true)
							 deleteCount++
						 }
						 catch (DataIntegrityViolationException e) {
							 flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'scriptTag.label', default: 'ScriptTag'),  scriptTagInstance.name])
						 }						 
					}
				}
			}
		}
		
		if(deleteCount  > 1)
		{
			flash.message = "ScriptTags deleted"
		}
		else
		{
			flash.message = message(code: 'default.deleted.message', args: [message(code: 'scriptTag.label', default: 'ScriptTag'),  scriptTagInstance.name])
		}
		redirect(action: "create" ,  params:[category:params?.category])
	}

	def getScriptTag() {
		List scriptTagInstanceList = []
		ScriptTag scriptTag = ScriptTag.findById(params.id)
		if(scriptTag){
			scriptTagInstanceList.add(scriptTag.name)
		}
		render scriptTagInstanceList as JSON
	}
	
	private List getScriptTagList(def groups, def params){
		return  ScriptTag.createCriteria().list(max:params?.max, offset:params?.offset ){
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}

			and{
				eq("category", Utility.getCategory(params?.category))
				
			}
			order params.sort?params.sort:'name', params.order?params.order:'asc'
		}
	}
	
	private int getScriptTagCount(def groups, def params){
		return  ScriptTag.createCriteria().count(){
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}

			and{
				eq("category", Utility.getCategory(params?.category))
				
			}
		}
	}	

}
