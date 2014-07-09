package com.comcast.rdk

import org.springframework.dao.DataIntegrityViolationException
import static com.comcast.rdk.Constants.KEY_ON
import org.springframework.dao.DataIntegrityViolationException
import grails.converters.JSON

class BoxTypeController {

	def utilityService
	
	static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

	def index() {
		redirect(action: "create")
	}

	def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		def boxTypeList = BoxType.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		def boxTypeListCnt = BoxType.findAllByGroupsOrGroupsIsNull(groupsInstance)
		[boxTypeInstance: new BoxType(params), boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt.size()]
	}

	def save() {
		def groupsInstance = utilityService.getGroup()
		def boxTypeList = BoxType.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		def boxTypeListCnt = BoxType.findAllByGroupsOrGroupsIsNull(groupsInstance)
		def boxTypeInstance = new BoxType(params)
		boxTypeInstance.groups = groupsInstance
		
		if (!boxTypeInstance.save(flush: true)) {
			render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt.size()])
			return
		}

		flash.message = message(code: 'default.created.message', args: [message(code: 'boxType.label', default: 'BoxType'), boxTypeInstance.name])
		redirect(action: "create")
	}

	def deleteBoxType(){
		def countVariable = 0
		def boxTypeInstance
		if(params?.listCount){ // to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					boxTypeInstance = BoxType.get(idDb)
					if (boxTypeInstance) {
						try{
							 boxTypeInstance.delete(flush: true)
						  }
						  catch (DataIntegrityViolationException e) {
							  flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'boxType.label', default: 'BoxType'),  boxTypeInstance.name])
						  }						 
					}
					
				}
			}
		}
		redirect(action: "create")
	}

	def getBoxType() {
		List boxTypeInstanceList = []
		BoxType boxType = BoxType.findById(params.id)
		if(boxType){
			boxTypeInstanceList.add(boxType.name)
			boxTypeInstanceList.add(boxType.type)
		}
		render boxTypeInstanceList as JSON
	}

	def update(Long id, Long version, Integer max) {
		def groupsInstance = utilityService.getGroup()
		def boxTypeInstance = BoxType.get(id)
		def boxTypeList = BoxType.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		def boxTypeListCnt = BoxType.findAllByGroupsOrGroupsIsNull(groupsInstance)
		params.max = Math.min(max ?: 10, 100)
		if (!boxTypeInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'boxType.label', default: 'BoxType'), id])
			render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt.size()])
			return
		}
		
		def boxTypeBasedOnName = BoxType?.findByName(params?.name)
		
		if(boxTypeBasedOnName && (boxTypeBasedOnName?.id !=  boxTypeInstance?.id)){
			flash.message = message(code: 'default.not.unique.message', args: [message(code: 'boxType.label', default: 'BoxType Name')])
			render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt.size()])
			return
		}
		
		if (version != null) {
			if (boxTypeInstance.version > version) {
				boxTypeInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						  [message(code: 'boxType.label', default: 'BoxType')] as Object[],
						  "Another user has updated this BoxType while you were editing")
				render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt.size()])
				return
			}
		}

		boxTypeInstance.properties = params

		if (!boxTypeInstance.save(flush: true)) {
			render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt.size()])
			return
		}

		flash.message = message(code: 'default.updated.message', args: [message(code: 'boxType.label', default: 'BoxType'), boxTypeInstance.name])
		redirect(action: "create")
	}


}
