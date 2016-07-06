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
import com.comcast.rdk.Category
import org.springframework.dao.DataIntegrityViolationException
//import com.sun.xml.internal.bind.v2.schemagen.xmlschema.List;
import grails.converters.JSON
import groovy.xml.MarkupBuilder
import org.apache.shiro.SecurityUtils
import org.apache.shiro.subject.Subject

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

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
		/*def scriptNameList = scriptService.getScriptNameList(requestGetRealPath)
		 def scriptGroupMap = scriptService.getScriptsMap(requestGetRealPath)
		 scriptGroupMap?.keySet()?.sort{a,b -> a <=> b}
		 scriptGroupMap = new TreeMap(scriptGroupMap)
		 def lists = ScriptGroup.executeQuery('select name from ScriptGroup')
		 [scriptGroupInstanceList: lists, scriptGroupInstanceTotal: lists.size(),error: params.error, scriptId: params.scriptId, scriptGroupId:params.scriptGroupId, scriptInstanceTotal: scriptNameList.size(), scriptGroupMap:scriptGroupMap]
		 */
		def scriptNameListV = scriptService.getScriptNameList(requestGetRealPath,"RDKV")
		scriptNameListV = scriptNameListV?scriptNameListV:[]
		def scriptNameListB = scriptService.getScriptNameList(requestGetRealPath, "RDKB")
		scriptNameListB = scriptNameListB?scriptNameListB:[]
		def scriptNameListTCL = scriptService.getTCLNameList(requestGetRealPath)
		scriptNameListTCL = scriptNameListTCL?scriptNameListTCL?.sort():[]
		def scriptGroupMapB = scriptService.getScriptsMap(requestGetRealPath, "RDKB")
		scriptGroupMapB = scriptGroupMapB?scriptGroupMapB:[:]
		def scriptGroupMapV = scriptService.getScriptsMap(requestGetRealPath, "RDKV")
		scriptGroupMapV = scriptGroupMapV?scriptGroupMapV:[:]
		
		//def lists = ScriptGroup.executeQuery('select name from ScriptGroup')
		def listsV = ScriptGroup.executeQuery("select name from ScriptGroup where category=:category order by name",[category:Category.RDKV])
		listsV = listsV?listsV : []
		def listsB = ScriptGroup.executeQuery("select name from ScriptGroup where category=:category order by name",[category:Category.RDKB])
		listsB = listsB?listsB : []
		def listsTCL = ScriptGroup.executeQuery("select name from ScriptGroup where category=:category order by name",[category:Category.RDKB_TCL])
		listsTCL = listsTCL?listsTCL?.sort():[]
		//[scriptGroupInstanceList: lists, scriptGroupInstanceTotal: lists.size(),
		
		[error: params.error, scriptId: params.scriptId, scriptGroupId:params.scriptGroupId,
			scriptInstanceTotalV: scriptNameListV?.size(),scriptInstanceTotalB: scriptNameListB?.size(),
			scriptGroupMapV:scriptGroupMapV, scriptGroupMapB:scriptGroupMapB, scriptGroupInstanceListV:listsV, scriptGroupInstanceListB:listsB,
			scriptGroupInstanceTotalV: listsV?.size(), scriptGroupInstanceTotalB: listsB?.size(),
			tclScripts:scriptNameListTCL, tclScriptInstanceTotal:scriptNameListTCL?.size(),  scriptGrpTcl :listsTCL, tclScriptSize : listsTCL?.size()  ]
	}

	/**
	 * Method to get script file list when selecting test suite 
	 */
	def getScriptsList(String group){
		def scripts
		def finalScripts = []
		if(group){
			def scriptGroup =  ScriptGroup.findByName(group)
			scripts = scriptGroup?.scriptList
			scripts.each{
				finalScripts.add(new ScriptFileBean(scriptName:it?.scriptName, id:it?.id, moduleName:it?.moduleName, category:it?.category))
			}
		}
		if(!finalScripts.isEmpty()){
			finalScripts.sort { a, b ->
				a.scriptName <=> b.scriptName

			}
		}
		render  new Gson().toJson(finalScripts)
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
		def category = params?.category?.trim()
		def scriptNameList = null
		def sList = null
		if(!Category.RDKB_TCL.toString().equals(category)){
			scriptNameList = scriptService.getScriptNameFileList(getRealPath(), category)
		}else{
			scriptNameList = scriptService.tclScriptsList
		}
		sList = scriptNameList.clone()
		sList?.sort{a,b -> a?.scriptName <=> b?.scriptName}

		[scriptGroupInstance: new ScriptGroup(params),scriptInstanceList:sList,category:params?.category]
	}


	/**
	 * Method to create script group.
	 * @return
	 */
	def createScriptGrp(){
		def errorList= []
		def scriptGroupInstance = new ScriptGroup(params)
		scriptGroupInstance.category = Utility.getCategory(params?.category)
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
		if (!scriptGroupInstance.save(flush: true)) {
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
	/*def edit(Long id) {
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
	 }*/

	def edit(String name) {
		def scriptGroupInstance = ScriptGroup.findByName(name)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			])
			redirect(action: "list")
			return
		}
		//def scripts = scriptService.getScriptNameFileList(getRealPath());
		def scripts = null
		if(scriptGroupInstance.category != Category.RDKB_TCL){
			scripts = scriptService.getScriptNameFileList(getRealPath(), scriptGroupInstance?.category?.toString());
		}
		else{
			scripts = scriptService.tclScriptsList
		}

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
		def primitiveTestList = primitiveService.getPrimitiveList(getRealPath(), params?.category)
		def lis = primitiveTestList.toList()
		Collections.sort(lis)
		[ primitiveTestList : lis, category: params?.category]
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
			def script = scriptService.getScript(getRealPath(),dirName,fileName, params.category?.trim())
			if(script){
				[script : script , category : params?.category]
			}else{
				render "Error : No script available with this name : "+fileName +"in module :"+dirName
			}
		}

	}


	/**
	 * Only display tcl script content
	 *  
	 */
	def tclScriptDisplay(){
		def scriptName = params?.scriptName
		def scriptText = scriptService.getTclScript(getRealPath(), scriptName)
		if(scriptText){
			render (view:"editScript", model:[script : scriptText , category : Category.RDKB_TCL.toString(), scriptName:scriptName])
		}else{
			render "Error : No script available with this name : "+scriptName
		}
	}
	
	
	def saveTcl() {
		def content =  params.tclText
		def script = params.scriptName
		if(content && script){
			def file = Utility.getTclFilePath(getRealPath(), script)
			try{
				if(file){
					Utility.writeContentToFile(content, file)
					removeLock(script)
					flash.message = message(code: 'default.updated.message', args: [
						message(code: 'script.label', default: 'Script'),
						params.scriptName])
				}
				else{
					removeLock(script)
					flash.error = 'File ${script} not found.'
				}
			}
			catch(Exception e){
				e.printStackTrace()
				removeLock(script)
				flash.error = "Error occured while updating. Please try again."
			}
		}
		else{
			flash.error = "No content/scriptname. Please try again."
		}
		
	redirect(action: "list")
		
	}
	
	

	def getRealPath(){
		//return request.getRealPath("/")
		return request.getSession().getServletContext().getRealPath("/")
	}


	/**
	 * Delete Script
	 * @return
	 */
	def deleteScript(){
		
		def isTcl = false
		if(params.id){
			String dirName
			String fileName
			def scriptDirName
			if(params.id?.contains('@')){
				StringTokenizer st = new StringTokenizer(params.id,"@")
				if(st.countTokens() == 2){
					dirName = st.nextToken()
					fileName = st.nextToken()
					scriptDirName = primitiveService.getScriptDirName(dirName)
				}
			}
			else{
				isTcl = true
				dirName = 'tcl'
				fileName = params.id
			}

			Map script = [:]

			File file = null


			def scriptObj = ScriptFile.findByScriptNameAndModuleName(fileName,dirName)


			if (!scriptObj) {
				flash.message = "Script not found"
				render("Not found")
			}else{
				boolean scriptInUse = false
				if(isTcl){
					file = new File(getTestScriptPath(scriptObj?.category.toString())+FILE_SEPARATOR +fileName+".tcl")
					scriptInUse = false // this need to be updated accordingly
					scriptService.deleteScript(scriptObj, scriptObj?.category?.toString())
				}
				else{
					file = new File(getTestScriptPath(scriptObj?.category.toString())+FILE_SEPARATOR + scriptDirName+FILE_SEPARATOR+dirName+FILE_SEPARATOR+fileName+".py")
					def script1 = scriptService.getScript(getRealPath(), dirName, fileName, scriptObj?.category?.toString())
					scriptInUse = scriptgroupService.checkScriptStatus(scriptObj,script1)
					scriptService.deleteScript(scriptObj, scriptObj?.category?.toString())
				}

				if(scriptInUse){
					flash.message = "Can't Delete. Scripts may be used in Script Group"
					render("Exception")
				}
				else{
					scriptObj.delete(flush: true)
				}
			}

			if(file != null && file.exists()){
				try {
					def fileDelete = file.delete()
					if(fileDelete){
						flash.message = "Deleted the script '${fileName}'"
						render("success")
					}else{
						flash.message = "Failed to delete the script '${fileName}'"
						render("failure")
					}
				} catch (Exception e) {
					e.printStackTrace()
				}
			}else{
				flash.message = "Failed to delete the script '${fileName}'"
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
			 int indx = line?.findIndexOf {  it.startsWith("'''")} 
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
		def scriptList = scriptService.getScriptNameList(getRealPath(),params?.category)
	//	if(scriptList?.toString().contains(params?.name?.toString().trim())){
		if(scriptList?.toString()?.contains(params?.name?.trim()?.toString())){
			render("Duplicate Script Name not allowed. Try Again.")
		}else if((!params?.ptest) || params?.ptest == "default" ){
			render("Please select a valid primitive test !!!")
		}
		else{
			boolean saveScript = false

			def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
			def moduleName = moduleMap.get(params?.ptest)

			def scriptsDirName = primitiveService.getScriptDirName(moduleName)
			//def ptest = primitiveService.getPrimitiveTest(getRealPath()+"//fileStore//testscripts//"+scriptsDirName+"//"+moduleName+"//"+moduleName+".xml", params?.ptest)
			
			def category = params?.category?.trim()
			def ptest
			def path = getRealPath()+Constants.FILE_SEPARATOR+"fileStore"+Constants.FILE_SEPARATOR

			if("RDKV".equals(category)){
				path = path+"testscriptsRDKV" + Constants.FILE_SEPARATOR + scriptsDirName.toString() + Constants.FILE_SEPARATOR + moduleName +Constants.FILE_SEPARATOR + moduleName +".xml"
			}
			else if("RDKB".equals(category)){
				path = path + "testscriptsRDKB" + Constants.FILE_SEPARATOR + scriptsDirName.toString() + Constants.FILE_SEPARATOR + moduleName  +Constants.FILE_SEPARATOR+moduleName+".xml"
			}
			ptest = primitiveService.getPrimitiveTest(path, params?.ptest)
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
			Set scrptTags = []
			
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

					def bTypeList = params.list("boxTypes")
					xml.box_types(){
						bTypeList.each{ bType ->
							bType = Integer.parseInt(bType)
							def boxType = BoxType.findById(bType)
							boxTypes.add(boxType)
							xml.box_type(boxType?.name)
							mkp.yield "\r\n    "
							mkp.comment ""
						}
					}

					def rdkVersList = params?.list("rdkVersions")

					xml.rdk_versions(){
						rdkVersList?.each { vers ->
							def rdkVers = RDKVersions.findById(vers)
							rdkVersions.add(rdkVers)
							xml.rdk_version(rdkVers?.buildVersion)
							mkp.yield "\r\n    "
							mkp.comment ""
						}
					}
					def scriptTagList = params?.scriptTags
					if(scriptTagList && scriptTagList instanceof List){
						scriptTagList = scriptTagList?.sort()
					}
					try {
						if(scriptTagList?.size() > 0){
							xml.script_tags(){
								scriptTagList?.each { tag ->
									def sTag = ScriptTag.findById(tag)
									scrptTags.add(sTag)
									xml.script_tag(sTag?.name)
									mkp.yield "\r\n    "
									mkp.comment ""
								}
							}
						}
					} catch (Exception e) {
						e.printStackTrace()
					}
				}

				String dirname = ptest?.module?.name

				dirname = dirname?.trim()


				def pathToDir =  "${request.getRealPath('/')}//fileStore"
				if("RDKV".equals(category)){
					pathToDir = pathToDir + Constants.FILE_SEPARATOR + "testscriptsRDKV"
				}
				else if("RDKB".equals(category)){
					pathToDir = pathToDir + Constants.FILE_SEPARATOR + "testscriptsRDKB"
				}

				//File dir = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName+"//"+dirname+"/")
				File dir = new File( pathToDir + Constants.FILE_SEPARATOR + scriptsDirName +  Constants.FILE_SEPARATOR +dirname)
				if(!dir.exists()){
					dir.mkdirs()
				}
				//File file = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName+"//"+dirname+"/"+params?.name?.trim()+".py");
				File file = new File( pathToDir + Constants.FILE_SEPARATOR + scriptsDirName + Constants.FILE_SEPARATOR+dirname+Constants.FILE_SEPARATOR+params?.name?.trim()+".py");
				if(!file.exists()){
					file.createNewFile()
				}
				File pyHeader = new File( "${request.getRealPath('/')}//fileStore//pyHeader.txt")
				def pyHeaderContentList = pyHeader?.readLines()
				String pyHeaderContent = ""
				pyHeaderContentList.each {
					pyHeaderContent += it?.toString()+"\n"
				}
				String data =pyHeaderContent+"'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+params?.scriptArea
				
				//String data = "'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+params?.scriptArea
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
					script.category = Utility.getCategory(params?.category)
					script.save(flush:true)
				}


				def sObject = new ScriptObject()
				sObject.setBoxTypes(boxTypes)
				sObject.setRdkVersions(rdkVersions)
				sObject.setScriptTags(scrptTags)
				sObject.setName(params?.name?.trim())
				sObject.setModule(ptest?.module?.name)
				sObject.setScriptFile(script)
				sObject.setLongDuration(longDuration)

				scriptService.updateScript(script, params?.category)
				scriptgroupService.saveToScriptGroups(script,sObject, params?.category)
				scriptgroupService.saveToDefaultGroups(script,sObject, boxTypes, params?.category)
				scriptgroupService.updateScriptsFromScriptTag(script,sObject,[],[])
				def sName = params?.name
				println "\n Successfully created \n"
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
		def scriptList = scriptService.getScriptNameList(request.getRealPath("/"), params?.category)
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
		def category = params?.category?.trim()
		def filePath = null
		if("RDKV".equals(category)){
			filePath = getRealPath() + FILE_SEPARATOR + "fileStore"+ FILE_SEPARATOR + "testscriptsRDKV" + FILE_SEPARATOR + scriptsDirName + FILE_SEPARATOR + moduleName+ FILE_SEPARATOR + moduleName +".xml"
		}
		else if("RDKB".equals(category)){
			filePath = getRealPath() + FILE_SEPARATOR + "fileStore"+ FILE_SEPARATOR + "testscriptsRDKB" + FILE_SEPARATOR + scriptsDirName + FILE_SEPARATOR + moduleName+ FILE_SEPARATOR + moduleName +".xml"
		}
		//def ptest = primitiveService.getPrimitiveTest(getRealPath()+"/fileStore/testscripts/"+scriptsDirName+"/"+moduleName+"/"+moduleName+".xml", params?.ptest)
		def ptest = primitiveService.getPrimitiveTest(filePath, params?.ptest)
		//		def module = Module.findByName(moduleName)
		def scrpt = scriptService.getScript(getRealPath(),moduleName, params?.prevScriptName, params?.category)
		def oldBoxTypes = scrpt?.boxTypes
		def oldRDKVersions = scrpt?.rdkVersions
		def oldTags = scrpt?.scriptTags
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
		Set scrptTags = []
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

				/*def bTypeList = params?.boxTypes
				 if(bTypeList instanceof List){
				 bTypeList = bTypeList?.sort()
				 }*/
				def bTypeList = params?.list("boxTypes")

				xml.box_types(){
					bTypeList?.each { bt ->
						def btype = BoxType.findById(bt)
						bTypes.add(btype)
						xml.box_type(btype?.name)
						mkp.yield "\r\n    "
						mkp.comment ""
					}
				}

				/*def rdkVersList = params?.rdkVersions
				 if(rdkVersList instanceof List){
				 rdkVersList = rdkVersList?.sort()
				 }*/

				def rdkVersList = params?.list("rdkVersions")
				xml.rdk_versions(){
					rdkVersList?.each { vers ->
						def rdkVer = RDKVersions.findById(vers)
						rdkVers.add(rdkVer)
						xml.rdk_version(rdkVer?.buildVersion)
						mkp.yield "\r\n    "
						mkp.comment ""
					}
				}

				def scriptTagList = params?.scriptTags
				if(scriptTagList instanceof List){
					scriptTagList = scriptTagList?.sort()
				}
				try {
					xml.script_tags(){
						scriptTagList?.each { tag ->
							def sTag = ScriptTag.findById(tag)
							scrptTags.add(sTag)
							xml.script_tag(sTag?.name)
							mkp.yield "\r\n    "
							mkp.comment ""
						}
					}
				} catch (Exception e) {
					e.printStackTrace()
				}


			}

			String dirname = ptest?.module?.name
			dirname = dirname?.trim()

			def scriptsDirName1 = primitiveService.getScriptDirName(moduleName)

			def testScriptPath = getTestScriptPath(params?.category?.trim())

			File dir = new File( testScriptPath+FILE_SEPARATOR+scriptsDirName1+FILE_SEPARATOR+dirname+"/")
			if(!dir.exists()){
				dir.mkdirs()
			}



			File file = new File( testScriptPath+FILE_SEPARATOR+scriptsDirName1+FILE_SEPARATOR+dirname+FILE_SEPARATOR+params?.name?.trim()+".py");
			if(!file.exists()){
				file.createNewFile()
			}
			File pyHeader = new File( "${request.getRealPath('/')}//fileStore//pyHeader.txt")
			def pyHeaderContentList = pyHeader?.readLines()
			String pyHeaderContent = ""
			pyHeaderContentList.each {
				pyHeaderContent += it?.toString()+"\n"
			}
			String data =pyHeaderContent+"'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+params?.scriptArea			
			
			//String data = "'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+params?.scriptArea
			file.write(data)
			if(params?.prevScriptName != params?.name && params?.prevScriptName?.trim() != params?.name?.trim()){
				//File file1 = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName1+"/"+dirname+"/"+params?.prevScriptName?.trim()+".py");
				File file1 = new File( testScriptPath+FILE_SEPARATOR+scriptsDirName1+FILE_SEPARATOR+dirname+FILE_SEPARATOR+params?.prevScriptName?.trim()+".py");
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
			scriptService.updateScriptNameChange(params?.prevScriptName,sFile, params?.category)
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
				script.setCategory(Utility.getCategory(params?.category))
				script.save(flush:true)
			}

			def sObject = new ScriptObject()
			sObject.setBoxTypes(bTypes)
			sObject.setRdkVersions(rdkVers)
			sObject.setName(params?.name?.trim())
			sObject.setModule(ptest?.module?.name)
			sObject.setScriptFile(script)
			sObject.setScriptTags(scrptTags)
			sObject.setLongDuration(longDuration)

			if(boxTypes){
				//			boxTypesList = scriptgroupService.createBoxTypeList(boxTypes)
				scriptgroupService.removeScriptsFromBoxScriptGroup(script,boxTypes,oldBoxTypes)
				//			scriptgroupService.removeScriptsFromBoxSuites1(script)
				if(isLongDuration != longDuration){
					scriptgroupService.updateScriptGroup(script,sObject, params?.category)
				}
				//			scriptgroupService.saveToDefaultGroup(script, boxTypesList)
			}

			scriptgroupService.saveToScriptGroups(script,sObject, params?.category)
			scriptgroupService.saveToDefaultGroups(script,sObject, bTypes,  params?.category)

			scriptgroupService.updateScriptsFromRDKVersionBoxTypeTestSuites1(script, sObject, params?.category)
			scriptgroupService.updateScriptsFromRDKVersionBoxTypeTestGroup(script,sObject,oldRDKVersions,oldBoxTypes)
			scriptgroupService.updateScriptsFromScriptTag(script,sObject,oldTags,oldBoxTypes)

			flash.message = message(code: 'default.updated.message', args: [
				message(code: 'script.label', default: 'Script'),
				params.name
			])
		}
		def newid= params?.id
		if(params?.id?.contains("@")){
			newid = params?.id?.split("@")[0]+"@"+params?.name
		}

		redirect(action: "list", params: [scriptId: newid])
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
		def category = params?.categoryFilter?.trim()
		def moduleMap = null
		def scriptNameList = []
		def scripts = []
		def searchName = params?.searchName?.trim()
		if(category.equals('RDKB_TCL')){
			scriptNameList = scriptService.getTCLNameList(getRealPath())
			if(searchName){
				if(scriptNameList.contains(searchName)){
					scripts.add(searchName)
				}
			}
			else{
				scripts = scriptNameList
			}
			
		}
		else{
			scriptNameList = scriptService.getScriptNameList(getRealPath(), category)
			moduleMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
			scriptNameList?.each {
				if(it?.toLowerCase()?.contains(searchName?.toLowerCase())){
					def moduleName = moduleMap.get(it)
					def script = scriptService.getScript(getRealPath(), moduleName, it, category)
					if(script){
						scripts.add(script)
					}
				}
			}
		}
		
		render(template: "searchList", model: [scriptList : scripts, category: category])
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

		def category = params?.category
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
			flash.message = message(code: 'default.updated.message', args: [message(code: 'scriptGroup.label', default: 'Test Suite'),scriptGroup])
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
				scriptGroupInstance.category = Utility.getCategory(category)
				selectedScripts.each{
					def moduleMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
					def moduleName = moduleMap.get(it?.key)
					def script = ScriptFile.findByScriptNameAndModuleName(it.key,moduleName)
					if(script){
						scriptGroupInstance.addToScriptList(script)
					}
					flash.message = message(code: 'default.created.message', args: [
						message(code: 'scriptGroup.label', default: 'Test Suite'),
						scriptGroupInstance.name
					])
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
		def scriptInstance = scriptService.getScript(getRealPath(), mName, params.scriptName, params?.category)
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
		def scriptInstance = scriptService.getScript(getRealPath(), mName, params.scriptName, params?.category)
		//		Script scriptInstance = Script.findByName(params.scriptName)
		if(scriptInstance){
			scriptInstanceList.add(mName+"@"+scriptInstance.name)
		}
		render scriptInstanceList as JSON
	}



	/**
	 * Method to trigger downloading the script content as python script file in script page.
	 * @return
	 */
	def exportScriptContent(){
		def opFail = false
		if(params?.id){
		  if(Category.RDKB_TCL.toString().equals(params?.category?.trim())){
			  if(!exportTclScript(params)){
				  opFail = true
			  }
		  }
		  else{
			  if(!exportScript(params)){
				  opFail = true
			  }
		  }
		  if(opFail){
			  flash.message = "Download failed. No valid script is available for download."
			  redirect(action: "list")
		  }
		}else{
			flash.message = "Download failed. No valid script is available for download."
			redirect(action: "list")
		}
	}

	/**
	 * Method to trigger downloading the script content as python script file from the execution result page.
	 * @return
	 */
	def exportScriptData(){
		if(params?.id){
			if(!exportScript(params)){
				flash.message = "Download failed. No valid script is available for download."
				render "Failed to download Script."
			}
		}else{
			flash.message = "Download failed. No valid script is available for download."
			render "Failed to download Script."
		}
	}

	/**
	 * Method to download the script content as pythoin file.
	 * @param params
	 * @return
	 */
	def exportScript(def params){
		def sMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
		def category = params?.category
		
		def moduleName = sMap.get(params?.id)
		def scriptDir = primitiveService.getScriptDirName(moduleName)
		if(category == null){
			category = primitiveService.getCategory(moduleName)
		}
		def path = getTestScriptPath(category) + FILE_SEPARATOR + scriptDir+ FILE_SEPARATOR +moduleName + FILE_SEPARATOR + params?.id+".py"
		File sFile = new File(path)
		if(sFile.exists()){
			params.format = "text"
			params.extension = "py"
			String data = new String(sFile.getBytes())
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ params?.id+".py\"")
			response.setHeader("Content-Length", ""+data.length())
			response.outputStream << data.getBytes()
		}else {
			flash.message = "Download failed. No valid script is available for download."
			redirect(action: "list")
		}
	}
	
	/**
	 * Method to download the script content as tcl file.
	 * @param params
	 * @return
	 */
	def exportTclScript(def params){
		def category = params?.category
		def path = Utility.getTclDir(getRealPath())+FILE_SEPARATOR + params?.id+".tcl"
		File sFile = new File(path)
		if(sFile.exists()){
			params.format = "text"
			params.extension = "tcl"
			String data = new String(sFile.getBytes())
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ params?.id+".tcl\"")
			response.setHeader("Content-Length", ""+data.length())
			response.outputStream << data.getBytes()
		}else {
			flash.message = "Download failed. No valid script is available for download."
			redirect(action: "list")
		}
	}


	/***
	 *  Downloads tcl script
	 */
	def exportTCL(){
		def scriptName = params?.scriptName?.trim()
		def path = getTestScriptPath(Category.RDKB_TCL.toString())
		File file = new File(path + FILE_SEPARATOR + scriptName + ".tcl")
		if(file.exists()){
			params.format = "text"
			params.extension = "tcl"
			String data = new String(file.getBytes())
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ scriptName+".tcl\"")
			response.setHeader("Content-Length", ""+data.length())
			response.outputStream << data.getBytes()
		}else {
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
		removeLock(params?.scriptName)
	}
	
	private void removeLock(def scriptName){
		ScriptService.scriptLockList.remove(scriptName)
	}

	/**
	 * REST method to retrieve the script list 
	 * @param scriptGroup
	 * @return
	 */
	def getScriptsByScriptGroup(String scriptGroup){
		JsonObject scriptJson = new JsonObject()
		try {
			if(scriptGroup){
				ScriptGroup sg = ScriptGroup.findByName(scriptGroup)
				if(sg){
					JsonArray scriptArray = new JsonArray()
					scriptJson.add(scriptGroup, scriptArray)
					sg?.scriptList?.each { scrpt ->
						JsonObject script = new JsonObject()
						script.addProperty("name", scrpt?.scriptName)
						script.addProperty("module", scrpt?.moduleName)
						scriptArray?.add(script)
					}
				}else{
					scriptJson.addProperty("status", "failure")
					scriptJson.addProperty("remarks", "No script groups found with name "+scriptGroup)
				}
			}else{
				Map sgMap = scriptService?.getScriptsMap(getRealPath())
				sgMap?.keySet().each { key ->
					List sList = sgMap.get(key)
					if(sList){
						JsonArray scriptArray = new JsonArray()
						scriptJson.add(key, scriptArray)
						sList?.each{sname ->
							ScriptFile scrpt = ScriptFile.findByScriptNameAndModuleName(sname,key)
							if(scrpt){
								JsonObject script = new JsonObject()
								script.addProperty("name", scrpt?.scriptName)
								scriptArray?.add(script)
							}
						}
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		render scriptJson
	}

	/**
	 * REST method to retrieve the script list
	 * @param moduleName
	 * @return
	 */
	def getScriptsByModule(String moduleName){
		JsonObject scriptJson = new JsonObject()
		try {
			if (moduleName){
				Map sgMap = scriptService?.getScriptsMap(getRealPath())
				List sList = sgMap.get(moduleName)
				if(sgMap){
					JsonArray scriptArray = new JsonArray()
					scriptJson.add(moduleName, scriptArray)
					sList?.each{sname ->
						ScriptFile scrpt = ScriptFile.findByScriptNameAndModuleName(sname,moduleName)
						if(scrpt){
							JsonObject script = new JsonObject()
							script.addProperty("name", scrpt?.scriptName)
							scriptArray?.add(script)
						}
					}
				}else{
					scriptJson.addProperty("status", "failure")
					scriptJson.addProperty("remarks", "no module found with name "+moduleName)
				}
			}else{
				Map sgMap = scriptService?.getScriptsMap(getRealPath())
				sgMap?.keySet().each { key ->
					List sList = sgMap.get(key)
					if(sList){
						JsonArray scriptArray = new JsonArray()
						scriptJson.add(key, scriptArray)
						sList?.each{sname ->
							ScriptFile scrpt = ScriptFile.findByScriptNameAndModuleName(sname,key)
							if(scrpt){
								JsonObject script = new JsonObject()
								script.addProperty("name", scrpt?.scriptName)
								scriptArray?.add(script)
							}
						}
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		render scriptJson
	}

	/**
	 * REST API :  The function implements for get all Script group details  
	 * @return
	 */

	def getAllScriptGroups(){
		JsonObject scriptGrpObj = new JsonObject()
		JsonArray scripts = new JsonArray()
		def scriptCount = 0
		try{
			def scriptGrpList  = ScriptGroup.list()
			scriptGrpList?.each{scriptGrpName ->
				JsonObject scriptGrp = new JsonObject()
				scriptCount = scriptGrpName?.scriptList?.size()
				scriptGrp?.addProperty("name",scriptGrpName.toString())
				scriptGrp?.addProperty("scriptcount",scriptCount.toString())
				scripts.add(scriptGrp)
			}
			scriptGrpObj.add("scriptgroups",scripts)
		}catch(Exception e){
		}

		render scriptGrpObj
	}

	/**
	 * REST API :
	 * function used to delete test suite
	 * @param suiteName
	 * @return
	 */
	def deleteScriptGroup(final String scriptGroup){

		JsonObject scriptGrp = new JsonObject()
		try{
			Subject currentUser = SecurityUtils.getSubject()
			if(currentUser?.hasRole('ADMIN')){
				def scriptGroupInstance = ScriptGroup?.findByName(scriptGroup)
				if(scriptGroupInstance){
					if(scriptGroupInstance?.delete(flush :true)){
						scriptGrp?.addProperty("status", "SUCCESS")
						scriptGrp?.addProperty("remarks","ScriptGroup deleted successfully " )
					}else{
						if(ScriptGroup?.findByName(scriptGroup)){
							scriptGrp?.addProperty("status", "FAILURE")
							scriptGrp?.addProperty("remarks","Error in Deleting ScriptGroup" )
						}else{
							scriptGrp?.addProperty("status", "SUCCESS")
							scriptGrp?.addProperty("remarks","ScriptGroup deleted successfully " )
						}
					}

				}else{
					scriptGrp?.addProperty("status", "FAILURE")
					scriptGrp?.addProperty("remarks","no script group found with name "+ scriptGroup)
				}
			}else{
				scriptGrp?.addProperty("status", "FAILURE")
				if(currentUser?.principal){
					scriptGrp?.addProperty("remarks","current user ${currentUser?.principal} don't have permission to delete script group" )
				}else{
					scriptGrp?.addProperty("remarks","login as admin user to perform this operation" )
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}
		render scriptGrp
	}


	private String getTestScriptPath(def category){
		def path = null
		category = Utility.getCategory(category?.trim())
		switch(category){
			case Category.RDKV: path =  getRealPath() +  "fileStore"+FILE_SEPARATOR + FileStorePath.RDKV.value()
				break;
			case Category.RDKB: path = getRealPath() + "fileStore" + FILE_SEPARATOR + FileStorePath.RDKB.value()
				break;
			case Category.RDKB_TCL: path = getRealPath()  + "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
				break;
			default:
				break;
		}
		return path
	}


	/**
	 * REST API :- create a new suite
	 * params : file uploaded through the Curl command
	 * Eg : curl http://localhost:8080/rdk-test-tool/scriptGroup/
	 */

	def createNewScriptGroup(){
		JsonObject scriptGroup = new JsonObject()
		ScriptGroup scriptGroupInstance = new ScriptGroup()
		def fileName
		String xml
		def node
		String category = ""
		String  idList
		boolean valid = false
		if(params?.scriptGroupXml){
			def uploadedFile = request.getFile('scriptGroupXml')
			if(uploadedFile?.originalFilename?.endsWith(".xml")){
				fileName = uploadedFile?.originalFilename?.replace(".xml","")
				InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
				def fileContent = reader?.readLines()
				if(ScriptGroup.findByName(fileName.trim())){
					scriptGroup?.addProperty("STATUS","FAILURE")
					scriptGroup.addProperty("Remarks","The test suite name already exists")
				}else{
					if(fileContent){
						try{
							String s = ""
							int indx = 0
							String scriptContent = ""
							if(fileContent.get(indx))	{
								while(indx < fileContent.size()){
									s = s + fileContent.get(indx)+"\n"
									indx++
								}
							}
							xml = s
							XmlParser parser = new XmlParser();
							node = parser.parseText(xml)
							category = node?.script_group?.category?.text()
							List<String> names = new ArrayList<String>()
							node?.script_group?.scripts?.script_name?.each{
								names.add(it.text())
							}

							idList =  names
							idList = idList?.replace(SQUARE_BRACKET_OPEN,"")
							idList = idList?.replace(SQUARE_BRACKET_CLOSE,"")
						}catch(Exception e){
							scriptGroup?.addProperty("STATUS","FAILURE")
							scriptGroup.addProperty("Remarks","Invalid xml tags  ")
						}
						if(idList.equals("")){
							scriptGroup?.addProperty("STATUS","FAILURE")
							scriptGroup.addProperty("Remarks"," scripts  name list is empty  ")
						}else{
							try{
								StringTokenizer st = new StringTokenizer(idList,",")
								while(st.hasMoreTokens()){
									String token = st.nextToken()
									if(token && token.size()>0){
										ScriptFile sctFile = ScriptFile.findByScriptName(token?.trim())
										if( sctFile != null  && !scriptGroupInstance?.scriptList?.contains(sctFile)){
											scriptGroupInstance.addToScriptList(sctFile)
											valid = true
										}
									}
								}
								if(valid){
									scriptGroupInstance.name = fileName
									scriptGroupInstance.category = Utility.getCategory(category)
									if(scriptGroupInstance.save(flush:true)){
										scriptGroup?.addProperty("STATUS","SUCCESS")
										scriptGroup.addProperty("Remarks","Script group created success fully ")
									}else{
										scriptGroup?.addProperty("STATUS","FAILURE")
										scriptGroup.addProperty("Remarks","Script Group not created  ")
									}
								}else {
									scriptGroup?.addProperty("STATUS","FAILURE")
									scriptGroup.addProperty("Remarks","Script name is not valid   ")
								}
							}catch(Exception e){
								println "ERRORS"+e.getMessage()
								scriptGroup?.addProperty("STATUS","FAILURE")
								scriptGroup.addProperty("Remarks","Invalid xml tags   ")
							}
						}
					}else{
						scriptGroup?.addProperty("STATUS","FAILURE")
						scriptGroup.addProperty("Remarks","File not Exists")
					}
				}
			}else{
				scriptGroup?.addProperty("STATUS","FAILURE")
				scriptGroup.addProperty("Remarks","file not in xml format ")
			}
		}else{
			scriptGroup?.addProperty("STATUS","FAILURE")
			scriptGroup.addProperty("Remarks","No file specified ")
		}
		render scriptGroup
	}

	def verifyScriptFile(String scriptName){
		ScriptFile scriptFile
		scriptFile = ScriptFile?.findByScriptName(scriptName)
		try {
			if(scriptFile && getScriptFileObj(getRealPath(), scriptFile?.moduleName,scriptFile?.scriptName) == null){
				def sgList = []
				def scriptGroups = ScriptGroup.where {
					scriptList { id == scriptFile?.id }
				}
				scriptGroups?.each{ scriptGrp ->
					sgList.add(scriptGrp?.id)
				}

				sgList?.each{ sId ->
					def sGroup = ScriptGroup.findById(sId)
					sGroup?.scriptList?.removeAll(scriptFile)
					sGroup?.save()
				}
				scriptFile?.delete()
				render "Success fully updated"
			}else{
				render "Error"
			}
		} catch (Exception e) {
			render "Error"+e.getMessage()
			e.printStackTrace()
		}
	}


	def getScriptFileObj(realPath,dirName,fileName){
		dirName = dirName?.trim()
		fileName = fileName?.trim()
		Map script = [:]
		try {

			def moduleObj = Module.findByName(dirName)
			def scriptDirName = Constants.COMPONENT
			if(moduleObj){
				if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
					scriptDirName = Constants.INTEGRATION
				}
			}
			File file = new File( "${realPath}//fileStore//testscripts//"+scriptDirName+"//"+dirName+"//"+fileName+".py");

			if(file.exists()){
				return file;
			}
		} catch (Exception e) {
			script = null
			e.printStackTrace()
		}
		return null;
	}
	/**
	 * Function used to the newly added script automatically add the script list without stop and start the "apache-tomcat" server.
	 * The refresh the script list, while calling the  initializeScriptsData() same as boot process.
	 */
	/**
	 * Function used to the newly added script automatically add the script list without stop and start the "apache-tomcat" server.
	 * The refresh the script list, while calling the  initializeScriptsData() same as boot process.
	 */
	def scriptListRefresh(){
		def requestGetRealPath = request.getRealPath("/")
		def scriptGroupMap = scriptService.getScriptsMap(requestGetRealPath)
		def refreshStatus = scriptService.scriptListRefresh(realPath ,scriptGroupMap )
		if(refreshStatus){
			flash.message =  "Script lists are same not modified "
		} else {
			flash.message = " Script list refreshment completed successfully "
		}
		redirect( action :"list")

	}
	/**
	 * Function used to implement download script group in .xml file format
	 * @return
	 */
	def downloadXml(){
		def scriptGrpName  = ScriptGroup.findByName(params.name)
		String scriptGroupData = ""
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		try{
			xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
			xml.xml(){
				xml.script_group(){
					xml.category(scriptGrpName?.category?.toString())
					xml.scripts(){
						scriptGrpName?.scriptList.each{ scriptName ->
							xml.script_name(scriptName)
						}

					}
				}
			}
			scriptGroupData = writer.toString()
		}catch (Exception e){
			log.error "ERROR "+e.getMessage()
			e.printStackTrace()
		}
		if(scriptGroupData){
			params.format = "text"
			params.extension = "xml"
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ params?.name+".xml\"")
			response.setHeader("Content-Length", ""+scriptGroupData.length())
			response.outputStream << scriptGroupData.getBytes()
		}else{
			flash.message = "Download failed. Script Group data is not available."
			redirect(action: "list")
		}
	}

	/** This function used to uploading the new .xml fill in the test manager
	 * check the  .xml file or not
	 * check same script group is exists or not
	 * content of the file is same as the script group xml or not
	 * script list is empty or not
	 * return
	 */

	def upload() {
		def uploadedFile = request.getFile('file')
		String xmlContent = ""
		def node
		String s = ""
		String  idList
		String categ = ""
		int indx = 0
		if(uploadedFile){
			if( uploadedFile?.originalFilename?.endsWith(".xml")) {

				String fileName = uploadedFile?.originalFilename?.replace(".xml","")

				if(ScriptGroup.findByName(fileName?.trim())){
					flash.message= "Test Suite with same name already exists ..... "
				}else{
					InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
					def fileContent = reader?.readLines()
					if(fileContent){

						fileContent?.each{ xmlData->
							xmlContent += xmlData +"\n"

						}
						List<String> names = new ArrayList<String>()
						try{

							XmlParser parser = new XmlParser();
							node = parser.parseText(xmlContent)
							categ = node?.script_group?.category?.text()
							node.script_group.scripts.script_name.each{
								names.add(it.text())
							}
						}
						catch(Exception e){
							log.error "ERROR"+e.getMessage()
							e.printStackTrace()
						}
						try{


							if(names?.size() == 0){
								flash.message ="  Test suite xml doesnot contain valid script  list... "
							}else{
								ScriptGroup scriptGroupInstance = new ScriptGroup()
								scriptGroupInstance.category = Utility.getCategory(categ)
								names?.each{ token ->
									if(token && token.size()>0){
										ScriptFile sctFile = ScriptFile.findByScriptName(token?.trim())
										if( sctFile != null  && !scriptGroupInstance?.scriptList?.contains(sctFile)){
											scriptGroupInstance.addToScriptList(sctFile)
										}
									}
								}
								scriptGroupInstance.name = fileName.trim()
								if (!scriptGroupInstance.save(flush: true)) {
									flash.message = "File not uploaded"
								}else{
									flash.message = "File uploaded  successfully "
								}
							}
						}catch(Exception e ){
							log.error "ERROR "+ e.getMessage()
							flash.message = "XML data is not in correct format"
						}
					}
				}
			} else{
				flash.message="Error, The file extension is not in .xml format"
			}
		}else{
			flash.message="Not a valid file"
		}
		redirect(action:"list")
		return
	}
	
	def verifyScriptGroup(String scriptGroup,String category, String remove){
		ScriptGroup sg = ScriptGroup?.findByName(scriptGroup)
		def rPath = getRealPath()
		List removeList = []
		sg?.scriptList.each { script ->
			Map scriptInstance1 = scriptService.getScript(rPath,script?.moduleName, script?.scriptName, category)
			if(scriptInstance1 == null || scriptInstance1?.keySet()?.size() ==  0){
				if(remove?.equals("true")){
					removeList.add(script)
				}
			}
		}
		if(removeList?.size() > 0){
			def sGroup = ScriptGroup.findByName(scriptGroup)
			sGroup.scriptList.removeAll(removeList)
			sGroup.save(flush:true)
		}
		render "removedList "+removeList
	}
	
}