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
import groovy.util.slurpersupport.GPathResult
import javax.xml.parsers.ParserConfigurationException;
import org.codehaus.groovy.grails.web.context.ServletContextHolder as SCH;
import org.xml.sax.SAXException;
import com.google.gson.JsonObject;

/**
 * Service class for the PrimitiveTest domain.
 *
 */
class PrimitivetestService {
	static datasource = 'DEFAULT'
    /**
     * Injects the grailsApplication.
     */
    def grailsApplication
  
    /**
     * Throws runtime exception with the specified message.
     * @param msg
     */
    private void abortTransaction(final String msg) {
        throw new RuntimeException(msg);
    }

  
    /**
     * Returns the JSON data corresponding to the PrimitiveData.
     * sample data is 
     * <pre>
     * {"id":1,"jsonrpc":"2.0","method":"play","params":{"locator":"3","frequency":"etre"}}
     * </pre>
     * @param primitiveTest
     * @return
     * @author ajith
     */
    public JsonObject getJsonData(final PrimitiveTest primitiveTest, String idValue) {
		
		if(idValue == null){
			idValue = ID_DEFAULT
		}
		
        log.info(" getJsonData ::::::::: "+primitiveTest?.name)        
        JsonObject outData = new JsonObject()
        if(primitiveTest){
            outData.addProperty(KEY_ID, idValue);
            outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
            outData.addProperty(KEY_METHOD, primitiveTest?.function?.name.trim());            
            Set<Parameter> parameters = primitiveTest?.getParameters();
            for ( Parameter parameter : parameters ) {
                if(parameter?.parameterType?.parameterTypeEnum.getTypeValue().equals("integer") ){
                    try{
                        int val = Integer.parseInt(parameter?.value);
                        outData.addProperty (parameter?.parameterType.name, val);
                    }catch (Exception e){
                        log.error("----Exception in converting to integer"+e.printStackTrace())
                    }
                }
				else if(parameter?.parameterType?.parameterTypeEnum.getTypeValue().equals("float") ){
					try{
					    
						float floatVal = Float.parseFloat(parameter?.value)
						outData.addProperty (parameter?.parameterType.name, floatVal);
					}catch (Exception e){
						log.error("----Exception in converting to float"+e.printStackTrace())
					}
				}
				else if(parameter?.parameterType?.parameterTypeEnum.getTypeValue().equals("double") ){
					try{
						
						double doubleVal = Double.parseDouble(parameter?.value)
						outData.addProperty (parameter?.parameterType.name, doubleVal);
					}catch (Exception e){
						log.error("----Exception in converting to float"+e.printStackTrace())
					}
				}				
                else{
                    outData.addProperty( parameter?.parameterType.name, parameter?.value.trim() );
                }
            }
        }      
        return outData
    }

}
