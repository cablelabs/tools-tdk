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


import static com.comcast.rdk.Constants.*
import org.springframework.dao.DataIntegrityViolationException
//import com.sun.xml.internal.bind.v2.schemagen.xmlschema.List;
import grails.converters.JSON
import org.apache.shiro.SecurityUtils
/**
 * Controller class for Script and ScriptGroup domain.
 * @author sreejasuma
 */

class ScriptGroupController {

	static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

	def utilityService
	
    /**
     * Injecting scriptgroupService
     */
	def scriptgroupService
    
	def index() {
		redirect(action: "list", params: params)
	}
	
    /**
     * Lists Script and Script Groups in a tree in list.gsp
     * @return
     */
	def list = {	
		def groupsInstance = utilityService.getGroup()
		def scriptInstanceList = Script.findAllByGroupsOrGroupsIsNull(groupsInstance)
		def scriptGroupMap = createScriptList(scriptInstanceList);
		def scriptGrpInstanceList = ScriptGroup.findAllByGroupsOrGroupsIsNull(groupsInstance)
		[scriptInstanceList: scriptInstanceList, scriptGroupInstanceList: scriptGrpInstanceList, scriptGroupInstanceTotal: scriptGrpInstanceList.size(),error: params.error, scriptId: params.scriptId, scriptGroupId:params.scriptGroupId, scriptInstanceTotal: scriptInstanceList.size(), scriptGroupMap:scriptGroupMap]
	}
	
	/**
	 * Method to create the filtered script list based on module
	 * @param scriptInstanceList
	 * @return
	 */
	private Map createScriptList(def scriptInstanceList ){
		List scriptList = []
		Map scriptGroupMap = [:]
		scriptInstanceList.each { script ->
			PrimitiveTest primitiveTest = script.getPrimitiveTest()
			if(primitiveTest){
				String moduleName = primitiveTest.getModule().getName();
				List subList = scriptGroupMap.get(moduleName);
				if(subList == null){
					subList = []
					scriptGroupMap.put(moduleName, subList);
				}
				subList.add(script)
			}
		}
		
		return scriptGroupMap
	}

    /**
     * Create ScriptGroup
     * @return
     */
	def create() {
		[scriptGroupInstance: new ScriptGroup(params)]
	}

    /**
     * Save ScriptGroup
     * @return
     */
	def save() {
		def scriptGroupInstance = new ScriptGroup(params)
        if(ScriptGroup.findByName(params?.name)){
            flash.message = "TestSuite name is already in use. Please use a different name."
            redirect(action: "list")
            return
        }
        else if(!(params?.scripts)){
            flash.message = "Select scripts to create a test suite."
            redirect(action: "list")
            return
        }
		scriptGroupInstance.groups = utilityService.getGroup()
		if (!scriptGroupInstance.save(flush: true)) {
			return
		}
		flash.message = message(code: 'default.created.message', args: [
			message(code: 'scriptGroup.label', default: 'Test Suite'),
			scriptGroupInstance.name
		])
		redirect(action: "list")
	}

	/**
	 * Show ScriptGroup
	 * @return
	 */
	def show(Long id) {
		def scriptGroupInstance = ScriptGroup.get(id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				id
			])
			redirect(action: "list")
			return
		}

		[scriptGroupInstance: scriptGroupInstance]
	}

    /**
     * Edit ScriptGroup
     * @return
     */
	def edit(Long id) {
		def scriptGroupInstance = ScriptGroup.get(id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			])
			redirect(action: "list")
			return
		}       
		[scriptGroupInstance: scriptGroupInstance]
	}

    /**
     * Update ScriptGroup
     * @return
     */
	def update(Long id, Long version) {
		def scriptGroupInstance = ScriptGroup.get(id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			])
			redirect(action: "list",params: [scriptGroupId: params.id])
			return
		}

		if (version != null) {
			if (scriptGroupInstance.version > version) {
				scriptGroupInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						[
							message(code: 'scriptGroup.label', default: 'Test Suite')] as Object[],
						"Another user has updated this ScriptGroup while you were editing")
				render(view: "edit", model: [scriptGroupInstance: scriptGroupInstance])
				return
			}
		}

		scriptGroupInstance.properties = params

		if (!scriptGroupInstance.save(flush: true)) {
			flash.message = "TestSuite name is already in use. Please use a different name."
            redirect(action: "list",params: [scriptGroupId: params.id])
			return
		}

		flash.message = message(code: 'default.updated.message', args: [
			message(code: 'scriptGroup.label', default: 'Test Suite'),
			scriptGroupInstance.name
		])
		redirect(action: "list", params: [scriptGroupId: params.id])
	}

    /**
     * Delete ScriptGroup
     * @return
     */
	def deleteScriptGrp() {
		def scriptGroupInstance = ScriptGroup.findById(params?.id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
			return
		}

		try {
			scriptGroupInstance.delete(flush: true)
			flash.message = message(code: 'default.deleted.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
		}
		catch (DataIntegrityViolationException e) {
			flash.message = message(code: 'default.not.deleted.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
		}
	}

    /**
     * Delete ScriptGroup
     * @return
     */
	def delete() {
		def scriptGroupInstance = ScriptGroup.findById(params?.id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
			return
		}

		try {
			scriptGroupInstance.delete(flush: true)
			flash.message = message(code: 'default.deleted.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
		}
		catch (DataIntegrityViolationException e) {
			flash.message = message(code: 'default.not.deleted.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
		}
	}

    /**
     * Create Script
     * @return
     */
	def createScript() {
		def primitiveTestList = PrimitiveTest.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(), [order: 'asc', sort: 'name'])//PrimitiveTest.list([order: 'asc', sort: 'name'])		
		[ primitiveTestList : primitiveTestList]
	}

    /**
     * Edit Script
     * @return
     */
	def editScript() {
		
		if(params.id){
			def script = Script.get(params.id)
			[script : script , flag : params?.flag]
		}
		
	}

    /**
     * Delete Script
     * @return
     */
	def deleteScript(){
        
        /** 
         * Delete script after checking whether is script is executing on a device
         * or the script is present in a script group which is selected to execute
         */
		def script = Script.findById(params?.id)
        if (!script) {
            flash.message = "Script not found"
            render("Not found")
        }
        boolean scriptInUse = scriptgroupService.checkScriptStatus(script)
        
        if(scriptInUse){
            flash.message = "Can't Delete. Scripts may be used in Script Group"
            render("Exception")
        }
        else{    		
    		try {
    			script.delete(flush: true)
    			flash.message = "Deleted the script '${script.name}'"
    			render("success")
    		}
    		catch (DataIntegrityViolationException e) {
    			flash.message = "Can't Delete. Scripts may be used in Script Group"
    			render("Exception")
    		}
        }        
	}
	
    /**
     * Save Script
     * @return
     */
    def saveScript() {
		
        def error = ''
        if(Script.findByName(params?.name)){
			render("Duplicate Script Name not allowed. Try Again.")
        }
        else{
            def scriptInstance = new Script(params)
            scriptInstance.name = params?.name
            scriptInstance.primitiveTest = PrimitiveTest.findById(params?.ptest)
            scriptInstance.scriptContent = params?.scriptArea
            scriptInstance.synopsis = params.synopsis
			scriptInstance.groups = utilityService.getGroup()
			scriptInstance.executionTime = params?.executionTime
						
			def boxTypes = params?.boxTypes
			def boxTypesList = []
			boxTypesList = scriptgroupService.createBoxTypeList(boxTypes)

            if (!scriptInstance.save(flush: true)) {                
                log.error "Error saving Script instance : ${scriptInstance.errors}"
				render("Error in saving Script. Try Again." )             
            }
            else{
                scriptgroupService.saveToDefaultGroup(scriptInstance, boxTypesList)
				render(message(code: 'default.created.message', args: [
                    message(code: 'script.label', default: 'Script'),
                    scriptInstance.name
                ]))
            }
        }
    }
    
	/**
	 * Update Script
	 * @return
	 */
	def updateScript(Long id, Long version) {

		def scriptInstance = Script.get(id)
		if (!scriptInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'script.label', default: 'Script'),
				id
			])
			redirect(action: "list")
			return
		}

		if (version != null) {
			if (scriptInstance.version > version) {
				scriptInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						[
							message(code: 'script.label', default: 'Script')] as Object[],
						"Another user has updated this Script while you were editing")
				return
			}
		}
		def boxTypes = params.boxTypes
		def boxTypesList = []
		scriptInstance.name = params.name
		scriptInstance.scriptContent = params.scriptArea
		scriptInstance.synopsis = params.synopsis
		scriptInstance.primitiveTest = PrimitiveTest.findById(params.ptest)
		scriptInstance.executionTime = Integer.parseInt(params?.executionTime)
	
		if (!scriptInstance.save(flush: true)) {
			log.error "Error saving Script instance : ${scriptInstance.errors}"
			return
		}

		if(boxTypes){
			boxTypesList = scriptgroupService.createBoxTypeList(boxTypes)
			scriptgroupService.removeScriptsFromBoxSuites(scriptInstance)
			scriptgroupService.saveToDefaultGroup(scriptInstance, boxTypesList)
		}

		scriptInstance.properties = params

		flash.message = message(code: 'default.updated.message', args: [
			message(code: 'script.label', default: 'Script'),
			scriptInstance.name
		])

		redirect(action: "list", params: [scriptId: params.id])
	}	
    
    /**
     * Get Module name, version and testGroup
     * through ajax call
     * @return
     */
    def getModuleName(){
        List moduleDetails = []
        PrimitiveTest primitiveTest = PrimitiveTest.findById(params?.primId)
        moduleDetails.add( primitiveTest.module.name.toString().trim() )
        moduleDetails.add( primitiveTest.module.rdkVersion.toLowerCase().trim() )
        moduleDetails.add( primitiveTest.module.testGroup.toString().trim() )
		moduleDetails.add( primitiveTest.module.executionTime.toString().trim() )
        render moduleDetails as JSON
    }
    
    /**
     * Show streaming details in a popup in script page
     * @param max
     * @return
     */
    def showStreamDetails(){       
		def streamingDetailsList = StreamingDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
		[streamingDetailsInstanceList: streamingDetailsList, streamingDetailsInstanceTotal: streamingDetailsList.size()]
       // [streamingDetailsInstanceList: StreamingDetails.list(), streamingDetailsInstanceTotal: StreamingDetails.count()]
    }
    
    /**
     * Get the list of scripts based on the scriptName.
     * @return
     */
    def searchScript(){
        def scripts = Script.findAll("from Script as b where b.name like '%${params?.searchName}%'")
        render(template: "searchList", model: [scriptList : scripts])
    }
    
    /**
     * Get the list of scripts based on the scriptName, primitiveTest and selected box types.
     * @return
     */
    def advsearchScript(){
        def scriptList = scriptgroupService.getAdvancedSearchResult(params?.searchName,params?.primtest,params?.selboxTypes)             
        render(template: "searchList", model: [scriptList : scriptList])
    }
    
    /**
     * Adds a new scriptGroup based on the selection of scripts from the 
     * list of scripts obtained after performing a search
     * @return
     */
    def addScriptGroupfromSeachList(){    

        def selectedScripts = params.findAll { it.value == KEY_ON }
        if(params?.suiteRadioGroup.equals( KEY_EXISTING )){
            ScriptGroup scriptGroup = ScriptGroup.findById(params?.testsuite)
            if(scriptGroup){
                def scriptInstance
                selectedScripts.each{
                    Script script = Script.findById(it.key)                    
                    scriptInstance = scriptGroup.scripts.find { it.id == script.id }
                    if(!scriptInstance){
                        scriptGroup.addToScripts(script)
                    }                    
                }
            }
        }
        else{
            def scriptGroupInstance = new ScriptGroup()
            
            if(ScriptGroup.findByName(params?.newSuiteName)){
                flash.message =  message(code: 'script.add.group')              
            }
            else if(!(selectedScripts)){
                flash.message = message(code: 'script.empty.select')               
            }
            else{
                scriptGroupInstance.name = params?.newSuiteName
                selectedScripts.each{
                    Script script = Script.findById(it.key)
                    scriptGroupInstance.addToScripts(script)
                }
            }
            if (!scriptGroupInstance.save(flush: true)) {
                flash.message = message(code: 'default.created.message', args: [
                message(code: 'scriptGroup.label', default: 'Test Suite'),
                scriptGroupInstance.name])               
            }
        } 
        redirect(action: "list")
    }
	
	
	
	/**
	 * Method to check whether script with same name exist or not. If yes returns the id of script
	 * @return
	 */
	def fetchScript(){

		List scriptInstanceList = []
		Script scriptInstance = Script.findByName(params.scriptName)
		if(scriptInstance){
			scriptInstanceList.add(scriptInstance.id)
		}
		render scriptInstanceList as JSON
	}
	
    
}