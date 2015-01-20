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
import groovy.xml.MarkupBuilder
import org.apache.shiro.SecurityUtils

/**
 * Controller class for Script and ScriptGroup domain.
 * @author sreejasuma
 */

class ScriptGroupController {

	static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

	def utilityService
	
	def scriptService
	
	def primitiveService
	
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
		def requestGetRealPath = request.getRealPath("/")
		def scriptNameList = scriptService.getScriptNameList(requestGetRealPath)
		def scriptGroupMap = scriptService.getScriptsMap(requestGetRealPath)
		scriptGroupMap?.keySet()?.sort{a,b -> a <=> b}
		def scriptGrpInstanceList = ScriptGroup.findAllByGroupsOrGroupsIsNull(groupsInstance)
		[scriptGroupInstanceList: scriptGrpInstanceList, scriptGroupInstanceTotal: scriptGrpInstanceList.size(),error: params.error, scriptId: params.scriptId, scriptGroupId:params.scriptGroupId, scriptInstanceTotal: scriptNameList.size(), scriptGroupMap:scriptGroupMap]
	}
	
	
	/**
	 * Method to create the filtered script list based on module
	 * @param scriptInstanceList
	 * @return
	 */
	private Map getScriptList(){
		List scriptList = []
		Map scriptGroupMap = [:]
		List dirList = [Constants.COMPONENT,Constants.INTEGRATION]
		dirList.each{ directory ->
		File scriptsDir = new File( "${request.getRealPath('/')}//fileStore//testscripts//"+directory+"//")
		if(scriptsDir.exists()){
			def modules = scriptsDir.listFiles()
			modules.each { module ->
				File [] files = module.listFiles(new FilenameFilter() {
					@Override
					public boolean accept(File dir, String name) {
						return name.endsWith(".py");
					}
				});
			
			def list = []
			
			files.each { file ->
				String name = file?.name?.replace(".py", "")
				list.add(name)
			}
				
				scriptGroupMap.put(module?.name, list)
			}
		}
		}
		
		
		return scriptGroupMap
	}
	

	
	def getScriptNameFileList(){
		List scriptList = []
		Map scriptGroupMap = [:]
		List dirList = [Constants.COMPONENT,Constants.INTEGRATION]
		dirList.each{ directory ->
		File scriptsDir = new File( "${request.getRealPath('/')}//fileStore//testscripts//"+directory+"//")
		if(scriptsDir.exists()){
			def modules = scriptsDir.listFiles()
			modules.each { module ->
				
				File [] files = module.listFiles(new FilenameFilter() {
					@Override
					public boolean accept(File dir, String name) {
						return name.endsWith(".py");
					}
				});
			
			
			files.each { file ->
				String name = file?.name?.replace(".py", "")
				def sFile = ScriptFile.findByScriptNameAndModuleName(name,module.getName())
				if(sFile == null){
					sFile = new ScriptFile()
					sFile.setModuleName(module?.getName())
					sFile.setScriptName(name)
					sFile.save(flush:true)
				}
				scriptList.add(sFile)
			}
				
			}
		}
		}
		
		return scriptList
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
		
		def scriptNameList = scriptService.getScriptNameFileList(getRealPath())
		def sList = scriptNameList.clone()
		sList?.sort{a,b -> a?.scriptName <=> b?.scriptName}
		
		[scriptGroupInstance: new ScriptGroup(params),scriptInstanceList:sList]
	}

	
	/**
	 * Method to create script group.
	 * @return
	 */
	def createScriptGrp(){
		def errorList= []
		def scriptGroupInstance = new ScriptGroup(params)
		if(ScriptGroup.findByName(params?.name)){
			flash.message = "TestSuite name is already in use. Please use a different name."
			errorList.add("TestSuite name is already in use. Please use a different name.")
			render errorList as JSON
			return
		}
		else if(!(params?.idList)){
			flash.message = "Select scripts to create a test suite."
			errorList.add("Select scripts to create a test suite.")
			render errorList as JSON
			return
		}
		
		def idList = params?.idList
			idList = idList.replaceAll("sgscript-","")
			idList = idList.replaceAll("end","")
			
			StringTokenizer st = new StringTokenizer(idList,",")
		while(st.hasMoreTokens()){
			String token = st.nextToken()

			if(token && token.size()>0){
				ScriptFile sctFile = ScriptFile.findById(token)
				if(sctFile && !scriptGroupInstance?.scriptList?.contains(sctFile)){
					scriptGroupInstance.addToScriptList(sctFile)
				}

			}
		}
			
			scriptGroupInstance.groups = utilityService.getGroup()
			if (!scriptGroupInstance.save(flush: true)) {ex
				errorList.add("Error in saving script group")
				render errorList as JSON
				render errorList as JSON
				return
			}
			flash.message = message(code: 'default.created.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			])
			errorList.add(message(code: 'default.created.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			]))
			render errorList as JSON 
	}
	
	def updateScriptGrp(){
		def errorList= []
		def scriptGroupInstance = ScriptGroup.get(params.id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			])
			errorList.add(message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			]))
			render errorList as JSON
		}
		try {
			if (params.version != null) {
				def a = scriptGroupInstance.version
				def b = params.version
				long vers1 = 0
				long vers2 = 0
				if( a instanceof String){
					vers1 = Long.parseLong(a)
				}
				
				if( b instanceof String){
					vers2 = Long.parseLong(b)
				}
				
				if (vers1 > vers2) {
					scriptGroupInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
							[
							 message(code: 'scriptGroup.label', default: 'Test Suite')] as Object[],
							"Another user has updated this ScriptGroup while you were editing")
							render(view: "edit", model: [scriptGroupInstance: scriptGroupInstance])
							
							errorList.add("Another user has updated this ScriptGroup while you were editing");
							render errorList as JSON
							return
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

		
		if(!(params?.idList)){
			flash.message = "Select scripts to update a test suite."
			errorList.add("Select scripts to update a test suite.");
			render errorList as JSON
			return
		}
		scriptGroupInstance.name = params.get("name")
		scriptGroupInstance.scriptList.clear();
		def idList = params?.idList
			idList = idList.replaceAll("sgscript-","")
			idList = idList.replaceAll("end","")
			StringTokenizer st = new StringTokenizer(idList,",")
		while(st.hasMoreTokens()){
			String token = st.nextToken()
			if(token && token.size()>0){
				ScriptFile sctFile = ScriptFile.findById(token)
				if(sctFile && !scriptGroupInstance?.scriptList?.contains(sctFile)){
					scriptGroupInstance.addToScriptList(sctFile)
				}
			}
		}
			

		if (!scriptGroupInstance.save(flush: true)) {
			
			flash.message = "TestSuite name is already in use. Please use a different name."
			errorList.add("TestSuite name is already in use. Please use a different name.");
			render errorList as JSON
			return
		}
		flash.message = message(code: 'default.updated.message', args: [
			message(code: 'scriptGroup.label', default: 'Test Suite'),
			scriptGroupInstance.name
		])
		
		errorList.add(message(code: 'default.updated.message', args: [
			message(code: 'scriptGroup.label', default: 'Test Suite'),
			scriptGroupInstance.name
		]));
		render errorList as JSON
	}
    /**
     * Save ScriptGroup
     * @return
     */
	def save() {
//		def scriptGroupInstance = new ScriptGroup(params)
//        if(ScriptGroup.findByName(params?.name)){
//            flash.message = "TestSuite name is already in use. Please use a different name."
//            redirect(action: "list")
//            return
//        }
//        else if(!(params?.scripts) && !(params?.scriptElement)){
//            flash.message = "Select scripts to create a test suite."
//            redirect(action: "list")
//            return
//        }
//		
//		if(params?.scriptElement){
//			def list = params?.scriptElement
//			list = list.replaceAll("script-","")
//			println " listt "+list
//			
//			StringTokenizer st = new StringTokenizer(list,",")
//			while(st.hasMoreTokens()){
//				Script sct = Script.findById(st.nextToken())
//				println " scriptt "+ sct
//				if(sct){
//					scriptGroupInstance.addToScriptsList(sct)
//				}
//			}
//		}
//		
//		scriptGroupInstance.groups = utilityService.getGroup()
//		if (!scriptGroupInstance.save(flush: true)) {
//			return
//		}
//		flash.message = message(code: 'default.created.message', args: [
//			message(code: 'scriptGroup.label', default: 'Test Suite'),
//			scriptGroupInstance.name
//		])
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
		def scripts = scriptService.getScriptNameFileList(getRealPath());   
		
		def time1 = System.currentTimeMillis()
		
		def list4 = scripts.findAll(){
			!((scriptGroupInstance.scriptList).contains(it))
		}
		list4.sort{a,b -> a?.scriptName <=> b?.scriptName}
		
		[scripts:list4,scriptNameList:scriptGroupInstance.scriptList,scriptGroupInstance: scriptGroupInstance]
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
//		def primitiveTestList = PrimitiveTest.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(), [order: 'asc', sort: 'name'])//PrimitiveTest.list([order: 'asc', sort: 'name'])		
		def primitiveTestList = primitiveService.getPrimitiveList(getRealPath())
		def lis = primitiveTestList.toList()
		Collections.sort(lis)
		[ primitiveTestList : lis]
	}

    /**
     * Edit Script
     * @return
     */
	def editScript() {
		if(params.id){
			StringTokenizer st = new StringTokenizer(params.id,"@")
			String dirName
			String fileName
			if(st.countTokens() == 2){
				dirName = st.nextToken()
				fileName = st.nextToken()
			}
			def script = scriptService.getScript(getRealPath(),dirName,fileName)
			
			if(script){
			[script : script , flag : params?.flag]
			}else{
				render "Error : No script available with this name : "+fileName +"in module :"+dirName
			}
			}
		
	}
	
	def getRealPath(){
		return request.getRealPath("/")
	}
	

    /**
     * Delete Script
     * @return
     */
	def deleteScript(){

		if(params.id){
			StringTokenizer st = new StringTokenizer(params.id,"@")
			String dirName
			String fileName
			if(st.countTokens() == 2){
				dirName = st.nextToken()
				fileName = st.nextToken()
			}
			
			def scriptDirName = primitiveService.getScriptDirName(dirName)
			File file = new File( "${getRealPath()}//fileStore//testscripts//"+scriptDirName+"//"+dirName+"//"+fileName+".py");
			Map script = [:]

			
			def scriptObj = ScriptFile.findByScriptNameAndModuleName(fileName,dirName)
			

			if (!scriptObj) {
				flash.message = "Script not found"
				render("Not found")
			}else{
				def script1 = scriptService.getScript(getRealPath(), dirName, fileName)
				boolean scriptInUse = scriptgroupService.checkScriptStatus(scriptObj,script1)
				scriptService.deleteScript(scriptObj)

				if(scriptInUse){
					flash.message = "Can't Delete. Scripts may be used in Script Group"
					render("Exception")
				}
				else{
					scriptObj.delete(flush: true)
				}
			}
			
			if(file.exists()){
				try {
					def fileDelete = file.delete()
					if(fileDelete){
						flash.message = "Deleted the script '${fileName}'"
						render("success")
					}else{
						flash.message = "Failed to delet the script '${fileName}'"
						render("failure")
					}
				} catch (Exception e) {
					e.printStackTrace()
				}
			}else{
				flash.message = "Failed to delet the script '${fileName}'"
				render("failure")
			}
			
		}

	}
	
	def getScript(dirName,fileName){
		
		def scriptDirName = primitiveService.getScriptDirName(dirName)
		File file = new File( "${request.getRealPath('/')}//fileStore//testscripts//"+scriptDirName+"//"+dirName+"//"+fileName+".py");
		Map script = [:]
		if(file.exists()){
			String s = ""
			List line = file.readLines()
			int indx = 0
			String scriptContent = ""
			if(line.get(indx).startsWith("'''"))	{
					indx++
					while(indx < line.size() &&  !line.get(indx).startsWith("'''")){
					s = s + line.get(indx)+"\n"
					indx++
				}
				indx ++
				while(indx < line.size()){
					scriptContent = scriptContent + line.get(indx)+"\n"
					indx++
				}
			}
			
			
			String xml = s
			XmlParser parser = new XmlParser();
			def node = parser.parseText(xml)
			script.put("id", node.id.text())
			script.put("version", node.version.text())
			script.put("name", node.name.text())
			script.put("skip", node.skip.text())
			def nodePrimitiveTestidText = node.primitiveTestid.text()
			def primitiveTst = PrimitiveTest.findById(nodePrimitiveTestidText)
			script.put("primitiveTest",primitiveTst)
			def versList = []
			def btList = []
			Set btSet = node?.boxTypes.boxType.collect{ it.text() }
			Set versionSet = node?.rdkVersions.rdkVersion.collect{ it.text() }
			btSet.each { bt ->
				btList.add(BoxType.findByName(bt))
			}
			versionSet.each { ver ->
				versList.add(RDKVersions.findByBuildVersion(ver))
			}
			script.put("rdkVersions", versList)
			script.put("boxTypes", btList)
			script.put("status", node?.status?.text())
			script.put("synopsis", node?.synopsis?.text())
			script.put("scriptContent", scriptContent)
			script.put("executionTime", node.execution_time.text())
		}
		return script
	}
	
    /**
     * Save Script
     * @return
     */
    def saveScript() {
		
        def error = ''
		def scriptList = scriptService.getScriptNameList()
        if(scriptList?.contains(params?.name?.trim())){
			render("Duplicate Script Name not allowed. Try Again.")
        }else if((!params?.ptest) || params?.ptest == "default" ){
			render("Please select a valid primitive test !!!")
        }
        else{
			boolean saveScript = false
			
			def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
			def moduleName = moduleMap.get(params?.ptest)
			
			def scriptsDirName = primitiveService.getScriptDirName(moduleName)
			def ptest = primitiveService.getPrimitiveTest(getRealPath()+"//fileStore//testscripts//"+scriptsDirName+"//"+moduleName+"//"+moduleName+".xml", params?.ptest)
			
				def writer = new StringWriter()
				def xml = new MarkupBuilder(writer)

				int time = 0
				if(params?.executionTime){
					try {
						time = Integer.parseInt(params?.executionTime)
					} catch (Exception e) {
						e.printStackTrace()
					}
				}

				boolean skipStatus
				if(params?.skipStatus.equals("on")){
					skipStatus = true
				}else{
					skipStatus = false
				}
				boolean longDuration = false
				if(params?.longDuration.equals("on")){
					longDuration = true
				}else{
					longDuration = false
				}
				

				Set boxTypes = []
				Set rdkVersions = []
			try {

				
				xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
				xml.xml(){
					xml.id("") //TODO add logic for id
					mkp.yield "\r\n  "
					mkp.comment "Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty"
					xml.version(1)
					mkp.yield "\r\n  "
					mkp.comment "Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1"
					xml.name(params?.name?.trim())
					mkp.yield "\r\n  "
					mkp.comment "If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension"
					xml.primitive_test_id(ptest?.id)
					mkp.yield "\r\n  "
					mkp.comment "Do not change primitive_test_id if you are editing an existing script."
					xml.primitive_test_name(ptest?.name)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.primitive_test_version(ptest?.version)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.status(Status.FREE)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.synopsis(params.synopsis?.trim())
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.groups_id(utilityService.getGroup()?.id)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.execution_time(time)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.long_duration(longDuration)
					mkp.yield "\r\n  "
					mkp.comment "execution_time is the time out time for test execution"
					xml.remarks(params?.remarks?.trim())
					mkp.yield "\r\n  "
					mkp.comment "Reason for skipping the tests if marked to skip"
					xml.skip(skipStatus?.toString())
					mkp.yield "\r\n  "
					mkp.comment ""
					
					def bTypeList = params?.boxTypes
					if(bTypeList instanceof List){
						bTypeList = bTypeList?.sort()
					}
					
					xml.box_types(){
						bTypeList?.each { bt ->
							def boxType = BoxType.findById(bt)
							boxTypes.add(boxType)
							xml.box_type(boxType?.name)
							mkp.yield "\r\n    "
							mkp.comment ""
						}
					}
					
					def rdkVersList = params?.rdkVersions
					if(rdkVersList instanceof List){
					rdkVersList = rdkVersList?.sort()
					}
					
					xml.rdk_versions(){
						rdkVersList?.each { vers ->

							def rdkVers = RDKVersions.findById(vers)
							rdkVersions.add(rdkVers)
							xml.rdk_version(rdkVers?.buildVersion)
							mkp.yield "\r\n    "
							mkp.comment ""
						}
					}

				}

				String dirname = ptest?.module?.name
				dirname = dirname?.trim()

				File dir = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName+"//"+dirname+"/")
				if(!dir.exists()){
					dir.mkdirs()
				}

				File file = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName+"//"+dirname+"/"+params?.name?.trim()+".py");
				if(!file.exists()){
					file.createNewFile()
				}
				String data = "'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+params?.scriptArea
				file.write(data)
				saveScript = true
			} catch (Exception e) {
				log.error "Error saving Script instance : ${params?.name}"
				render("Error in saving Script. Try Again." )
			}
				
			//TODO adding to default group pending
			
//			scriptInstance.groups = utilityService.getGroup()
			
			if(saveScript){
			def script = ScriptFile.findByScriptNameAndModuleName(params?.name?.trim(),ptest?.module?.name)
			if(script == null){
				script = new ScriptFile()
				script.setScriptName(params?.name)
				script.setModuleName(ptest?.module?.name)
				script.save(flush:true)
			}
			
			
			def sObject = new ScriptObject()
			sObject.setBoxTypes(boxTypes)
			sObject.setRdkVersions(rdkVersions)
			sObject.setName(params?.name?.trim())
			sObject.setModule(ptest?.module?.name)
			sObject.setScriptFile(script)
			sObject.setLongDuration(longDuration)
			
			scriptService.updateScript(script)
			scriptgroupService.saveToScriptGroups(script,sObject)
            scriptgroupService.saveToDefaultGroups(script,sObject, boxTypes)
			def sName = params?.name
				render(message(code: 'default.created.message', args: [
                    message(code: 'script.label', default: 'Script'),
                    sName
                ]))
			
        }
        }
    }
    
	
	/**
	 * Update Script
	 * @return
	 */
	def updateScript(Long id, Long version) {
		def scriptList = scriptService.getScriptNameList(request.getRealPath("/"))
		if (!scriptList?.contains(params?.prevScriptName?.trim())) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'script.label', default: 'Script'),
				id
			])
			redirect(action: "list")
			return
		}
		def moduleMap = primitiveService.getPrimitiveModuleMap(params?.ptest)
		def moduleName = moduleMap.get(params?.ptest)
		def scriptsDirName = primitiveService.getScriptDirName(moduleName)
		def ptest = primitiveService.getPrimitiveTest(getRealPath()+"/fileStore/testscripts/"+scriptsDirName+"/"+moduleName+"/"+moduleName+".xml", params?.ptest)
//		def module = Module.findByName(moduleName)
		def scrpt = scriptService.getScript(getRealPath(),moduleName, params?.prevScriptName)
		
		boolean isLongDuration = scrpt?.longDuration
		
		if (params.scriptVersion != null) {
			
			def a = scrpt.version
			def b = params.scriptVersion
			long vers1 = 0
			long vers2 = 0
			
			
			if( a instanceof String){
				vers1 = Long.parseLong(a)
			}
			
			if( b instanceof String){
				vers2 = Long.parseLong(b)
			}
			if (vers1 > vers2) {
				clearEditLock(params?.name)
						flash.message = "Script changes not saved, another user has updated this Script while you were editing !!!"
						redirect(action: "list")
				return
			}
		}
		boolean saveScript =  false
		boolean longDuration = false
				Set bTypes = []
				Set rdkVers = []
		try {
			
			
			
			def writer = new StringWriter()
			def xml = new MarkupBuilder(writer)
			
			def b = params.scriptVersion
			long vers2 = 0
			if( b instanceof String){
				vers2 = Long.parseLong(b)
				vers2 ++
			}
			
			int time = 0
			if(params?.executionTime){
				try {
					time = Integer.parseInt(params?.executionTime)
				} catch (Exception e) {
					e.printStackTrace()
				}
			}
			
			
			if(params?.longDuration.equals("on")){
				longDuration = true
			}else{
				longDuration = false
			}
			
	
	boolean skipStatus
	if(params?.skipStatus.equals("on")){
		skipStatus = true
	}else{
		skipStatus = false
	}
	
			
			xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
			xml.xml(){
				xml.id(scrpt?.id)
				mkp.yield "\r\n  "
				mkp.comment "Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty"
				xml.version(vers2)
				mkp.yield "\r\n  "
				mkp.comment "Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1"
				xml.name(params?.name?.trim())
				mkp.yield "\r\n  "
				mkp.comment "If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension"
				xml.primitive_test_id(ptest?.id)
				mkp.yield "\r\n  "
				mkp.comment "Do not change primitive_test_id if you are editing an existing script."
				xml.primitive_test_name(ptest?.name)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.primitive_test_version(ptest?.version)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.status(Status.FREE)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.synopsis(params.synopsis?.trim())
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.groups_id(utilityService.getGroup()?.id)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.execution_time(time)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.long_duration(longDuration)
				mkp.yield "\r\n  "
				mkp.comment "execution_time is the time out time for test execution"
				xml.remarks(params?.remarks?.trim())
				mkp.yield "\r\n  "
				mkp.comment "Reason for skipping the tests if marked to skip"
				xml.skip(skipStatus?.toString())
				mkp.yield "\r\n  "
				mkp.comment ""
				
				def bTypeList = params?.boxTypes
				if(bTypeList instanceof List){
					bTypeList = bTypeList?.sort()
				}
				
				xml.box_types(){
					bTypeList?.each { bt ->
						def btype = BoxType.findById(bt)
						bTypes.add(btype)
						xml.box_type(btype?.name)
						mkp.yield "\r\n    "
						mkp.comment ""
					}
				}
				
				def rdkVersList = params?.rdkVersions
				if(rdkVersList instanceof List){
				rdkVersList = rdkVersList?.sort()
				}
				xml.rdk_versions(){
					rdkVersList?.each { vers ->
					def rdkVer = RDKVersions.findById(vers)
					rdkVers.add(rdkVer)
					xml.rdk_version(rdkVer?.buildVersion)
					mkp.yield "\r\n    "
					mkp.comment ""
					}
				}
				
				
				
			}
			
			String dirname = ptest?.module?.name
					dirname = dirname?.trim()
					
			def scriptsDirName1 = primitiveService.getScriptDirName(moduleName)
							
			File dir = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName1+"/"+dirname+"/")
			if(!dir.exists()){
				dir.mkdirs()
			}
			
			
			
			File file = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName1+"/"+dirname+"/"+params?.name?.trim()+".py");
			if(!file.exists()){
				file.createNewFile()
			}
			String data = "'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+params?.scriptArea
			file.write(data)
			if(params?.prevScriptName != params?.name && params?.prevScriptName?.trim() != params?.name?.trim()){
				File file1 = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName1+"/"+dirname+"/"+params?.prevScriptName?.trim()+".py");
				if(file1.exists() ){
					file1.delete()
				}
			}
			saveScript = true
		} catch (Exception e) {
			e.printStackTrace()
		}
			
		def boxTypes = bTypes?.toList()
		def boxTypesList = []
//		scriptInstance.name = params.name
//		scriptInstance.scriptContent = params.scriptArea
//		scriptInstance.synopsis = params.synopsis
//		scriptInstance.remarks = params?.remarks
//		
//		if(params?.skipStatus.equals("on")){
//			scriptInstance.skip = true
//		}else{
//		scriptInstance.skip = false
//		}
//		scriptInstance.primitiveTest = PrimitiveTest.findById(params.ptest)
//		scriptInstance.executionTime = Integer.parseInt(params?.executionTime)
//	
//		if (!scriptInstance.save(flush: true)) {
//			log.error "Error saving Script instance : ${scriptInstance.errors}"
//			return
//		}
//
//		if(boxTypes){
//			boxTypesList = scriptgroupService.createBoxTypeList(boxTypes)
//			scriptgroupService.removeScriptsFromBoxSuites(scriptInstance)
//			scriptgroupService.saveToDefaultGroup(scriptInstance, boxTypesList)
//		}
//
//		scriptInstance.properties = params
//		
//		scriptgroupService.updateScriptsFromRDKVersionBoxTypeTestSuites(scriptInstance)
		if(params?.prevScriptName != params?.name ){
			def sFile = ScriptFile.findByScriptName(params?.prevScriptName)
			sFile.scriptName = params?.name
			sFile.save()
			scriptService.updateScriptNameChange(params?.prevScriptName,sFile)
		}
		
		clearEditLock(params?.name)
		if(!saveScript){
			log.error "Error saving Script instance : ${params.name}"
						return
		}else{
		
		
		def script = ScriptFile.findByScriptNameAndModuleName(params?.name?.trim(),ptest?.module?.name)
		if(script == null){
			script = new ScriptFile()
			script.setScriptName(params?.name)
			script.setModuleName(ptest?.module?.name)
			script.save(flush:true)
		}
		
		def sObject = new ScriptObject()
		sObject.setBoxTypes(bTypes)
		sObject.setRdkVersions(rdkVers)
		sObject.setName(params?.name?.trim())
		sObject.setModule(ptest?.module?.name)
		sObject.setScriptFile(script)
		sObject.setLongDuration(longDuration)
		
		if(boxTypes){
//			boxTypesList = scriptgroupService.createBoxTypeList(boxTypes)
			scriptgroupService.removeScriptsFromBoxSuites1(script)
			if(isLongDuration != longDuration){
				scriptgroupService.updateScriptGroup(script,sObject)
			}
//			scriptgroupService.saveToDefaultGroup(script, boxTypesList)
		}
		
		scriptgroupService.saveToScriptGroups(script,sObject)
		scriptgroupService.saveToDefaultGroups(script,sObject, bTypes)
		
		
		
				
		scriptgroupService.updateScriptsFromRDKVersionBoxTypeTestSuites1(script,sObject)
		
		flash.message = message(code: 'default.updated.message', args: [
			message(code: 'script.label', default: 'Script'),
			params.name
		])
		}
		redirect(action: "list", params: [scriptId: params.id])
	}	
    
    /**
     * Get Module name, version and testGroup
     * through ajax call
     * @return
     */
    def getModuleName(){
        List moduleDetails = []
		def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def moduleName = moduleMap.get(params?.primId)
		def module = Module.findByName(moduleName)
        moduleDetails.add(module.name.toString().trim() )
        moduleDetails.add(module.rdkVersion.toLowerCase().trim() )
        moduleDetails.add( module.testGroup.toString().trim() )
		moduleDetails.add(module.executionTime.toString().trim() )
        render moduleDetails as JSON
    }
    
    /**
     * Show streaming details in a popup in script page
     * @param max
     * @return
     */
    def showStreamDetails(){       
		def streamingDetailsList = StreamingDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
		def radioStreamingDetails = RadioStreamingDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
		[streamingDetailsInstanceList: streamingDetailsList, radioStreamingDetails:radioStreamingDetails, streamingDetailsInstanceTotal: streamingDetailsList.size()]
       // [streamingDetailsInstanceList: StreamingDetails.list(), streamingDetailsInstanceTotal: StreamingDetails.count()]
    }
    
    /**
     * Get the list of scripts based on the scriptName.
     * @return
     */
    def searchScript(){
//        def scripts = Script.findAll("from Script as b where b.name like '%${params?.searchName}%'")
		def moduleMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
		
		def scriptNameList = scriptService.getScriptNameList(getRealPath())
		def scripts = []
		scriptNameList?.each {
			if(it?.toLowerCase()?.contains(params?.searchName?.toLowerCase())){
				def moduleName = moduleMap.get(it)
				def script = scriptService.getScript(getRealPath(), moduleName, it)
				if(script){
					scripts.add(script)
				}
			}
		}
		
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
					def moduleMap = scriptService.getScriptNameModuleNameMapping(getRealPath())  
					def moduleName = moduleMap.get(it?.key)   
					def script = ScriptFile.findByScriptNameAndModuleName(it.key,moduleName)
					if(script){
						scriptInstance = scriptGroup.scriptList.find { it.id == script?.id }
						if(!scriptInstance){
							scriptGroup.addToScriptList(script)
						}
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
                   def moduleMap = scriptService.getScriptNameModuleNameMapping(getRealPath())  
					def moduleName = moduleMap.get(it?.key)   
					def script = ScriptFile.findByScriptNameAndModuleName(it.key,moduleName)
					if(script){
                    scriptGroupInstance.addToScriptList(script)
					}
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
		def scriptMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
		def mName = scriptMap.get(params.scriptName)
		def scriptInstance = scriptService.getScript(getRealPath(), mName, params.scriptName)
//		Script scriptInstance = Script.findByName(params.scriptName)
		if(scriptInstance){
			scriptInstanceList.add(scriptInstance.name)
		}
		render scriptInstanceList as JSON
	}
	
	def fetchScriptWithScriptName(){

		List scriptInstanceList = []
		def scriptMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
		def mName = scriptMap.get(params.scriptName)
		def scriptInstance = scriptService.getScript(getRealPath(), mName, params.scriptName)
		//		Script scriptInstance = Script.findByName(params.scriptName)
		if(scriptInstance){
			scriptInstanceList.add(mName+"@"+scriptInstance.name)
		}
		render scriptInstanceList as JSON
	}
	
	
	
	/**
	 * Method to download the script content as python script file.
	 * @return
	 */
	def exportScriptContent(){
		if(params?.id){
//			Script script = Script.findById(params?.id)
			def sMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
			def moduleName = sMap.get(params?.id)
			def scriptDir = primitiveService.getScriptDirName(moduleName)
			File sFile = new File(getRealPath()+"/fileStore/testscripts/"+scriptDir+"/"+moduleName+"/"+params?.id+".py")
			if(sFile.exists()){
//			def script = scriptService.getScript(getRealPath(), moduleName, params?.id)
			params.format = "text"
			params.extension = "py"
			String data = new String(sFile.getBytes())
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ params?.id+".py\"")
			response.setHeader("Content-Length", ""+data.length())
			response.outputStream << data.getBytes()
			}else{
			flash.message = "Download failed. No valid script is available for download."
			redirect(action: "list")
		}
		}else{
			flash.message = "Download failed. No valid script is available for download."
			redirect(action: "list")
		}
	}
	
	def exportScriptAsXML(){
//		exportCurrentScript(params,response)
		
		exportAllPrimitive();
		exportAllScripts();
//		redirect(action: "list", params: params)
//		if(params?.id){
//			Script script = Script.findById(params?.id)
//
//			def writer = new StringWriter()
//			def xml = new MarkupBuilder(writer)
//			xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
//			xml.xml(){
//				xml.name(script?.name)
//				xml.id(script?.id)
//				xml.version(1)
//				xml.primitiveTestid(script?.primitiveTest?.id)
//				xml.primitiveTestName(script?.primitiveTest?.name)
//				xml.primitiveTestVersion(script?.primitiveTest?.version)
//				xml.status(script?.status)
//				xml.synopsis(script?.synopsis?.trim())
//				xml.groupsid(script?.groups?.id)
//				xml.execution_time(script?.executionTime)
//				xml.remarks(script?.remarks?.trim())
//				xml.skip(script?.skip?.toString())
//				
//			}
//			response.setHeader "Content-disposition", "attachment; filename=${script?.name}.py"
//			response.contentType = 'application/octet-stream;'
//			response.outputStream << "'''"
//			response.outputStream << "\n"
//			response.outputStream << writer.toString()
//			response.outputStream << "\n"
//			response.outputStream << "'''"
//			response.outputStream << "\n"
//			response.outputStream << script?.scriptContent
//			response.outputStream.flush()
//		}
	}
	def exportCurrentScript(params,response){
				if(params?.id){
					Script script = Script.findById(params?.id)
		
					def writer = new StringWriter()
					def xml = new MarkupBuilder(writer)
					xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
					xml.xml(){
						xml.name(script?.name)
						mkp.comment "If you are adding a new script you can specify the script name."
						xml.id(script?.id)
						xml.version(1)
						xml.primitiveTestid(script?.primitiveTest?.id)
						xml.primitiveTestName(script?.primitiveTest?.name)
						xml.primitiveTestVersion(script?.primitiveTest?.version)
						xml.status(script?.status)
						xml.synopsis(script?.synopsis?.trim())
						xml.groupsid(script?.groups?.id)
						xml.execution_time(script?.executionTime)
						xml.remarks(script?.remarks?.trim())
						xml.skip(script?.skip?.toString())
		
					}
					response.setHeader "Content-disposition", "attachment; filename=${script?.name}.py"
					response.contentType = 'application/octet-stream;'
					response.outputStream << "'''"
			response.outputStream << "\n"
			response.outputStream << writer.toString()
			response.outputStream << "\n"
			response.outputStream << "'''"
					response.outputStream << "\n"
					response.outputStream << script?.scriptContent
					response.outputStream.flush()
				}
	}
	
	
	def exportAllScripts(){
		try {
			def groupsInstance = utilityService.getGroup()
			def scriptInstanceList = Script.findAllByGroupsOrGroupsIsNull(groupsInstance)
			def sMap = createScriptList(scriptInstanceList)
			
			def mList = Module.findAll()
			mList.each {  modl ->
			
			def sList = sMap.get(modl?.name)
			
			sList.each { script ->
			def writer = new StringWriter()
			def xml = new MarkupBuilder(writer)
			xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
			xml.xml(){
				xml.id(script?.id)
				mkp.yield "\r\n  "
				mkp.comment "Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty"
				xml.version(1)
				mkp.yield "\r\n  "
				mkp.comment "Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1"
				xml.name(script?.name)
				mkp.yield "\r\n  "
				mkp.comment "If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension "
				xml.primitive_test_id(script?.primitiveTest?.id)
				mkp.yield "\r\n  "
				mkp.comment "Do not change primitive_test_id if you are editing an existing script."
				xml.primitive_test_name(script?.primitiveTest?.name)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.primitive_test_version(script?.primitiveTest?.version)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.status(script?.status)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.synopsis(script?.synopsis?.trim())
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.groups_id(script?.groups?.id)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.execution_time(script?.executionTime)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.long_duration(script?.longDuration)
				mkp.yield "\r\n  "
				mkp.comment "execution_time is the time out time for test execution"
				xml.remarks(script?.remarks?.trim())
				mkp.yield "\r\n  "
				mkp.comment "Reason for skipping the tests if marked to skip"
				xml.skip(script?.skip?.toString())
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.box_types(){
					script.boxTypes.each { bt ->
					xml.box_type(bt.name)
					mkp.yield "\r\n    "
					mkp.comment ""
					}
				}
				xml.rdk_versions(){
					script.rdkVersions.each { vers ->
					xml.rdk_version(vers.buildVersion)
					mkp.yield "\r\n    "
					mkp.comment ""
					}
				}
				
			}
			
			String dirname = modl?.name
					dirname = dirname?.trim()
					def scriptsDirName = primitiveService.getScriptDirName(dirname)
							File dir = new File( "${request.getRealPath('/')}/fileStore/testscripts/"+scriptsDirName+"/"+dirname+"/")
			if(dir.exists()){
				dir.mkdirs()
			}
			
			File file = new File( "${request.getRealPath('/')}/fileStore/testscripts/"+scriptsDirName+"/"+dirname+"/"+script?.name?.trim()+".py");
			if(!file.exists()){
				file.createNewFile()
			}
			String data = "'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+script?.scriptContent
					file.write(data)
			}
			
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

	}
	def exportAllPrimitive(){

			try {
				def mList = Module.findAll()
						mList.each {  modl ->
						
						
						def writer = new StringWriter()
						def xml = new MarkupBuilder(writer)
						xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
						xml.xml(){
							
							module("name":modl?.name, "testGroup":modl.testGroup){
								
								xml.primitiveTests(){
									def pList = PrimitiveTest.findAllByModule(modl)
											if(pList){
												
												pList.each { primitive ->
												xml.primitiveTest(name : primitive?.name, id : primitive?.id , version :primitive?.version ){
													xml.function(primitive?.function?.name)
													xml.parameters(){
														primitive.parameters.each { param ->
														parameter("name" :param.parameterType.name,"value" :param.value)
														}
													}
												}
												
												}
											}
								}
							}
						}
						String dirname = modl?.name
						dirname = dirname?.trim()
						def scriptsDirName = primitiveService.getScriptDirName(dirname)
						File dir = new File( "${request.getRealPath('/')}/fileStore/testscripts/"+scriptsDirName+"/"+dirname+"/")
						
						if(!dir.exists()){
							dir.mkdirs()
						}
						
						File file = new File( "${request.getRealPath('/')}/fileStore/testscripts/"+scriptsDirName+"/"+dirname+"/"+dirname+".xml");
						if(!file.exists()){
							file.createNewFile()
						}
						file.write(writer.toString())
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
	}
	
	def addEditLock(){
		
		def scriptName = params?.scriptName
		if(ScriptService.scriptLockList.contains(scriptName)){
			ScriptService.scriptLockList.add(params?.scriptName)
			render "false" as String
			return
		}else{
			ScriptService.scriptLockList.add(params?.scriptName)
		}
		render "true" as String
	}
	
	def clearEditLock(def scriptName){
		ScriptService.scriptLockList.remove(scriptName)
	}
	
	def removeEditLock(){
		ScriptService.scriptLockList.remove(params?.scriptName)
	}
	

}