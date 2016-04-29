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
import grails.converters.JSON
import groovy.xml.MarkupBuilder
import groovy.xml.XmlUtil

import org.springframework.dao.DataIntegrityViolationException

import com.google.gson.JsonObject

class PrimitiveTestController {

    static allowedMethods = [save: "POST", update: "POST", delete: "POST"]
        
    def primitivetestService
	
	def primitiveService

	def utilityService
	
    def index() {
        redirect(action: "list", params: params)
    }

    def list() { 
    	def primitiveTestList = primitiveService.getAllPrimitiveTest(request.getRealPath("/"))
        [primitiveTestInstanceList: primitiveTestList, primitiveTestInstanceTotal: primitiveTestList.size()]
    }
	
	/**
	 * Method to create the filtered script list based on module
	 * @param scriptInstanceList
	 * @return
	 */
	private Map createPrimitiveTestMap(def primitiveTestList ){
		List primitiveList = []
		Map primitiveTestMap = [:]
		primitiveTestList.each { primitiveTest ->
				String moduleName = primitiveTest.getModule().getName();
				List subList = primitiveTestMap.get(moduleName);
				if(subList == null){
					subList = []
					primitiveTestMap.put(moduleName, subList);
				}
				subList.add(primitiveTest)
		}
		return primitiveTestMap
	}
	
	/**
	 * TODO: Complete java doc
	 * @return
	 * @author subrata
	 */
	def template() {
		def moduleInstanceList = Module.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(), [order: 'asc', sort: 'name'])
		[moduleInstanceList : moduleInstanceList]
	}
	
	
	/**
	 * TODO: Complete java doc
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
	 * TODO: Compete java doc
	 * @return
	 * 
	 * @author subrata
	 */
	def getParameters1() {
		if(! params.functionId) {
			render "No function id found"
			return
		}
		
		def function = Function.get(params.functionId as Long)
		if(! function) {
			render "Function not found with id : ${params.functionId}"
		}
		
		def parameters = []
		def parameterTypes = ParameterType.withCriteria {
			eq ('function', function)
			order('name')
		}
		
		parameterTypes.each { 
			def result = [id: it.id, name: it.name, range: it.rangeVal, type: it.parameterTypeEnum?.toString()]
			parameters += result
		}
		render parameters as JSON
	}

	/**
	 * TODO: Complete java doc
	 * @return
	 * 
	 * @author subrata
	 */
	def create() {
		def primitiveTestList = primitiveService.getPrimitiveList(getRealPath())
		def primitiveTestMap =  primitiveService.getAllPrimitiveTest(getRealPath())
		[primitiveTestList : primitiveTestList, error: params.error, primitiveTestId: params.primitiveTestId, primitiveTestCount : PrimitiveTest.count(),,primitiveTestMap:primitiveTestMap]
	}

	def getRealPath(){
		request.getRealPath("/")
	}
	
	def getPrimitiveFilePath(def moduleName){
		def scriptDirName = primitiveService.getScriptDirName(moduleName)
		return getRealPath()+"/fileStore/testscripts/"+scriptDirName+"/"+moduleName+"/"+moduleName+".xml"
	}
	
	def getPrimitiveFileDirectory(def moduleName){
		def scriptDirName = primitiveService.getScriptDirName(moduleName)
		return getRealPath()+"/fileStore/testscripts/"+scriptDirName+"/"+moduleName+"/"
	}
	
	/**
	 * TODO: Complete java doc
	 * @return
	 * 
	 * @author subrata
	 */
    def save() {
		def error = ''
			try {      
				def primitiveList = primitiveService.getPrimitiveList(getRealPath())   
                if(primitiveList.contains(params?.testName)){
					render("Duplicate PrimitiveTest Name not allowed. Try Again")
                }
                else{                    
                    def moduleObj = Module.get(params?.module as Long)
                    def fun = Function.get(params?.functionValue as Long)
					
					def primitiveFile = new File(getPrimitiveFilePath(moduleObj?.getName()))
					
					if(primitiveFile.exists()){
						def data = primitiveFile.readBytes()
					def root = new XmlSlurper().parse(primitiveFile)
					def list1 = []
                        if(params.parameterTypeIds) {
                            params.parameterTypeIds.split(", ").each {
                                if(it) {
                                    def value = params["value_${it}"]
                                    def parameterType = ParameterType.get(it as Long)
									
									def pMap = [:]
									pMap.put("parameterType",parameterType?.name)
									pMap.put("value",value ?: '')
									list1.add(pMap)
                                }
                            }
							def funName = fun?.getName()
							root?.module?.primitiveTests?.appendNode{
								primitiveTest(name :params?.testName,id:" ",version: "1"){
								function(fun?.getName())
								parameters{
								list1.each { p ->
									parameter("name":p?.parameterType,"value":p?.value)
								}
								}
							}
							}
                        }
                        else{
                         
							root?.module?.primitiveTests?.appendNode{
								primitiveTest(name :params?.testName,id:'',version:'1'){
								function(fun?.getName())
									parameters()
							}
							}
							
                        }
//                    }
                    try {
						  def writer = new FileWriter(primitiveFile)
                    XmlUtil.serialize(root, writer)
                   if( primitiveService.addToPrimitiveList(params?.testName,moduleObj.getName()))
				   {
					   render "PrimitiveTest created successully"
				   }
				   else
				   {	
					   render "PrimitiveTest not created successully "
				   }
				   
					} catch (Exception e) {
						primitiveFile.write(new String(data))
						e.printStackTrace()
					}
//					render(message(code: 'default.created.message', args: [
//						message(code: 'primitiveTest.label', default: 'Primitive Test'),
//						params?.testName
//					]))
					}else{
						if(moduleObj){
							def list1 = []
							if(params.parameterTypeIds) {
								params.parameterTypeIds.split(", ").each {
									if(it) {
										def value = params["value_${it}"]
										def parameterType = ParameterType.get(it as Long)
										
										def pMap = [:]
										pMap.put("parameterType",parameterType?.name)
										pMap.put("value",value ?: '')
										list1.add(pMap)
									}
								}
							}
								def funName = fun?.getName()
							try {
								def writer = new StringWriter()
								def xml = new MarkupBuilder(writer)
								xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
								xml.xml(){
									
									xml.module("name":moduleObj?.name, "testGroup":moduleObj.testGroup){
										
										
										xml.primitiveTests(){
											
											xml.primitiveTest(name : params?.testName, id : '' , version :'1' ){
												xml.function(funName)
												if(list1.size()> 0){
													xml.parameters(){
														list1.each { p ->
														xml.parameter("name":p?.parameterType,"value":p?.value)
														}
													}
												}else{
													xml.parameters()
												}
											}
										}
									}
								}
								String dirname = moduleObj?.name
										dirname = dirname?.trim()
												File dir = new File(getPrimitiveFileDirectory(dirname))
								
								if(!dir.exists()){
									dir.mkdirs()
								}
								
								File file = new File( getPrimitiveFilePath(dirname));
								if(!file.exists()){
									file.createNewFile()
								}
								
								File xmlHeader = new File( "${request.getRealPath('/')}//fileStore//xmlHeader.txt")
								def xmlHeaderContentList = xmlHeader?.readLines()
								String xmlHeaderContent = ""
								xmlHeaderContentList.each {
									xmlHeaderContent += it?.toString()+"\n"
								}
								file.write(xmlHeaderContent+writer.toString())
								//file.write(writer.toString())
								primitiveService.addToPrimitiveList(params?.testName,moduleObj.getName())
							} catch (Exception e) {
								e.printStackTrace()
							}
						}
					}
                }				
			}
			catch(Throwable th) {
			}
			
    }
	
    def deleteTest() {
		def primitiveName = params?.id
		def primitiveList = primitiveService.getPrimitiveList(getRealPath())
		if(!primitiveList.contains(primitiveName)){
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveName])
            redirect(action: "create")
            return
        }
		
        try {
			if(primitiveService.deletePrimitiveTest(getRealPath(), primitiveName)){
          flash.message = message(code: 'default.deleted.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveName])
          render("success")
			}else{
			flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveName])
            render("success")
			}
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveName])
            render("success")
        }
    }
    

	/**
	 * TODO: Complete java doc
	 * @return
	 * 
	 * @author subrata
	 */
	def getEditableTest() {
		def primitiveModuleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def module = primitiveModuleMap.get(""+params?.id)
		def primitiveTest =primitiveService.getPrimitiveTest(getPrimitiveFilePath(module), params?.id)
		def functions = Function.findAllByModule(primitiveTest?.module)
		def parameterTypes = ParameterType.findAllByFunction(primitiveTest?.function)	
		def ids = parameterTypes - (primitiveTest?.parameters?.parameterType)
		[primitiveTest: primitiveTest, functions: functions, paramTypes : parameterTypes, newParams : ids]
	}
	


	/**
	 * TODO: Complete java doc
	 * @param id
	 * @param version
	 * @return
	 * 
	 * @author subrata
	 */
    def update(Long id, Long version) {
		def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def moduleName = moduleMap.get(params?.id)
		def primitiveFilePath = getPrimitiveFilePath(moduleName)
		
		File ff =new File(primitiveFilePath);
		def data = ff.readBytes()
		def error
		long vers1 = 0
		if (params?.ptVersion != null) {
			try {
				def b = params?.ptVersion
				if( b instanceof String){
					vers1 = Long.parseLong(b)
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
		def fun = Function.get(params?.functionValue as Long)
		def primitiveFile = new File(primitiveFilePath)
		if(primitiveFile.exists()){
			//def root = new XmlSlurper().parse(primitiveFile)
			def lines = primitiveFile?.readLines()
			int indx = lines?.findIndexOf { it.startsWith("<?xml")}
			String xmlComtent =""
			while(indx < lines.size()){
						xmlComtent = xmlComtent + lines.get(indx)+"\n"
						indx++
			}
			def parser = new XmlParser();
			def root = parser.parseText(xmlComtent)

			def list1 = []
			if(params.parameterTypeIds) {
				params.parameterTypeIds.split(", ").each {
					if(it) {
						def value = params["value_${it}"]
						def parameterType = ParameterType.get(it as Long)

						def pMap = [:]
						pMap.put("parameterType",parameterType?.name)
						pMap.put("value",value ?: '')
						list1.add(pMap)
					}
				}
				def funName = fun?.getName()
				def pNode = root?.module?.primitiveTests?.primitiveTest?.find{ it.@name == params?.id }
				long vers2 = 0
							
							try {
								vers2 = Long.parseLong((""+pNode?.@version)?.trim())
							} catch (Exception e) {
								e.printStackTrace()
							}
				if(vers2 == vers1){
					vers2 ++
				
				pNode.replaceNode{
					primitiveTest(name :params?.id,id:" ",version: vers2){
						function(fun.getName())
						parameters(){
						list1.each { p ->
							parameter("name":p?.parameterType,"value":p?.value)
						}
						}
					}
				}
				
				try {
					OutputStreamWriter out = new OutputStreamWriter(new FileOutputStream(primitiveFile),"UTF-8");
					XmlUtil.serialize(root, out)
					flash.message = message(code: 'default.updated.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), params?.id])
				} catch (Exception e) {
					File ff1 =new File(primitiveFilePath);
					ff1.write(new String(data))
					flash.message = "Error in updating the primitive test" 
					e.printStackTrace()
				}
				}else{
					flash.message = "Another user has updated this PrimitiveTest while you were editing"
				}
				
			}
		}else{
			flash.message = "Error in updating the primitive test" 
		}
		
		redirect(action: 'create', params: [primitiveTestId: params.id,error: error])
		
    }
   
    
    public static boolean isFloat(String number){
        def status = true
        try
        {
          Float.parseFloat(number);
        }
        catch(NumberFormatException e)
        {
          status = false
        }
        return status
    }
    
    public static boolean isInteger(String str) {
        if (str == null) {
            return false;
        }
        int length = str.length();
        if (length == 0) {
            return false;
        }
        int i = 0;
        if (str.charAt(0) == '-') {
            if (length == 1) {
                return false;
            }
            i = 1;
        }
        for (; i < length; i++) {
            char c = str.charAt(i);
            if (c <= '/' || c >= ':') {
                return false;
            }
        }
        return true;
    }
    
    /**
     * Returns JSON data
     * @param testName
     * @param idVal
     * @return
     */
	def getJson(final String testName, final String idVal) {
		def scriptDirName
		def primitiveTest
		def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def mName= moduleMap.get(testName)
		try{
			if(mName){
				scriptDirName = primitiveService.getScriptDirName(mName)
				primitiveTest = primitiveService.getPrimitiveTest(getRealPath()+"/fileStore/testscripts/"+scriptDirName+"/"+mName+"/"+mName+".xml", testName)
			}
		}catch(Exception e){
			println e.getMessage()
		}
		render primitivetestService.getJsonData( primitiveTest, idVal )
	}
    
       /**
     * Returns JSON data of stream details based on the
     * streamId received
     * @param idVal
     * @return
     */
	def getStreamDetails(final String idVal, final String stbIp) {
		
		Device device = Device.findByStbIpAndIsChild(stbIp?.trim(),STAND_ALONE_DEVICE);
		JsonObject outData = new JsonObject()
		String boxtype = device?.boxType?.type?.toLowerCase()
		String deviceNotFound = "Device not found"
		if(device){
		if(boxtype?.equals( BOXTYPE_CLIENT ) ) {
			String gateway = device?.gatewayIp.toString()
			Device gatewayDevice =  Device.findByStbName(gateway.trim())
			if(gateway) {

				if(idVal?.startsWith("R")){
					RadioStreamingDetails streamingDetails = RadioStreamingDetails.findByStreamId(idVal)
					DeviceRadioStream deviceStream = DeviceRadioStream.findByDeviceAndStream( gatewayDevice, streamingDetails )
					outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
					outData.addProperty(KEY_GATEWAYIP, gatewayDevice?.stbIp?.toString());
					outData.addProperty(KEY_CHANNELTYPE, "radio");
					outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
					outData.addProperty(KEY_RECORDERID, gatewayDevice?.recorderId?.toString());
					outData.addProperty(KEY_AUDIOFORMAT, "N/A");
					outData.addProperty(KEY_VIDEOFORMAT, "N/A");
				}else{
					StreamingDetails streamingDetails = StreamingDetails.findByStreamId(idVal)
					DeviceStream deviceStream = DeviceStream.findByDeviceAndStream( gatewayDevice, streamingDetails )
					outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
					outData.addProperty(KEY_GATEWAYIP, gatewayDevice?.stbIp?.toString());
					outData.addProperty(KEY_CHANNELTYPE, streamingDetails?.channelType?.toString());
					outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
					outData.addProperty(KEY_RECORDERID, gatewayDevice?.recorderId?.toString());
					outData.addProperty(KEY_AUDIOFORMAT, streamingDetails?.audioFormat?.toString());
					outData.addProperty(KEY_VIDEOFORMAT, streamingDetails?.videoFormat?.toString());
				}
			}
		}else if(boxtype?.equals( BOXTYPE_STANDALONE_CLIENT )) {
			String gateway = device?.gatewayIp.toString()
			Device gatewayDevice =  Device.findByStbName(gateway.trim())
			if(gateway) {

				if(idVal?.startsWith("R")){
					RadioStreamingDetails streamingDetails = RadioStreamingDetails.findByStreamId(idVal)
					DeviceRadioStream deviceStream = DeviceRadioStream.findByDeviceAndStream( device, streamingDetails )
					outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
					outData.addProperty(KEY_GATEWAYIP, gatewayDevice?.stbIp?.toString());
					outData.addProperty(KEY_CHANNELTYPE, "radio");
					outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
					outData.addProperty(KEY_RECORDERID, gatewayDevice?.recorderId?.toString());
					outData.addProperty(KEY_AUDIOFORMAT, "N/A");
					outData.addProperty(KEY_VIDEOFORMAT, "N/A");
				}else{
					StreamingDetails streamingDetails = StreamingDetails.findByStreamId(idVal)
					DeviceStream deviceStream = DeviceStream.findByDeviceAndStream( device, streamingDetails )
					outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
					outData.addProperty(KEY_GATEWAYIP, gatewayDevice?.stbIp?.toString());
					outData.addProperty(KEY_CHANNELTYPE, streamingDetails?.channelType?.toString());
					outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
					outData.addProperty(KEY_RECORDERID, gatewayDevice?.recorderId?.toString());
					outData.addProperty(KEY_AUDIOFORMAT, streamingDetails?.audioFormat?.toString());
					outData.addProperty(KEY_VIDEOFORMAT, streamingDetails?.videoFormat?.toString());
				}
			}


		}else{

			if(idVal?.startsWith("R")){
				RadioStreamingDetails streamingDetails = RadioStreamingDetails.findByStreamId(idVal)
				DeviceRadioStream deviceStream = DeviceRadioStream.findByDeviceAndStream( device, streamingDetails )
				outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
				outData.addProperty(KEY_GATEWAYIP, device?.stbIp?.toString());
				outData.addProperty(KEY_CHANNELTYPE, "radio");
				outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
				outData.addProperty(KEY_RECORDERID, device?.recorderId?.toString());
				outData.addProperty(KEY_AUDIOFORMAT, "N/A");
				outData.addProperty(KEY_VIDEOFORMAT, "N/A");
			}else{
				StreamingDetails streamingDetails = StreamingDetails.findByStreamId(idVal)
				DeviceStream deviceStream = DeviceStream.findByDeviceAndStream( device, streamingDetails )
				outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
				outData.addProperty(KEY_GATEWAYIP, device?.stbIp?.toString());
				outData.addProperty(KEY_CHANNELTYPE, streamingDetails?.channelType?.toString());
				outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
				outData.addProperty(KEY_RECORDERID, device?.recorderId?.toString());
				outData.addProperty(KEY_AUDIOFORMAT, streamingDetails?.audioFormat?.toString());
				outData.addProperty(KEY_VIDEOFORMAT, streamingDetails?.videoFormat?.toString());
			}
		}
		render outData
		}else{
			render deviceNotFound
		}
	}
	
	
	/**
	 * Method to check whether Primitive Test with same Name exist or not. If yes returns the id of Primitive Test
	 * @return
	 */
	def fetchPrimitiveTest(){

		List primitiveTestInstanceList = []
		
		def primitiveMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def moduleName = primitiveMap.get(params?.testName)
		if(moduleName){
		def primitiveTestInstance = primitiveService.getPrimitiveTest(getPrimitiveFilePath(moduleName), params?.testName)
		if(primitiveTestInstance){
			primitiveTestInstanceList.add(primitiveTestInstance.name)
		}
		}
		render primitiveTestInstanceList as JSON
	}
	
}
