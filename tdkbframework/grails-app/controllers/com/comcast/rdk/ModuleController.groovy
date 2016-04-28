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

import com.google.gson.JsonArray;
import com.google.gson.JsonObject
import grails.converters.JSON
import org.springframework.dao.DataIntegrityViolationException
import org.springframework.util.StringUtils;
import org.apache.shiro.SecurityUtils
import com.comcast.rdk.Category

/**
 * Class to create Modules, Functions and Parameters
 * @author sreejasuma
 *
 */

class ModuleController {

	def utilityService
    def moduleService
	
	def rootPath = null
	
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
		def category = getCategory(params?.category)
		def moduleInstanceList = getModuleList(groupsInstance, params)
		def moduleInstanceListCnt = getModuleCount(groupsInstance, category)
        [moduleInstanceList: moduleInstanceList, moduleInstanceTotal: moduleInstanceListCnt, category:params?.category]
    }

	def crashlog(){
		//def moduleInstanceList = Module.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(), [order: 'asc', sort: 'name'])
		def moduleInstanceList = getModuleList(utilityService.getGroup(), params)
		[moduleInstanceList: moduleInstanceList, category : params?.category]
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
					if(StringUtils.hasText(logfilename)){
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
		redirect(action: "crashlog", params:[category:params?.category])		
	}
	/**
	 * Function transfer the moduleList to the view page
	 *   
	 */
	def logFileNames(){
		def moduleInstanceList = getModuleList(utilityService.getGroup(), params)
		[moduleInstanceList: moduleInstanceList, category: params?.category]
	}

	/**
	 *The Function transfer the stbLogFiles in view page configureStbLogs
	 * @return
	 */
	def getLogList(){
		Module module = Module.findById(params?.moduleid)
		render(template:"configureStbLogs", model:[ stbLogFiles : module?.stbLogFiles])	
	}
	
	/**
	 * The function used to save the current StbLogFiles in database
	 * @return
	 */
	
	def saveLogsFiles(){
		List lst = []
		if(params?.stbLogFiles){
			if((params?.stbLogFiles) instanceof String){
				lst.add(params?.stbLogFiles)
			}
			else{
				params?.stbLogFiles.each{ stblogfilename ->
					if(StringUtils.hasText(stblogfilename)){
						lst.add(stblogfilename)
					}
				}
			}
			Module module = Module.findById(params?.module.id)
			module.stbLogFiles = lst 
			if(module.save(flush:true)){
				flash.message = "Updated Log Files to the Module "+module?.name
			}
			else{
				flash.message = "Error in saving. Please retry "
			}
		}
		redirect(action: "logFileNames", params:[category: params?.category])
	}
	
	
	
    def configuration() {    
        // Redirect to show page without any parameters
		//[category:params?.category]
    }
	
	def setExecutionWaitTime(final int executiontime, final String moduleName){
//		def c = Script.createCriteria()
//		def scriptList = c.list {
//			primitiveTest{
//				module{
//					eq("name", moduleName)
//				}
//			}
//		}
//		scriptList.each{script ->
//			script.executionTime = executiontime
//			script.save(flush:true)
//		}		
	}
	
    /**
     * Create Module, Function and parameter types
     * @return
     */
    def create() { 
		def modules = getModuleList(utilityService.getGroup(), params) 
        [moduleInstance: new Module(params), functionInstance : new Function(params), parameterTypeInstance : new ParameterType(params),category:params?.category, modules:modules]
    }

    def save() {
        def moduleInstance = new Module(params)
		moduleInstance.groups = utilityService.getGroup()
		Category category = getCategory(params?.category)
		def savedEntity = true
		def createdFile = true
		Module.withTransaction { status ->
			if (!moduleInstance.save(flush: true)) {
				savedEntity = false
			}
			if(savedEntity){
				def created = moduleService.createModule(moduleInstance, getRootPath(), category, params?.testGroup)
				if(!created){
					status.setRollbackOnly()
					createdFile = false
				}
			}
		}
		setExecutionWaitTime(moduleInstance.executionTime, moduleInstance.name)
		if(!savedEntity){
			def map = create()
			map.put('moduleInstance', moduleInstance)
			render(view: "create", model: map)
			return
		}
		if(!createdFile){
			flash.message =  "Failed to save ${moduleInstance}. Error occured while creating primitivetest for ${moduleInstance} in fileStore."
			render(view: "create", model: [category: params?.category])
			return
		}
        flash.message = message(code: 'default.created.message', args: [message(code: 'module.label', default: 'Module'), moduleInstance.name])
        redirect(action: "create",  params:[category:params?.category])
    }

    /**
     * Save function corresponding to the selected modules
     * @return
     */
    def saveFunction() {
		Function.withTransaction { status ->
			try{
			def functionInstance = new Function(params)
			if (!functionInstance.save(flush: true)) {
				def map = create()
				map.put('functionInstance', functionInstance)
				flash.message = message(code: 'default.created.message', args: [message(code: 'function.label', default: 'Function'), functionInstance.name])				
				render(view: "create", model: map)
				return
			}
			//try{
				//moduleService.addFunction(params, getRootPath(), getCategory(params?.category))
				//flash.message = message(code: 'default.created.message', args: [message(code: 'function.label', default: 'Function'), functionInstance.name])
			}
			catch(Exception e){
				status.setRollbackOnly()
				e.printStackTrace()
				flash.message = message(code: 'default.not.created.message', args: [message(code: 'function.label', default: 'Function'), functionInstance.name])
			}
		}
        redirect(action: "create", params:[category:params?.category])
    }
    
    /**
     * Save parameter corresponding to the selected modules
     * and functions
     * @return
     */
	def saveParameter() {
		//ParameterType.withTransaction{ status ->
			try{
				def parameterTypeInstance = new ParameterType(params)
				if (!parameterTypeInstance.save(flush: true)) {
					//def map = create()
					
					//map.put('parameterTypeInstance', parameterTypeInstance)
					
					flash.message = message(code: 'default.not.created.message', args: [message(code: 'parameterType.label', default: 'ParameterType'), parameterTypeInstance.name])
					//render(view: "create", model:map)
					render(view: "create", model:['parameterTypeInstance': parameterTypeInstance])
					
					return
				}else{
				
				flash.message = message(code: 'default.created.message', args: [message(code: 'parameterType.label', default: 'ParameterType'), parameterTypeInstance.name])
				
				}
				/*def result = moduleService.addParameter(params, getRootPath(), getCategory(params?.category))
				 if(result.success){
				 flash.message = message(code: 'default.created.message', args: [message(code: 'parameterType.label', default: 'ParameterType'), parameterTypeInstance.name])
				 }
				 else{
				 flash.error = result.message
				 status.setRollbackOnly()
				 }*/

			}catch(Exception e){
				e.printStackTrace()
				println "ERROR "+e.getMessage()
			}
	//	}
		redirect(action: "create", params:[category:params?.category])
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
		println " functionInstance "+ functionInstance
		println "parameteInstanceList--->>> "+parameteInstanceList
        [params : params , moduleInstance : moduleInstance, functionInstanceList : functionInstance, functionInstanceCount : functionInstance.size(), parameteInstanceList : parameteInstanceList, parameteInstanceListTotal : parameteInstanceList.size(), category:moduleInstance?.category]
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
            def path=request.getSession().getServletContext().getRealPath("")
            moduleService.deleteFunctionandParameters(moduleInstance, getCategory(params?.category), path)           
            moduleInstance.delete(flush: true)
            flash.message = message(code: 'default.deleted.message', args: [message(code: 'module.label', default: 'Module'),  moduleInstance.name])
            redirect(action: "list", params:[category:params?.category])
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'module.label', default: 'Module'),  moduleInstance.name])
            redirect(action: "show", id: id, params:[category:params?.category])
        }
    }
    
   
    
    /**
     * Deletes the selected function/s
     */
    def deleteFunction = {
        Function functionInstance
		def unDeletedList = []
		def fnList = []
		def selectedFunctions = params.findAll { it.value == KEY_ON }
        try{
			selectedFunctions.each{
				def key = it.key
				try {
					Function.withTransaction { resultstatus ->
						functionInstance = Function.findById(key)
						fnList.add(functionInstance?.name)
						try{
							if(!functionInstance.delete(flush:true)){
								if(functionInstance?.errors?.allErrors?.size() > 0){
									unDeletedList.add(functionInstance?.name)
								}
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
			flash.message = "${message(code: 'default.not.deleted.message', args: [message(code: 'function.label', default: 'Function'), unDeletedList.toString() ])}"
		}
		//fnList.removeAll(unDeletedList)
		//if(!fnList.isEmpty()){
		//	moduleService.removeFunction(params, getRootPath(), getCategory(params?.category), fnList)
		//}
        redirect(action: "show", id : params?.moduleid, params:[category:params?.category])    
    }
    
    /**
     * Deletes the selected parameter/s
     */
	def deleteParameterType = {
		def parameterTypeInstance
		def unDeletedList = []
		def paramsList = []
		def selectedParameters = params.findAll { it.value == KEY_ON }
		try{
			selectedParameters.each{
				def key = it.key
				try {					
					ParameterType.withTransaction { resultstatus ->
						parameterTypeInstance = ParameterType.findById(key)
						paramsList.add(parameterTypeInstance?.name)
						try{
							if(!parameterTypeInstance.delete(flush:true)){
								if(parameterTypeInstance?.errors?.allErrors?.size() > 0){
									unDeletedList.add(parameterTypeInstance?.name)
								}
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
		paramsList.removeAll(unDeletedList)
		if(unDeletedList.size() > 0){
			flash.message = "${message(code: 'default.not.deleted.message', args: [message(code: 'parameter.label', default: 'Parameter'), unDeletedList.toString() ])}"
		}
		//if(!paramsList.isEmpty()){
		//	moduleService.removeParameters(params, getRootPath(),getCategory(params?.category), paramsList)
		//}
		redirect(action: "show", id : params?.moduleid, params:[category:params?.category])
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
	
	/**
	 * REST method to get the time out values configured for  modules
	 * @param moduleName
	 * @return
	 */
	def getModuleScriptTimeOut(final String moduleName) {
		JsonObject moduleObj = new JsonObject()
		if(moduleName){
			try{
				def moduleInstance= Module.findByName(moduleName)
				if(moduleInstance){
					moduleObj.addProperty("module",moduleInstance?.name?.toString())
					moduleObj.addProperty("timeout",moduleInstance?.executionTime)
				}else{
					moduleObj.addProperty("status", "failure")
					moduleObj.addProperty("remarks", "invalid module name ")
				}
			}
			catch(Exception e){
				println e.getMessage()
				log.error("Invalid module name ")
			}
		}else{
			def mList = Module.findAll()
			JsonArray mArray = new JsonArray()
			mList?.each { module ->
				JsonObject mObject = new JsonObject()
				mObject.addProperty("module",module?.name?.toString())
				mObject.addProperty("timeout",module?.executionTime)
				mArray.add(mObject)
			}
			moduleObj.add("timeoutlist", mArray)
		}

		render moduleObj
	}
	
	private List getModuleList(def groups, def params){
		return  Module.createCriteria().list(max:params.max, offset:params.offset ){
			if(groups != null){
				eq("groups",groups)
			}
			else{
				isNull("groups")
			}
			and{
				eq("category", Utility.getCategory(params?.category))
				
			}
			order params.sort?params.sort:'name', params.order?params.order:'asc'
		}
	}
	
	private int getModuleCount(def groups, def category){
		return  Module.createCriteria().count{
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
	
	private Category getCategory(def category){
		return Category.valueOf(category)
	}
	
	private String getRootPath(){
		return request.getSession().getServletContext().getRealPath(Constants.FILE_SEPARATOR)
	}
	
}
