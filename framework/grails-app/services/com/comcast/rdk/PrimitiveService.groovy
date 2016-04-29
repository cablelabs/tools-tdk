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

import groovy.xml.XmlUtil

/**
 * Service class to handle the primitive xml
 *
 */
class PrimitiveService {
	
	public static volatile SortedMap primitiveModuleMap = new TreeMap(String.CASE_INSENSITIVE_ORDER);
	
	public static volatile Set primitiveList = []
	
	public static volatile Map primitiveMap = [:]
	
	public static TESTSCRIPTS_PATH = "/fileStore/testscripts/"
	
	def initializePrimitiveTests(def realPath){
		List primitiveTestList = []
		
		List dirList = [Constants.COMPONENT,Constants.INTEGRATION]
		dirList.each{ directory ->
		
		File scriptsDir = new File( "${realPath}${TESTSCRIPTS_PATH}"+directory+"/")
		if(scriptsDir.exists()){
			def modules = scriptsDir.listFiles()
			modules.each { module ->
				File [] files = module.listFiles(new FilenameFilter() {
					@Override
					public boolean accept(File dir, String name) {
						return name.endsWith(module?.name?.toString()?.trim()+".xml");
					}
				});
			def list = []
			files.each { file ->
				def lines = file?.readLines()
				int indx = lines?.findIndexOf { it.startsWith("<?xml")}
				String xmlComtent =""
				while(indx < lines.size()){
							xmlComtent = xmlComtent + lines.get(indx)+"\n"
							indx++
				}
				def parser = new XmlParser();
				def node = parser.parseText(xmlComtent?.toString())		
				//def node = new XmlParser().parse(file)
				def pList = []
				node.each{
						try {
							it.primitiveTests.each{
								it.primitiveTest.each {
									String pName = "${it.attribute('name')}"
									pName = pName?.trim()
									pList.add(pName)
									primitiveList.add(pName)
									primitiveModuleMap.put(pName,""+module.getName())
								}
							}
						} catch (Exception e) {
						e.printStackTrace()
					}
				   }
				
				primitiveMap.put(""+module.getName(), pList)
			}
		}
		
	}
		}
	}

    def getAllPrimitiveTest(def realPath){
		if(primitiveMap == null || primitiveMap.keySet().size() == 0){
			initializePrimitiveTests(realPath)
		}
		return primitiveMap
    }
	
	def getPrimitiveModuleMap(def realPath){
		if(primitiveModuleMap == null || primitiveModuleMap.keySet().size() == 0){
			initializePrimitiveTests(realPath)
		}
		return primitiveModuleMap
	}
	
	def getPrimitiveList(def realPath){
		if(primitiveList == null || primitiveList.size() == 0){
			initializePrimitiveTests(realPath)
		}
		return primitiveList
	}
	
	def addToPrimitiveList(def name,def module){
		if(!primitiveMap.containsKey(module)){
			primitiveMap.put(module,[])
		}
		primitiveMap.get(module)?.add(name)
		primitiveModuleMap.put(name, module)
		primitiveList.add(name)
	}
	
	def parsePrimitiveXml(def filePath){
		File primitiveXml = new File(filePath)
		def node = new XmlParser().parse(primitiveXml)
		def pList = []
		node.each{
			it.primitiveTests.each{
			 it.primitiveTest.each {
				 pList.add("${it.attribute('name')}")
			 }
			}
		   }
		return pList
	}
	
	def deletePrimitiveTest(def realPath,def primitiveTestName){
		def moduleName = primitiveModuleMap.get(primitiveTestName)
		primitiveList.removeAll(primitiveTestName)

		primitiveMap?.get(moduleName)?.remove(primitiveTestName)

		primitiveModuleMap.remove(primitiveTestName)
		
		def moduleObj = Module.findByName(moduleName)
		def scriptDirName = Constants.COMPONENT
		if(moduleObj){
			if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
				scriptDirName = Constants.INTEGRATION
			}
		}
		
		File primitiveFile = new File(realPath+"/fileStore/testscripts/"+scriptDirName+"/"+moduleName+"/"+moduleName+".xml")
		def root = new XmlSlurper().parse(primitiveFile)
		def primitiveNode = root.module.primitiveTests.primitiveTest.find{ it.@name == primitiveTestName }
		primitiveNode.replaceNode{}
		def writer = new FileWriter(primitiveFile)
		XmlUtil.serialize(root, writer)

		return true
	}
	def getScriptDirName(def moduleName){
		def moduleObj = Module.findByName(moduleName)
		def scriptDirName = Constants.COMPONENT
		if(moduleObj){
			if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
				scriptDirName = Constants.INTEGRATION
			}
		}
		return scriptDirName
	}
	def getPrimitiveTest(def filePath,def primitiveTestName){
		Map primitiveMap = [:]
		try {
			File primitiveXml = new File(filePath)
			//def local = new XmlParser()
			//def node = local.parse(primitiveXml)
			def lines = primitiveXml?.readLines()
			int indx = lines?.findIndexOf { it.startsWith("<?xml")}
			String xmlContent =""
			while(indx < lines.size()){
						xmlContent = xmlContent + lines.get(indx)+"\n"
						indx++
			}
			def parser = new XmlParser();			
			def node = parser.parseText(xmlContent?.toString())


			node.each{
				it.primitiveTests.each{
					it.primitiveTest.each {
						if("${it.attribute('name')}".equalsIgnoreCase(primitiveTestName)){
							primitiveMap.put("name", "${it.attribute('name')}")
							primitiveMap.put("version",  "${it.attribute('version')}")
							primitiveMap.put("id","${it.attribute('id')}")
							Set paramList = []
							def moduleName = primitiveModuleMap.get(primitiveTestName)
							primitiveMap.put("module",Module.findByName(moduleName))
							def fun = Function.findByModuleAndName(Module.findByName(moduleName),it.function.text())
							primitiveMap.put("function",fun)
							it.parameters.each {
								it.parameter.each{
									def pType = ParameterType.findByNameAndFunction("${it.attribute('name')}",fun)
									Map param = [:]
									param.put("parameterType",pType)
									param.put("value", "${it.attribute('value')}")
									paramList.add(param)
								}
								primitiveMap.put("parameters",paramList)
							}
							//				 return primitiveMap
						}else{
							def ss = "${it.attribute('name')}"
							if(ss == primitiveTestName){
							}
						}
					}
				}
			}
		} catch (Exception e) {
			primitiveMap = null
			e.printStackTrace()
		}
		return primitiveMap
	}
}
