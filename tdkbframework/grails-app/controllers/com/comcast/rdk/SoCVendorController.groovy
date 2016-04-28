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

import org.grails.datastore.gorm.finders.MethodExpression.IsNull;
import org.springframework.dao.DataIntegrityViolationException
import grails.converters.JSON

import com.comcast.rdk.Category 


class SoCVendorController {

	def utilityService
	
    static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

    def index() {
        redirect(action: "create", params: params)
    }
	
    def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		def category = Utility.getCategory(params?.category)
		def soCVendorList = getVendorList(groupsInstance, params) 
		def soCVendorListCnt = getVendorListCount(groupsInstance, category)
		[soCVendorInstance: new SoCVendor(params) ,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt, category:params?.category]
    }

    def save(Integer max) {
        def soCVendorInstance = new SoCVendor(params)
		params.max = Math.min(max ?: 10, 100)		
		def groupsInstance = utilityService.getGroup()
		def category = Utility.getCategory(params?.category)
		def soCVendorList = getVendorList(groupsInstance, [name:'name',order:'asc']) 
		def soCVendorListCnt =  getVendorListCount(groupsInstance, category)
		soCVendorInstance.groups = groupsInstance
        if (!soCVendorInstance.save(flush: true)) {
            render(view: "create", model: [soCVendorInstance: soCVendorInstance,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt], category:params?.category)
            return
        }

        flash.message = message(code: 'default.created.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor'), soCVendorInstance.name])
        redirect(action: "create", params:[category:params?.category])
    }

    def update(Long id, Long version,Integer max) {
        def soCVendorInstance = SoCVendor.get(id)		
		def groupsInstance = utilityService.getGroup()
		def category = Utility.getCategory(params?.category)
		def soCVendorList = getVendorList(groupsInstance, params) 
		def soCVendorListCnt =  getVendorListCount(groupsInstance, category)
		params.max = Math.min(max ?: 10, 100)
        if (!soCVendorInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor'), id])
            render(view: "create", model: [soCVendorInstance: soCVendorInstance,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt, category:params?.category])
            return
        }
		
		def socVendorBasedOnName = SoCVendor?.findByName(params?.name)
		
		if(socVendorBasedOnName && (socVendorBasedOnName?.id !=  soCVendorInstance?.id)){
			flash.message = message(code: 'default.not.unique.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor Name')])
			render(view: "create", model: [soCVendorInstance: soCVendorInstance,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt, category:params?.category])
			return
		}
		
        if (version != null) {
            if (soCVendorInstance.version > version) {
                soCVendorInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                          [message(code: 'soCVendor.label', default: 'SoCVendor')] as Object[],
                          "Another user has updated this SoCVendor while you were editing")
                render(view: "create", model: [soCVendorInstance: soCVendorInstance,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt, category:params?.category])
                return
            }
        }

        soCVendorInstance.properties = params

        if (!soCVendorInstance.save(flush: true)) {
			render(view: "create", model: [soCVendorInstance: soCVendorInstance,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt, category:params?.category])
            return
        }

        flash.message = message(code: 'default.updated.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor'), soCVendorInstance.name])
        redirect(action: "create",params:[category:params?.category])
    }
	
	def deleteSoCVendor(){
		def countVariable = 0
		int deleteCount = 0
		def soCVendorInstance
		if(params?.listCount){ // to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					soCVendorInstance = SoCVendor.get(idDb)
					if (soCVendorInstance) {
						try{
							 soCVendorInstance.delete(flush: true)
							 deleteCount++
						 }
						 catch (DataIntegrityViolationException e) {
							 flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor'),  soCVendorInstance.name])
						 }						 
					}
				}
			}
		}
		
		if(deleteCount  > 1)
		{
			flash.message = "SoCVendors deleted"
		}
		else
		{
			flash.message = message(code: 'default.deleted.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor'),  soCVendorInstance.name])
		}
		redirect(action: "create", params:[category:params?.category])
	}

	def getSoCVendor() {
		List soCVendorInstanceList = []
		SoCVendor soCVendor = SoCVendor.findById(params.id)
		if(soCVendor){
			soCVendorInstanceList.add(soCVendor.name)
		}
		render soCVendorInstanceList as JSON
	}
	
	private List getVendorList(def groups, def params){
		return  SoCVendor.createCriteria().list(max:params?.max, offset:params?.offset){
			if(groups != null){
				eq("groups",groups)
			}
			else{
				isNull("groups")
			}
			and{
				eq("category", Utility.getCategory(params?.category))
			}
			order params.name?params.name:'name',params.order?params.order:'asc'
		} 
	} 
	
	private int getVendorListCount(def groups, def category){
		return  SoCVendor.createCriteria().count{
			if(groups != null){
				eq("groups",groups)
			}
			else{
				isNull("groups")
			}
			and{
				eq("category", category)
			}
		}
	}
}
