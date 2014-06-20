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
import grails.converters.JSON
import org.springframework.dao.DataIntegrityViolationException
import org.apache.shiro.SecurityUtils

/**
 * Class to create Modules, Functions and Parameters
 * @author sreejasuma
 *
 */

class ModuleController {

	def utilityService
	
    static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

    def index() {
        redirect(action: "list", params: params)
    }
	
    /**
     * List modules
     * @param max
     * @return
     */
    def list(Integer max) {
        params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		def moduleInstanceList = Module.findAllByGroupsOrGroupsIsNull(groupsInstance, params)
		def moduleInstanceListCnt = Module.findAllByGroupsOrGroupsIsNull(groupsInstance)
        [moduleInstanceList: moduleInstanceList, moduleInstanceTotal: moduleInstanceListCnt.size()]
    }

	def crashlog(){
		def moduleInstanceList = Module.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(), [order: 'asc', sort: 'name'])
		[moduleInstanceList: moduleInstanceList]
	}
	
	/**
	 * Method to get the file list based on module
	 * @param max
	 * @return
	 */
	def getFileList(){
		Module module = Module.findById(params?.moduleid)
		render(template:"crashfilelist", model:[ crashfiles : module?.logFileNames])		
	}
	
	def saveCrashLogs(){		
		List lst = []
		if(params?.logFileNames){
			if((params?.logFileNames) instanceof String){
				lst.add(params?.logFileNames)
			}
			else{
				(params?.logFileNames).each{ logfilename ->
					if(!(logfilename.isEmpty())){
						lst.add(logfilename)
					}
				}				
			}
			Module module = Module.findById(params?.module.id)			
			module.logFileNames = lst
			if(module.save(flush:true)){
				flash.message = "Updated Log Files to the Module "+module?.name
			}
			else{
				flash.message = "Error in saving. Please retry "
			}			
		}				
		redirect(action: "crashlog")		
	}
	
    def configuration() {    
        // Redirect to show page without any parameters
    }
	
	def setExecutionWaitTime(final int executiontime, final String moduleName){
		def c = Script.createCriteria()
		def scriptList = c.list {
			primitiveTest{
				module{
					eq("name", moduleName)
				}
			}
		}
		scriptList.each{script ->
			script.executionTime = executiontime
			script.save(flush:true)
		}		
	}
	
    /**
     * Create Module, Function and parameter types
     * @return
     */
    def create() {        
        [moduleInstance: new Module(params), functionInstance : new Function(params), parameterTypeInstance : new ParameterType(params)]
    }

    def save() {
        def moduleInstance = new Module(params)
		moduleInstance.groups = utilityService.getGroup()
        if (!moduleInstance.save(flush: true)) {
            render(view: "create", model: [moduleInstance: moduleInstance])
            return
        }
		setExecutionWaitTime(moduleInstance.executionTime, moduleInstance.name)
        flash.message = message(code: 'default.created.message', args: [message(code: 'module.label', default: 'Module'), moduleInstance.name])
        redirect(action: "create")
    }

    /**
     * Save function corresponding to the selected modules
     * @return
     */
    def saveFunction() {
        def functionInstance = new Function(params)
        if (!functionInstance.save(flush: true)) {
            render(view: "create", model: [functionInstance: functionInstance])
            return
        }
        flash.message = message(code: 'default.created.message', args: [message(code: 'function.label', default: 'Function'), functionInstance.name])
        redirect(action: "create")
    }
    
    /**
     * Save parameter corresponding to the selected modules
     * and functions
     * @return
     */
    def saveParameter() {
        def parameterTypeInstance = new ParameterType(params)
        if (!parameterTypeInstance.save(flush: true)) {
            render(view: "create", model: [parameterTypeInstance: parameterTypeInstance])
            return
        }
        flash.message = message(code: 'default.created.message', args: [message(code: 'parameterType.label', default: 'ParameterType'), parameterTypeInstance.name])
        redirect(action: "create")
    }
	
	def updateTimeOut(){
		try{			
			Module moduleInstance = Module.findById(params?.moduleId)
			moduleInstance.executionTime = Integer.parseInt(params?.timeout)
			if(moduleInstance.save(flush:true)){
				setExecutionWaitTime(moduleInstance.executionTime, moduleInstance.name)
				render "Updated TimeOut"
			}
			else{
				render "TimeOut not updated. Try Again!!"
			}			
		}catch(Exception e){
		}		
	}
	

    /**
     * Show Modules, Functions and Parameters
     * @param id
     * @return
     */
    def show(Long id) {                
        def moduleInstance = Module.get(id)
        def functionInstance
        def parameterInstance
        def parameteInstanceList = []
        if (!moduleInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'module.label', default: 'Module'), id])
            redirect(action: "list")
            return
        }
        else{
            functionInstance = Function.findAllByModule( moduleInstance )  
            def parameterTypeTnstance
            functionInstance.each{ fn ->
                parameterInstance = ParameterType.findAllByFunction(fn)
                parameterInstance.each{ parameter ->                    
                    parameterTypeTnstance = ParameterType.get( parameter.id )
                    parameteInstanceList.add(parameterTypeTnstance)
                }                
            }                 
        }
        [params : params , moduleInstance : moduleInstance, functionInstanceList : functionInstance, functionInstanceCount : functionInstance.size(), parameteInstanceList : parameteInstanceList, parameteInstanceListTotal : parameteInstanceList.size()]
    }


    /**
     * TODO : If required
     * @param id
     * @return
     */
    def edit(Long id) {
        def moduleInstance = Module.get(id)
        if (!moduleInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'module.label', default: 'Module'), id])
            redirect(action: "list")
            return
        }

        [moduleInstance: moduleInstance]
    }

    /**
     * TODO : If required
     * @param id
     * @return
     */
    def update(Long id, Long version) {
        def moduleInstance = Module.get(id)
        if (!moduleInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'module.label', default: 'Module'), id])
            redirect(action: "list")
            return
        }

        if (version != null) {
            if (moduleInstance.version > version) {
                moduleInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                          [message(code: 'module.label', default: 'Module')] as Object[],
                          "Another user has updated this Module while you were editing")
                render(view: "edit", model: [moduleInstance: moduleInstance])
                return
            }
        }

        moduleInstance.properties = params

        if (!moduleInstance.save(flush: true)) {
            render(view: "edit", model: [moduleInstance: moduleInstance])
            return
        }

        flash.message = message(code: 'default.updated.message', args: [message(code: 'module.label', default: 'Module'), moduleInstance.name])
        redirect(action: "show", id: moduleInstance.id)
    }

    /**
     * Deletes the module and the corresponding
     * functions and parameters
     * @param id
     * @return
     */
    def delete(Long id) {
        def moduleInstance = Module.get(id)
        if (!moduleInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'module.label', default: 'Module'),  moduleInstance.name])
            redirect(action: "list")
            return
        }
        try {                       
            deleteFunctionandParameters(moduleInstance)           
            moduleInstance.delete(flush: true)
            flash.message = message(code: 'default.deleted.message', args: [message(code: 'module.label', default: 'Module'),  moduleInstance.name])
            redirect(action: "list")
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'module.label', default: 'Module'),  moduleInstance.name])
            redirect(action: "show", id: id)
        }
    }
    
    /**
     * Deletes functions of the given module
     * @param moduleInstance
     * @return
     */
    def deleteFunctionandParameters(final Module moduleInstance){
        def functionInstance = Function.findAllByModule(moduleInstance)
        functionInstance.each{ fnInstance ->
            deleteParameters(fnInstance)
            fnInstance.delete(flush: true)
        }
    }
    
    /**
     * Deletes parameters of the given function
     * @param function
     * @return
     */
    def deleteParameters(final Function function){
        def parameterList = ParameterType.findAllByFunction(function)
        parameterList?.each { parameters ->
            try{
                def parameterInstanceList = Parameter.findByParameterType(parameters)
                parameterInstanceList?.each { parameterType ->
                    parameterType.delete()
                }
                parameters.delete()
            }
            catch(Exception ex){
                log.error(parameters.errors)
            }
        }
    }
    
    
    /**
     * Deletes the selected function/s
     */
    def deleteFunction = {
        Function functionInstance
		def unDeletedList = []
		def selectedFunctions = params.findAll { it.value == KEY_ON }
        try{
			selectedFunctions.each{
				def key = it.key
				try {
					Function.withTransaction { resultstatus ->
						functionInstance = Function.findById(key)
						try{
							if(!functionInstance.delete(flush:true)){
								unDeletedList.add(functionInstance?.name)
							}
						}
						catch (org.springframework.dao.DataIntegrityViolationException e) {
							unDeletedList.add(functionInstance?.name)
						}						
						resultstatus.flush()
					}
				} catch (Exception e) {
					unDeletedList.add(functionInstance?.name)
				}
			}        
			flash.message = "Function/s deleted"
        }      
        catch (Exception e) {
            log.trace e.printStackTrace()
            flash.message = "${message(code: 'default.not.deleted.message', args: [message(code: 'function.label', default: 'Function'), unDeletedList.toString() ])}"
        }
		if(unDeletedList.size() > 0){
			flash.message = "${message(code: 'default.not.deleted.message', args: [message(code: 'parameter.label', default: 'Parameter'), unDeletedList.toString() ])}"
		}
        redirect(action: "show", id : params?.moduleid)    
    }
    
    /**
     * Deletes the selected parameter/s
     */
	def deleteParameterType = {
		def parameterTypeInstance
		def unDeletedList = []
		def selectedParameters = params.findAll { it.value == KEY_ON }
		try{
			selectedParameters.each{
				def key = it.key
				try {					
					ParameterType.withTransaction { resultstatus ->
						parameterTypeInstance = ParameterType.findById(key)
						try{
							if(!parameterTypeInstance.delete(flush:true)){
								unDeletedList.add(parameterTypeInstance?.name)
							}
						}
						catch (org.springframework.dao.DataIntegrityViolationException e) {
							unDeletedList.add(parameterTypeInstance?.name)
						}
						
						resultstatus.flush()
					}
				} catch (Exception e) {
					unDeletedList.add(parameterTypeInstance?.name)
				}
			}
			flash.message = "Parameter/s deleted"
		}

		catch (Exception e) {
			flash.message = "${message(code: 'default.not.deleted.message', args: [message(code: 'parameter.label', default: 'Parameter'), parameterTypeInstance?.name])}"
		}

		if(unDeletedList.size() > 0){
			flash.message = "${message(code: 'default.not.deleted.message', args: [message(code: 'parameter.label', default: 'Parameter'), unDeletedList.toString() ])}"
		}

		redirect(action: "show", id : params?.moduleid)
	}
    
    /**
     * Get the functions under the specific modules 
     * @return
     */
    def getFunctions() {
        if(! params.moduleId) {
            render "No module id found"
            return
        }
        
        def module = Module.get(params.moduleId as Long)
        
        if(! module) {
            render "No module found with id : ${params.moduleId}"
            return
        }
        
        def functions = Function.findAllByModule(module)
        render functions as JSON
    }
}
