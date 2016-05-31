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


/**
 * Service class to manage the script files in file store.
 *
 */
class ScriptService {
	
	public static volatile List scriptsList = []
	
	public static volatile List scriptNameList = []
	
	public static volatile Map scriptMapping = [:]
	
	public static volatile Map scriptGroupMap = [:]
	
	public static volatile Set scriptSet = []
	
	public static volatile List scriptLockList = []
	
	def primitiveService
	
	def scriptgroupService
	
	def updateScript(def script){
		scriptsList.add(script)
		scriptNameList.add(script?.scriptName)
		def list = scriptGroupMap.get(script?.moduleName)
		if(list == null){
			list = []
			scriptGroupMap.put(script?.moduleName,list)
		}
		list.add(script?.scriptName)
		
		scriptMapping.put(script?.scriptName,script?.moduleName)
	}
	
	def updateScriptNameChange(def oldName , def newScript){
		scriptNameList.add(oldName)
		scriptNameList.add(newScript?.scriptName)
		boolean removedOld = false
		Iterator<ScriptFile> iter = scriptsList.iterator()
		while(iter.hasNext()){
			def obj = iter.next()
			if(oldName.equals(obj.scriptName)){
				iter.remove()
				removedOld = true
			}
		}

		if(removedOld){
			scriptsList.add(newScript)
		}
		def list = scriptGroupMap.get(newScript?.moduleName)
		if(list == null){
			list = []
			scriptGroupMap.put(newScript?.moduleName,list)
		}
		list.remove(oldName)
		list.add(newScript?.scriptName)
		scriptMapping.remove(oldName)
		scriptMapping.put(newScript?.scriptName,newScript?.moduleName)
	}
	
	def deleteScript(def script){
		scriptsList.remove(script)
		scriptNameList.remove(script?.scriptName)
		def list = scriptGroupMap.get(script?.moduleName)
		if(list != null){
			list.remove(script?.scriptName)
		}
		scriptMapping.remove(script?.scriptName?.toString().trim())
	}

	def initializeScriptsData(def realPath){
		try {
			def list1 = scriptsList.collect()
			def scriptFileList = ScriptFile?.findAll()
			scriptsList.clear()
			List scriptList = []
			
			boolean updateReqd = isDefaultSGUpdateRequired(realPath)

			List dirList = [
				Constants.COMPONENT,
				Constants.INTEGRATION
			]
			def start = System.currentTimeMillis()
			dirList.each{ directory ->
				File scriptsDir = new File( "${realPath}//fileStore//testscripts//"+directory+"//")
				if(scriptsDir.exists()){
					def modules = scriptsDir.listFiles()
					
					Arrays.sort(modules);
					
					modules.each { module ->

						def start1 =System.currentTimeMillis()
						try {
							File [] files = module.listFiles(new FilenameFilter() {
										@Override
										public boolean accept(File dir, String name) {
											return name.endsWith(".py");
										}
									});
							def start2 = System.currentTimeMillis()
							def sLst = []
							files.each { file ->
								String name = ""+file?.name?.trim()?.replace(".py", "")
								def sFile
								ScriptFile.withTransaction {
									sFile = ScriptFile.findByScriptNameAndModuleName(name,module.getName())
									if(sFile == null){
										sFile = new ScriptFile()
										sFile.setModuleName(module?.getName())
										sFile.setScriptName(name)
										sFile.save(flush:true)
									}
								}
								if(!scriptsList.contains(sFile)){
									scriptsList.add(sFile)
									sLst.add(name)
									scriptMapping.put(name, module?.getName())
								}

								if(!scriptNameList.contains(name)){
									scriptNameList.add(name)
								}
								if(updateReqd == true){
									updateDefaultScriptGroups(realPath,name,module?.getName())
								}
							}

							sLst?.sort()
							scriptGroupMap.put(module?.getName(), sLst)
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
				}
			}
//			removeOrphanScriptFile(realPath,scriptFileList, scriptsList)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return scriptsList
	}
	def removeOrphanScriptFile(String realPath,List oldList , List newList){
		oldList.removeAll(newList)
		int indx = 0;
		List deleteFiles = []
		Map sgMap = [:]
		oldList?.each { scriptFile ->

			if(getScriptFileObj(realPath, scriptFile?.moduleName,scriptFile?.scriptName) == null){
				indx ++
				def scriptGroups = ScriptGroup.where {
					scriptList { id == scriptFile.id }
				}

				def scriptInstance
				def sgId = []
				boolean flag = false
				scriptGroups?.each{ scriptGrp ->
					flag = true
					def sList = sgMap.get(scriptGrp?.name)
					if(sList == null){
						sList = []
						sgMap.put(scriptGrp?.name,sList)
					}
					sList.add(scriptFile)
				}
				if(!flag){
					deleteFiles.add(scriptFile?.id)
				}
			}
		}
		
		
		sgMap?.keySet().each { sname ->
			try {
				ScriptGroup.withTransaction {
					ScriptGroup sGroup = ScriptGroup.findByName(sname)
					if(sGroup){
						List sList = sgMap.get(sname)
//						if(sList?.size() <= 7){
//							println " SG<<>><<> "+sname
//						sList?.each{ scriptInstance ->
//							sGroup.removeFromScriptList(scriptInstance)
//							sGroup?.scriptList?.removeAll(sList);
//							sGroup?.save(flush:true)
//						}
//						}
					}
				}
			} catch (Exception e) {
				println " ERROR "+sname+" ee "+e.getMessage()
				e.printStackTrace()
			}
		}
		
		
		deleteFiles?.each { sFileId ->
			ScriptFile.withTransaction {
				def sFile = ScriptFile.get(sFileId)
				if(sFile){
					sFile.delete()
				}
			}
		}
	}
  
	
	def removeFromSG(def sid , def scriptFile){
		def  scriptInstance
		ScriptGroup.withTransaction {
			ScriptGroup sGroup = ScriptGroup.get(sid)
			scriptInstance = sGroup?.scriptList?.find { it?.id == scriptFile?.id }
			if(scriptInstance){
				sGroup.removeFromScriptList(scriptInstance)
				sGroup.save(flush:true)
			}

			def scriptInstanceList = sGroup?.scriptList?.findAll { it?.id == scriptFile?.id }
			if(scriptInstanceList?.size() > 0){
				if(scriptInstance){
					sGroup?.scriptList?.removeAll(scriptInstance);
				}
			}
		}
	}
	def updateDefaultScriptGroups(def realPath, def name , def moduleName){
		try {
			def sFile
			ScriptFile.withTransaction{
				sFile= ScriptFile.findByScriptNameAndModuleName(name,moduleName)
			}
			if(sFile){
				def script = getMinimalScript(realPath,moduleName, name)
				if(script){
					def sObject = new ScriptObject()
					sObject.setBoxTypes(script?.boxTypes?.toSet())
					sObject.setRdkVersions(script?.rdkVersions.toSet())
					sObject.setName(name)
					sObject.setModule(moduleName)
					sObject.setScriptFile(sFile)
					sObject.setScriptTags(script?.scriptTags?.toSet())
					sObject.setLongDuration(script?.longDuration)

					ScriptGroup.withTransaction{
						scriptgroupService.saveToScriptGroups(sFile,sObject)
						scriptgroupService.saveToDefaultGroups(sFile,sObject, script?.boxTypes)
					}
					createDefaultGroupWithoutOS(sObject,sFile)
					createDefaultScriptTagGroup(sObject,sFile)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	def createDefaultGroupWithoutOS(def scriptObject , def scriptFile){
		def sName = scriptObject.getModule()
		Module module
		Module.withTransaction{
			module = Module.findByName(sName)
		}
		if(module?.testGroup != TestGroup.OpenSource){
			scriptObject?.boxTypes?.each{ bType ->

				scriptObject?.rdkVersions?.each{ vers ->

					String name = vers?.toString()+"_"+bType?.name+Constants.NO_OS_SUITE
					ScriptGroup.withTransaction {
						def scriptGrpInstance = ScriptGroup.findByName(name)
						if(!scriptObject?.getLongDuration()){
							if(!scriptGrpInstance){
								scriptGrpInstance = new ScriptGroup()
								scriptGrpInstance.name = name
							}
							if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptFile)){
								scriptGrpInstance.addToScriptList(scriptFile)
								scriptGrpInstance.save(flush:true)
							}
						}else{
							if(scriptGrpInstance && scriptGrpInstance?.scriptList?.contains(scriptFile)){
								scriptGrpInstance.removeFromScriptList(scriptFile)
							}
						}
					}
				}
			}
		}
	}
	
	
	def createDefaultScriptTagGroup(def scriptObject , def scriptFile){
			scriptObject?.boxTypes?.each{ bType ->

				scriptObject?.scriptTags?.each{ tag ->
					String name = tag?.toString()+"_"+bType?.name
					ScriptGroup.withTransaction {
						def scriptGrpInstance = ScriptGroup.findByName(name)
							if(!scriptGrpInstance){
								scriptGrpInstance = new ScriptGroup()
								scriptGrpInstance.name = name
							}
							if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptFile)){
								scriptGrpInstance.addToScriptList(scriptFile)
								scriptGrpInstance.save(flush:true)
							}
					}
				}
			}
	}
			
  
  def getScriptNameFileList(def realPath){
	  if(scriptsList == null || scriptsList.size() == 0){
		  initializeScriptsData(realPath)
	  }
	  return scriptsList
  }
  
  def getScriptNameModuleNameMapping(def realPath){
	  if(scriptMapping == null || scriptMapping.keySet().size() == 0){
		  initializeScriptsData(realPath)
	  }
	  return scriptMapping
  }
  
  def Map getScriptsMap(def realPath){
	  if(scriptGroupMap == null || scriptGroupMap.keySet().size() == 0){
		  initializeScriptsData(realPath)
	  }
	  return scriptGroupMap
  }
  
  def getScriptNameList(def realPath){
	  if(scriptNameList == null || scriptNameList.size() == 0){
		  initializeScriptsData(realPath)
	  }
	  return scriptNameList
  }
  /**
   * Function for return the total scripts list 
   * @param realPath
   * @return
   */
  
  def getScriptsList(def realPath ){
	  if( scriptsList == null || scriptsList.size() == 0 ){
		  initializeScriptsData(realPath)
	  }
	  return scriptsList
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
			}else{
				println " File Not present "+file?.getName()
			}
		} catch (Exception e) {
			println " file name "+fileName
			script = null
			e.printStackTrace()
		}
		return null;
	}
	
	def getScript(realPath,dirName,fileName){
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
				String s = ""
				List line = file.readLines()
				//int indx = 0
				int indx = line?.findIndexOf {  it.startsWith("'''")} 
				String scriptContent = ""
				if(line.get(indx).startsWith("'''"))	{
					indx++
					while(indx < line.size() &&  !line.get(indx).startsWith("'''")){
						if(!(line.get(indx)?.equals(""))){ //Issue fix  for line gap between xml tags
							s = s + line.get(indx)+"\n"
						}
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
				script.put("version", getIntegerValue(node.version.text()))
				script.put("name", node.name.text())
				def grpObj = null
				def grps = node?.groups_id?.text()
				if(grps){
					try {
						grpObj = Groups.findById(Integer.parseInt(grps))
					} catch (Exception e) {
						println " Error for script "+fileName+" = "+e.getMessage()
//						e.printStackTrace()
					}
				}
				script.put("groups",grpObj)
				script.put("skip", getBooleanValue(node.skip.text()))
				script.put("remarks",node?.remarks?.text())
				script.put("longDuration", getBooleanValue(node.long_duration.text()))
				def nodePrimitiveTestName = node.primitive_test_name.text()
				def primitiveMap = primitiveService.getPrimitiveModuleMap(realPath)
				def moduleName1 = primitiveMap.get(nodePrimitiveTestName)
				
				def moduleObj1 = Module.findByName(dirName)
				def primitiveDirName = Constants.COMPONENT
				if(moduleObj){
					if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
						primitiveDirName = Constants.INTEGRATION
					}
				}
				
				def primitiveTest = primitiveService.getPrimitiveTest(realPath+"/fileStore/testscripts/"+primitiveDirName+"//"+moduleName1+"/"+moduleName1+".xml",nodePrimitiveTestName)
				script.put("primitiveTest",primitiveTest)
				def versList = []
				def sTagList = []
				def btList = []
				Set btSet = node?.box_types?.box_type?.collect{ it.text() }
				Set versionSet = node?.rdk_versions?.rdk_version?.collect{ it.text() }
				Set scriptTagSet = node?.script_tags?.script_tag?.collect{ it.text() }
				btSet.each { bt ->
					btList.add(BoxType.findByName(bt))
				}
				versionSet.each { ver ->
					versList.add(RDKVersions.findByBuildVersion(ver))
				}
				scriptTagSet?.each { tag ->
					sTagList.add(ScriptTag.findByName(tag))
				}
				
				script.put("rdkVersions", versList)
				script.put("scriptTags", sTagList)
				script.put("boxTypes", btList)
				def statusText = node?.status?.text()
				script.put("status",getStatus(statusText) )
				script.put("synopsis", node?.synopsis?.text())
				script.put("scriptContent", scriptContent)
				script.put("executionTime", getExecutionTime(node?.execution_time?.text()))
			}else{
			}
		} catch (Exception e) {
			script = null
			e.printStackTrace()
		}
		return script
	}
	 
	 def getMinimalScript(realPath,dirName,fileName){
		 dirName = dirName?.trim()
		 fileName = fileName?.trim()
		 
		 def moduleObj = Module.findByName(dirName)
		 def scriptDirName = Constants.COMPONENT
		 if(moduleObj){
			 if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
				 scriptDirName = Constants.INTEGRATION
			 }
		 }
		 
		 File file = new File( "${realPath}//fileStore//testscripts//"+scriptDirName+"//"+dirName+"//"+fileName+".py");
		 
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
			 script.put("id", node?.id?.text())
			 script.put("version", getIntegerValue(node.version.text()))
			 script.put("name", node.name.text())
			 script.put("skip", getBooleanValue(node.skip.text()))
			 script.put("longDuration", getBooleanValue(node.long_duration.text()))
			 def versList = []
			 def btList = []
			 Set btSet = node?.box_types?.box_type?.collect{ it.text() }
			 Set versionSet = node?.rdk_versions?.rdk_version?.collect{ it.text() }
			 btSet.each { bt ->
				 btList.add(BoxType.findByName(bt))
			 }
			 versionSet.each { ver ->
				 versList.add(RDKVersions.findByBuildVersion(ver))
			 }
			 script.put("rdkVersions", versList)
			 script.put("boxTypes", btList)
		 }
		 return script
	 }
	 
	def getStatus(def statusText){
		Status status = Status.NOT_FOUND
		if(statusText){
			if(statusText == Status.ALLOCATED){
				status = Status.ALLOCATED
			}else if(statusText == Status.BUSY){
				status = Status.BUSY
			}else if(statusText == Status.FREE){
				status = Status.FREE
			}else if(statusText == Status.HANG){
				status = Status.HANG
			}else if(statusText == Status.TDK_DISABLED){
				status =  Status.TDK_DISABLED
			}
			else{
				status = Status.NOT_FOUND
			}
		}
		return status
	}
	
	def getExecutionTime(String exTime){
		int execTime = 2
		if(exTime){
			execTime = Integer.parseInt(exTime?.trim())
		}
		
		return execTime
	}
	
	def getBooleanValue(String bText){
		if(bText){
			if(bText?.trim() == "true"){
				return true
			}
		}
		return false
	}
	
	def getIntegerValue(String iText){
		int intVal
		if(iText){
			intVal = Integer.parseInt(iText?.trim())
		}
		return intVal
	}
	
	def isDefaultSGUpdateRequired(def realPath){
		try {
		Properties prop = new Properties();
		String fileName = realPath+"/fileStore/script.config";
		File ff = new File(fileName)
		if(ff.exists()){
			InputStream is = new FileInputStream(fileName);
			prop.load(is);
			def value = prop.getProperty("defaultScriptGroup");
			if(value){
				if(value.equals("true")){
					return true
				}
			}

		}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return false
	}
	
	
	
	def scriptListRefresh(def realPath , def totalScriptList){
		
		boolean  value1 =false
		try {
			def list1 = scriptsList.collect()
			scriptsList.clear()
			List scriptList = []
			boolean updateReqd = isDefaultSGUpdateRequired(realPath)
			List dirList = [
				Constants.COMPONENT,
				Constants.INTEGRATION
			]
			def start = System.currentTimeMillis()
			dirList.each{ directory ->
				File scriptsDir = new File( "${realPath}//fileStore//testscripts//"+directory+"//")
				if(scriptsDir.exists()){
					def modules = scriptsDir.listFiles()
					Arrays.sort(modules);
					modules.each { module ->
						def start1 =System.currentTimeMillis()
						try {
							File [] files = module.listFiles(new FilenameFilter() {
										@Override
										public boolean accept(File dir, String name) {
											return name.endsWith(".py");
										}
									});
							def start2 = System.currentTimeMillis()
							def sLst = []
							files.each { file ->
								String name = ""+file?.name?.trim()?.replace(".py", "")
								
								def sFile
								ScriptFile.withTransaction {
									sFile = ScriptFile.findByScriptNameAndModuleName(name,module.getName())
									if(sFile == null){
										sFile = new ScriptFile()
										sFile.setModuleName(module?.getName())
										sFile.setScriptName(name)
										sFile.save(flush:true)
									}
								}
								if(!scriptsList.contains(sFile)){
									scriptsList.add(sFile)
									sLst.add(name)
									scriptMapping.put(name, module?.getName())
								}

								if(!scriptNameList.contains(name)){
									scriptNameList.add(name)
								}
								if(updateReqd == true){
									updateDefaultScriptGroups(realPath,name,module?.getName())
								}
							}
							sLst.sort()
							totalScriptList?.each{ key, value ->
							if( key.toString()  ==  module.getName()?.toString()){
									if(!(value?.equals(sLst))){
										scriptGroupMap.put(module?.getName(), sLst)										
										value1 = false
									}else {
										value1 = true
									}
								}
							}
						} catch (Exception e) {
							println "ERROR"+e.getMessage()
							e.printStackTrace()
						}
					}
				}
			}
		} catch (Exception e) {
			log.error  "Error"+e.getMessage()
			e.printStackTrace()
		}
		return value1
	}
}
