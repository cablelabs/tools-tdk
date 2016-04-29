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
package com.comcast.rdk;

import static org.junit.Assert.*;
import org.codehaus.groovy.grails.web.context.ServletContextHolder as SCH


class PrimitiveServiceTests
{
    
    def primitivetestService
    
    def grailsApplication
    
    private void testPopulateModules() {
        
       println grailsApplication.config.modules.xmlfile.location
       String xmlFile =  SCH.servletContext.getRealPath( grailsApplication.config.modules.xmlfile.location );
       
       primitivetestService.parseAndSaveStubXml();
    }
    
    private void testJsonData() {
        primitivetestService.parseAndSaveStubXml();
        PrimitiveTest primitiveTest = new PrimitiveTest()
        primitiveTest.name = " Test 1"
        Module module = Module.findByName("Ocap")
        primitiveTest.module = module
        Function function = Function.findByName("play")
        primitiveTest.function = function
        Parameter parameter1 = new Parameter();
        ParameterType paramType1 = ParameterType.findByName("locator")
        parameter1.value = "3"
        parameter1.parameterType = paramType1
        
        if(!parameter1.save()) {
            println parameter1.errors
        }
        
        Parameter parameter2 = new Parameter();
        ParameterType paramType2 = ParameterType.findByName("frequency")
        parameter2.value = "50"
        parameter2.parameterType = paramType2
        
        if(!parameter2.save()) {
            println parameter2.errors
        }
        
        if(!primitiveTest.save()) {
            println primitiveTest
        }
        else {
            primitiveTest.addToParameters(parameter1)
            primitiveTest.addToParameters(parameter2)
        }
        
        println primitivetestService.getJsonData(primitiveTest)
        
        
        
    }
    
    void testExecute() {
//        primitivetestService.executeScript("print 'test'")
        println grailsApplication.config.EXEC_PATH
    }
    
    

}
