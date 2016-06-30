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

import org.springframework.dao.DataIntegrityViolationException
import static com.comcast.rdk.Constants.KEY_ON
import com.comcast.rdk.RDKVersions
import java.util.List;
import org.springframework.dao.DataIntegrityViolationException
import grails.converters.JSON

class RDKVersionsController {

   def utilityService
	
	static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

	def index() {
		redirect(action: "create", params:params)
	}

	def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		//def rdkVersionsList = com.comcast.rdk.RDKVersions.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		//def rdkVersionsListCnt = com.comcast.rdk.RDKVersions.findAllByGroupsOrGroupsIsNull(groupsInstance)
		def rdkVersionsList = getRDKVersionList(groupsInstance,params)
		def rdkVersionsListCnt = getRDKVersionCount(groupsInstance, params)
		def rdkVersion = new com.comcast.rdk.RDKVersions(params)
		[ rdkVersionsInstance: rdkVersion,  rdkVersionsInstanceList: rdkVersionsList,  rdkVersionsInstanceTotal:  rdkVersionsListCnt, category:params?.category]
	}

	def save() {
		def groupsInstance = utilityService.getGroup()
		if(params?.buildVersion){
			String build = params?.buildVersion
			if(build.contains(" ")){
				build = build.replaceAll(" ", "")
				params?.buildVersion  = build
			}
		}
		//def rdkVersionsList = com.comcast.rdk.RDKVersions.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		//def rdkVersionsListCnt = com.comcast.rdk.RDKVersions.findAllByGroupsOrGroupsIsNull(groupsInstance)
		def rdkVersionsList = getRDKVersionList(groupsInstance,params)
		def rdkVersionsListCnt = getRDKVersionCount(groupsInstance, params)
		def rdkVersionsInstance = new com.comcast.rdk.RDKVersions(params)
		rdkVersionsInstance.groups = groupsInstance
		
		if (!rdkVersionsInstance.save(flush: true)) {
			render(view: "create", model: [rdkVersionsInstance: rdkVersionsInstance, rdkVersionsInstanceList: rdkVersionsList, rdkVersionsInstanceTotal: rdkVersionsListCnt, category:params?.category])
			return
		}

		flash.message = message(code: 'default.created.message', args: [message(code: 'rdkVersions.label', default: 'RDKVersions'), rdkVersionsInstance.buildVersion])
		redirect(action: "create", params:[category:params?.category])
	}

	def deleteRDKVersions(){
		def countVariable = 0
		int deleteCount = 0
		def rdkVersionsInstance
		if(params?.listCount){ // to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					rdkVersionsInstance = com.comcast.rdk.RDKVersions.get(idDb)
					if (rdkVersionsInstance) {
						
						try{
							rdkVersionsInstance.delete(flush: true)
							deleteCount++
						}
						catch (DataIntegrityViolationException e) {
							flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'rdkVersions.label', default: 'RDKVersions'),  rdkVersionsInstance.buildVersion])
						}
						  
					}
				}
			}
			}
		if(deleteCount  > 1)
		{
			flash.message = "RDKVersions deleted"
		}
		else
		{
			flash.message = message(code: 'default.deleted.message', args: [message(code: 'rdkVersions.label', default: 'RDKVersions'),  rdkVersionsInstance.buildVersion])
		}
		redirect(action: "create", params:[category:params?.category])
	}

	def getRDKVersions() {
		List rdkVersionsInstanceList = []
		com.comcast.rdk.RDKVersions rdkVersions = com.comcast.rdk.RDKVersions.findById(params?.id)
		if(rdkVersions){
			rdkVersionsInstanceList.add(rdkVersions.buildVersion)
		}
		render rdkVersionsInstanceList as JSON
	}

	def update(Long id, Long version, Integer max) {
		def groupsInstance = utilityService.getGroup()
		def rdkVersionsInstance = com.comcast.rdk.RDKVersions.get(id)
		//def rdkVersionsList = com.comcast.rdk.RDKVersions.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		//def rdkVersionsListCnt = com.comcast.rdk.RDKVersions.findAllByGroupsOrGroupsIsNull(groupsInstance)
		params.max = Math.min(max ?: 10, 100)
		def rdkVersionsList = getRDKVersionList(groupsInstance,params)
		def rdkVersionsListCnt = getRDKVersionCount(groupsInstance, params)
		if (!rdkVersionsInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'rdkVersions.label', default: 'RDKVersions'), id])
			render(view: "create", model: [rdkVersionsInstance: rdkVersionsInstance, rdkVersionsInstanceList: rdkVersionsList, rdkVersionsInstanceTotal: rdkVersionsListCnt, category:params?.category])
			return
		}
		
		def buildVersionOnName = com.comcast.rdk.RDKVersions.findByBuildVersion(params?.buildVersion)
		
		if(buildVersionOnName && (buildVersionOnName?.id !=  rdkVersionsInstance?.id)){
			flash.message = message(code: 'default.not.unique.message', args: [message(code: 'rdkVersions.label', default: 'BuildVersion')])
			render(view: "create", model: [rdkVersionsInstance: rdkVersionsInstance, rdkVersionsInstanceList: rdkVersionsList, rdkVersionsInstanceTotal: rdkVersionsListCnt, category:params?.category])
			return
		}
		
		if (version != null) {
			if (rdkVersionsInstance.version > version) {
				rdkVersionsInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						  [message(code: 'rdkVersions.label', default: 'RDKVersions')] as Object[],
						  "Another user has updated this RDKVersions while you were editing")
				render(view: "create", model: [rdkVersionsInstance: rdkVersionsInstance, rdkVersionsInstanceList: rdkVersionsList, rdkVersionsInstanceTotal: rdkVersionsListCnt, category:params?.category])
				return
			}
		}

		if(params?.buildVersion){
			String build = params?.buildVersion
			if(build.contains(" ")){
				build = build.replaceAll(" ", "")
				params?.buildVersion  = build
			}
		}
		
		rdkVersionsInstance.properties = params

		if (!rdkVersionsInstance.save(flush: true)) {
			render(view: "create", model: [rdkVersionsInstance: rdkVersionsInstance, rdkVersionsInstanceList: rdkVersionsList, rdkVersionsInstanceTotal: rdkVersionsListCnt, category:params?.category])
			return
		}

		flash.message = message(code: 'default.updated.message', args: [message(code: 'rdkVersions.label', default: 'RDKVersions'), rdkVersionsInstance.buildVersion])
		redirect(action: "create", params:[category:params?.category])
	}
	
	private List getRDKVersionList(def groups, def params){
		return  com.comcast.rdk.RDKVersions.createCriteria().list(max:params?.max, offset:params?.offset ){
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}

			and{
				eq("category", Utility.getCategory(params?.category))
				
			}
			order 'buildVersion', params.order?params.order:'asc'
		}
	}
	
	private int getRDKVersionCount(def groups, def params){
		return  com.comcast.rdk.RDKVersions.createCriteria().count(){
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
