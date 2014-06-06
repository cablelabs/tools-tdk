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

import java.util.Map;

import org.springframework.dao.DataIntegrityViolationException
import com.google.gson.JsonObject
import grails.converters.JSON
import org.apache.shiro.SecurityUtils

class PrimitiveTestController {

    static allowedMethods = [save: "POST", update: "POST", delete: "POST"]
        
    def primitivetestService

	def utilityService
	
    def index() {
        redirect(action: "list", params: params)
    }

    def list() {     
		def primitiveTestList = PrimitiveTest.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(), [order: 'asc', sort: 'name'])
		def primitiveTestMap = createPrimitiveTestMap(primitiveTestList);
        [primitiveTestInstanceList: primitiveTestList, primitiveTestInstanceTotal: primitiveTestList.size(),primitiveTestMap:primitiveTestMap]
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
	def getParameters() {
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
		def primitiveTestList = PrimitiveTest.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(), [order: 'asc', sort: 'name'])
		//def primitiveTestList = PrimitiveTest.list([order: 'asc', sort: 'name'])
		def primitiveTestMap = createPrimitiveTestMap(primitiveTestList);
		[primitiveTestList : primitiveTestList, error: params.error, primitiveTestId: params.primitiveTestId, primitiveTestCount : PrimitiveTest.count(),,primitiveTestMap:primitiveTestMap]
	}

	
	/**
	 * TODO: Complete java doc
	 * @return
	 * 
	 * @author subrata
	 */
    def save() {
		def error = ''
		PrimitiveTest.withTransaction { status ->
			try {                
                if(PrimitiveTest.findByName(params?.testName)){
					render("Duplicate PrimitiveTest Name not allowed. Try Again")
                }
                else{                    
                    def primitiveTest = new PrimitiveTest()                                        
                    primitiveTest.name = params?.testName
                    primitiveTest.module = Module.get(params?.module as Long)
                    primitiveTest.function = Function.get(params?.functionValue as Long)
					primitiveTest.groups = utilityService.getGroup()
                    if(! primitiveTest.save()) {
                        log.error "Error saving PrimitiveTest instance : ${primitiveTest.errors}"
						render("Error saving PrimitiveTest. Try Again.")
                    }
                    else{
                        if(params.parameterTypeIds) {
                            params.parameterTypeIds.split(", ").each {
                                if(it) {
                                    def value = params["value_${it}"]
                                    def parameterType = ParameterType.get(it as Long)
                                    def parameter = new Parameter()
                                    parameter.parameterType = parameterType
                                    parameter.value = value ?: ''
                                    if(parameter.save()) {
                                        primitiveTest.addToParameters(parameter)                                        
                                     
										render(message(code: 'default.created.message', args: [
                                                message(code: 'primitiveTest.label', default: 'Primitive Test'),
                                                primitiveTest.name
                                            ]))
                                    }
                                    else {
										render("&emsp;Error creating Primitive Test. Please make sure that all the inputs are valid. \n")
                                        log.error "Error saving Parameter : ${parameter.errors}"
                                        throw new RuntimeException("Value not supported")
                                    }
                                }
                            }
                        }
                        else{
                         
							render(message(code: 'default.created.message', args: [
                                message(code: 'primitiveTest.label', default: 'Primitive Test'),
                                primitiveTest.name
                            ]))
                        }
                    }
                }				
				status.flush()
			}
			catch(Throwable th) {
				status.setRollbackOnly()
			}
		}
    }
	
    def deleteTest() {
        Long id = params.id as Long
        PrimitiveTest primitiveTestInstance = PrimitiveTest.get(id)
        if (!primitiveTestInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveTestInstance?.name])
            redirect(action: "create")
            return
        }
		def script = Script.findByPrimitiveTest(primitiveTestInstance)	
		if(script){
			flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveTestInstance?.name])
            render("success")
			return
		}	
        try {
          primitiveTestInstance.delete(flush: true)
          flash.message = message(code: 'default.deleted.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveTestInstance?.name])
          render("success")
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveTestInstance?.name])
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
		def primitiveTest = PrimitiveTest.get(params.id as Long)
		def functions = Function.findAllByModule(primitiveTest.module)
		def parameterTypes = ParameterType.findAllByFunction(primitiveTest.function)	
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
		def primitiveTest = PrimitiveTest.get(id)
		def error
		if (version != null) {
			if (primitiveTest.version > version) {
				primitiveTest.errors.rejectValue("version", "default.optimistic.locking.failure",
						  [message(code: 'primitiveTest.label', default: 'PrimitiveTest')] as Object[],
						  "Another user has updated this PrimitiveTest while you were editing")
				render(view: "create", model: [primitiveTest: primitiveTest])
				return
			}
		}		
		
		PrimitiveTest.withTransaction { status ->
			try {
				def parameters = primitiveTest.parameters
				primitiveTest.parameters = null
				parameters.each { it.delete(flush: true) }

				if(params.parameterTypeIds) {
					params.parameterTypeIds.split(", ").each {
						if(it) {
							def value = params["value_${it}"]
							def parameterType = ParameterType.get(it as Long)
							def parameter = new Parameter()
							parameter.parameterType = parameterType
							parameter.value = value ?: ''
							if(parameter.save(validate: true, flush: true)) {
								parameter.primitiveTest = primitiveTest
                                flash.message = message(code: 'default.updated.message', args: [
                                    message(code: 'primitiveTest.label', default: 'PrimitiveTest'),
                                    primitiveTest.name
                                ])
							}
							else {
								error += "Error Updating Primitive Test - '${primitiveTest.name}'. Please make sure that all the inputs are valid. \n"
								log.error "Error saving Parameter : ${parameter.errors}"
								throw new RuntimeException("Value not supported")
							}
						}
					}
				}              
				status.flush()
			}
			catch(Throwable th) {
				status.setRollbackOnly()
			}
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
        PrimitiveTest primitiveTest = PrimitiveTest.findByName(testName)
        render primitivetestService.getJsonData( primitiveTest, idVal )
    }
    
    /**
     * Returns JSON data of stream details based on the
     * streamId received
     * @param idVal
     * @return
     */
    def getStreamDetails(final String idVal, final String stbIp) {
        Device device = Device.findByStbIp(stbIp.trim())    
        JsonObject outData = new JsonObject()
        String boxtype = device?.boxType?.type.toLowerCase()
        if(boxtype?.equals( BOXTYPE_CLIENT ))
        {
            String gateway = device?.gatewayIp.toString()
            Device gatewayDevice =  Device.findByStbName(gateway.trim())               
            if(gateway) {
                StreamingDetails streamingDetails = StreamingDetails.findByStreamId(idVal)
                DeviceStream deviceStream = DeviceStream.findByDeviceAndStream( gatewayDevice, streamingDetails )            
                outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
                outData.addProperty(KEY_GATEWAYIP, gatewayDevice?.stbIp.toString());
                outData.addProperty(KEY_CHANNELTYPE, streamingDetails?.channelType.toString());
                outData.addProperty(KEY_OCAPID, deviceStream?.ocapId.toString());
                outData.addProperty(KEY_RECORDERID, gatewayDevice?.recorderId.toString());
                outData.addProperty(KEY_AUDIOFORMAT, streamingDetails?.audioFormat.toString());
                outData.addProperty(KEY_VIDEOFORMAT, streamingDetails?.videoFormat.toString());
            }  
        } 
        else{
            StreamingDetails streamingDetails = StreamingDetails.findByStreamId(idVal)
            DeviceStream deviceStream = DeviceStream.findByDeviceAndStream( device, streamingDetails )
            outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
            outData.addProperty(KEY_GATEWAYIP, device?.stbIp.toString());
            outData.addProperty(KEY_CHANNELTYPE, streamingDetails?.channelType.toString());
            outData.addProperty(KEY_OCAPID, deviceStream?.ocapId.toString());
            outData.addProperty(KEY_RECORDERID, device?.recorderId.toString());
            outData.addProperty(KEY_AUDIOFORMAT, streamingDetails?.audioFormat.toString());
            outData.addProperty(KEY_VIDEOFORMAT, streamingDetails?.videoFormat.toString());
        }  
        render outData
    }
	
	
	/**
	 * Method to check whether Primitive Test with same Name exist or not. If yes returns the id of Primitive Test
	 * @return
	 */
	def fetchPrimitiveTest(){

		List primitiveTestInstanceList = []
		PrimitiveTest primitiveTestInstance = PrimitiveTest.findByName(params.testName)
		if(primitiveTestInstance){

			primitiveTestInstanceList.add(primitiveTestInstance.id)
		}
		render primitiveTestInstanceList as JSON
	}
	
}
