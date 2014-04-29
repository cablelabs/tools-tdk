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
    /**
     * Injects the grailsApplication.
     */
    def grailsApplication
    /**
     * Parses the stub xml file and stores that in the DB.
     * The stub xml location is placed in config.groovy 
     */
    public void parseAndSaveStubXml() {
        String xmlFile =  SCH.servletContext.getRealPath( grailsApplication.config.modules.xmlfile.location );
        populateModules(xmlFile)
    }
    /**
     * Throws runtime exception with the specified message.
     * @param msg
     */
    private void abortTransaction(final String msg) {
        throw new RuntimeException(msg);
    }
    /**
     * Parses the input xml file and populates the DB.
     * Assumption:
     *  Follows the following structure
     *
     * <pre>
     * <Module>
     *   <ModuleName>Ocap</ModuleName>
     *   <Function>
     *     <FunctionName>play</FunctionName>
     *     <Parameter>
     *       <ParameterName>locator</ParameterName>
     *       <ParameterType>integer</ParameterType>
     *       <ParameterValue>xxx</ParameterValue>
     *       <ParameterRange>0-5</ParameterRange>
     *     </Parameter>
     *   </Function>
     * </Module>
     * </pre>
     * @param xmlfilePath
     * @author ajith
     */
    public void populateModules(final String xmlfilePath) {
        try {
            File file = new File(xmlfilePath);
            XmlSlurper xmlSlurper = new XmlSlurper();
            GPathResult rootNode = xmlSlurper.parse( file );

            rootNode.Module?.each { moduleNode ->
                Module module = new Module()
                module.name =  moduleNode?.ModuleName
                module.testGroup = TestGroup.valueOf( moduleNode.TestGroup?.toString() )
                module.rdkVersion = moduleNode?.RdkVersion
                if(module.save()) {
                    log.info(" Saved Module Successfully "+module.name)
                    moduleNode.Function.each { functionNode ->
                        Function function = new Function();
                        function.name = functionNode?.FunctionName
                        function.module = module
                        if(function.save()) {
                            log.info(" Saved Function Successfully "+function.name)
                            functionNode.Parameter.each { parameterNode ->
                                ParameterType parameterType = new ParameterType()
                                parameterType.function = function
                                parameterType.name = parameterNode?.ParameterName
                                parameterType.parameterTypeEnum = ParameterTypeEnum.valueOf( parameterNode.ParameterType?.toString()?.toUpperCase() )
                                parameterType.rangeVal = parameterNode?.ParameterRange
                                if(parameterType.save()) {
                                    log.info(" Saved Parameter Successfully "+ parameterType?.name)
                                }
                                else {
                                    log.error( parameterType.errors)
                                    abortTransaction( " Parameter Save failed " )
                                }
                            }
                        }
                        else {
                            log.error(function.errors)
                            abortTransaction( " Function Save failed " )
                        }
                    }
                }
                else {
                    log.error(module.errors)
                    abortTransaction( " Module Save failed " )
                }
            }
        }
        catch ( ParserConfigurationException e ) {
            e.printStackTrace();
        }
        catch ( SAXException e ) {
            e.printStackTrace();
        }
        catch ( IOException e ) {
            e.printStackTrace();
        }
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
    public JsonObject getJsonData(final PrimitiveTest primitiveTest, final String idValue=ID_DEFAULT) {

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


    public void parseAndSaveBoxTypes() {
        String xmlFile =  SCH.servletContext.getRealPath( grailsApplication.config.boxdetails.xmlfile.location );
        populateBoxTypesToDB(xmlFile)
    }

    /**
     * Parses the input xml file and populates the DB.
     * Assumption:
     *  Follows the following structure
     *
     * <pre>
     * <Box>
     *     <SetTopBox>
     *       <Type>
     *           <BoxType>Xi3</BoxType>
     *       </Type>  
     *       <Model>
     *           <BoxModel>Intel</BoxModel>
     *       </Model>
     *       <Manufacturer>
     *           <BoxManufacturer>Arris</BoxManufacturer>
     *       </Manufacturer>
     *       <SoC>
     *           <SoCVendor>Parker</SoCVendor>
     *           <SoCVendor>Px001bn</SoCVendor>         
     *       </SoC>
     *     </SetTopBox>  
     *   </Box>
     * </pre>
     * @param xmlfilePath
     * @author sreejasuma
     */
    public populateBoxTypesToDB(final String xmlfilePath){
        try {
            File file = new File(xmlfilePath);
            XmlSlurper xmlSlurper = new XmlSlurper();
            GPathResult rootNode = xmlSlurper.parse( file );

            rootNode.SetTopBox?.each{ setTopBox ->

                setTopBox?.Type?.each { type ->
                    type.BoxType?.each { boxTypes ->
                        BoxType boxType = new BoxType();
                        boxType.name = boxTypes.BoxName
                        boxType.type = boxTypes.Type
                        if(boxType.save()) {
                            log.info(" Saved BoxType Successfully "+ boxType?.name)
                        }
                        else {
                            log.error boxType.errors
                            abortTransaction( " BoxType Save failed " )
                        }
                    }
                }

                setTopBox?.SoC?.each { soc ->
                    soc.SoCVendor?.each { soCVendors ->
                        SoCVendor soCVendor = new SoCVendor();
                        soCVendor.name = soCVendors
                        if(soCVendor.save()) {
                            log.info(" Saved SoCVendor Successfully "+ soCVendor?.name)
                        }
                        else {
                            log.error soCVendor.errors
                            abortTransaction( " SoCVendor Save failed " )
                        }
                    }
                }

                setTopBox?.Manufacturer?.each { manufacturer ->
                    manufacturer.BoxManufacturer?.each { boxManufacturers ->
                        BoxManufacturer boxManufacturer = new BoxManufacturer();
                        boxManufacturer.name = boxManufacturers
                        if(boxManufacturer.save()) {
                            log.info(" Saved BoxManufacturer Successfully "+ boxManufacturer?.name)
                        }
                        else {
                            log.error boxManufacturer.errors
                            abortTransaction( " BoxManufacturer Save failed " )
                        }
                    }
                }
            }

        }
        catch ( ParserConfigurationException e ) {
            e.printStackTrace();
        }
        catch ( SAXException e ) {
            e.printStackTrace();
        }
        catch ( IOException e ) {
            e.printStackTrace();
        }
    }


}
